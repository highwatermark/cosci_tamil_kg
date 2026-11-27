/* Nilai v3 reel: one fixed viewport, 31 scenes, scroll-scrubbed and reversible.
   Each scene's progress p (0..1) comes from the scroll spacer. Elements carry keyframes:
   data-k (transform + opacity), data-m/data-mt (path morph), data-dr (stroke draw), data-tx (text swap), data-n (counter). */
(function(){
"use strict";
var root=document.documentElement;
function $(id){ return document.getElementById(id); }
var reel=$('reel'), file=$('top'), vp=$('vp'), spacer=$('spacer');
if(!reel||!vp) return;
var Q=location.search;
var RM=(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)||/[?&]motion=reduce\b/.test(Q);
var CHECK=/[?&]check=1\b/.test(Q);
var DBG=/[?&]p=/.test(Q);
if(RM) root.classList.add('rm');
var SC=[].slice.call(vp.querySelectorAll('.sc3'));
var MK=[].slice.call(spacer.querySelectorAll('.mk'));
var NSC=SC.length, TR=.075;
var phoneMQ=window.matchMedia('(max-aspect-ratio: 9/10), (max-width: 700px)');
var phone=phoneMQ.matches;

/* easing */
var E={
  l:function(t){return t;},
  i:function(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;},
  o:function(t){return 1-Math.pow(1-t,3);},
  n:function(t){return t*t*t;},
  b:function(t){var c1=1.9,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2);},
  s:function(t){return t<1?0:1;},
  e:function(t){return t===0||t===1?t:Math.pow(2,-9*t)*Math.sin((t*10-.75)*2.1)+1;}
};
function clamp(v,a,b){ return v<a?a:v>b?b:v; }

function parseK(s){
  var tr={}, times=[];
  if(!s) return tr;
  s.split(';').forEach(function(fr){
    var m=fr.match(/^\s*([\d.]+)([a-z]?):(.*)$/); if(!m) return;
    var t=+m[1], e=m[2]||'i'; times.push(t);
    m[3].split(',').forEach(function(pv){ var q=pv.split('='); if(q.length<2) return; (tr[q[0]]=tr[q[0]]||[]).push([t,+q[1],e]); });
  });
  for(var k in tr){
    tr[k].sort(function(a,b){return a[0]-b[0];});
    var t0=tr[k][0][0];
    if(t0>0){ var d=(k==='o'||k==='s'||k==='sx'||k==='sy')?1:0, tp=0; times.forEach(function(x){ if(x<t0&&x>tp) tp=x; }); tr[k].unshift([tp,d,'l']); if(tp>0) tr[k].unshift([0,d,'l']); }
  }
  return tr;
}
function val(tk,p){
  if(p<=tk[0][0]) return tk[0][1];
  for(var i=1;i<tk.length;i++){ var k=tk[i]; if(p<=k[0]){ var a=tk[i-1], d=k[0]-a[0], u=d>0?(p-a[0])/d:1; return a[1]+(k[1]-a[1])*E[k[2]](u); } }
  return tk[tk.length-1][1];
}
var NUM=/-?\d*\.?\d+/g;
function prep(sc){
  var S={el:sc, k:[], m:[], dr:[], tx:[], n:[], w:[]};
  [].forEach.call(sc.querySelectorAll('[data-k],[data-kp]'),function(el){
    var c=(el.getAttribute('data-c')||'').split(' ').map(Number);
    S.k.push({el:el, svg:el instanceof SVGElement, t:parseK(el.getAttribute('data-k')), tp:el.hasAttribute('data-kp')?parseK(el.getAttribute('data-kp')):null, cx:c[0]||0, cy:c[1]||0, last:''});
  });
  [].forEach.call(sc.querySelectorAll('[data-m]'),function(el){
    var ds=el.getAttribute('data-m').split('|'), ts=[], te=[];
    el.getAttribute('data-mt').split(',').forEach(function(s){ var q=s.split('-'); ts.push(+q[0]); te.push(q.length>1?+q[1]:+q[0]); });
    var tpl=ds[0].split(NUM), nums=ds.map(function(d){ return d.match(NUM).map(Number); });
    var ok=nums.every(function(a){return a.length===nums[0].length;});
    if(!ok){ console.warn('morph skeleton mismatch',el); return; }
    S.m.push({el:el, ts:ts, te:te, nums:nums, tpl:tpl, last:-1});
  });
  [].forEach.call(sc.querySelectorAll('[data-dr]'),function(el){
    var v=el.getAttribute('data-dr').split(',').map(Number);
    el.setAttribute('pathLength','1'); el.style.strokeDasharray='1 1';
    S.dr.push({el:el, v:v, last:-1});
  });
  [].forEach.call(sc.querySelectorAll('[data-tx]'),function(el){
    S.tx.push({el:el, v:el.getAttribute('data-tx').split('|').map(function(s){ var i=s.indexOf(':'); return [+s.slice(0,i), s.slice(i+1)]; }), last:null});
  });
  [].forEach.call(sc.querySelectorAll('[data-n]'),function(el){
    var v=el.getAttribute('data-n').split(','); S.n.push({el:el, v:v.slice(0,4).map(Number), fmt:v[4]||'', last:null});
  });
  [].forEach.call(sc.querySelectorAll('.sent .w'),function(el,i){ S.w.push({el:el,i:i}); });
  S.nw=S.w.length;
  S.art=sc.querySelector('svg.art');
  S.tr=sc.getAttribute('data-tr')||'fade';
  S.fx=+(sc.getAttribute('data-fx')||500); S.fy=+(sc.getAttribute('data-fy')||500);
  S.pu=(sc.getAttribute('data-pu')||'').split('|').filter(Boolean).map(function(s){ return s.split(':').map(Number); });
  S.stop=sc.querySelector('.sent .stop');
  S.dur=+sc.getAttribute('data-dur')||5.2;
  S.led=+(sc.getAttribute('data-led')||0);
  S.p=-1;
  return S;
}
var ST=SC.map(prep);

function render(S,p){
  if(S.p===p) return; S.p=p;
  var i, it;
  for(i=0;i<S.k.length;i++){
    it=S.k[i]; var T=(phone&&it.tp)?it.tp:it.t;
    var o=T.o?val(T.o,p):1, x=T.x?val(T.x,p):0, y=T.y?val(T.y,p):0, s=T.s?val(T.s,p):1,
        sx=(T.sx?val(T.sx,p):1)*s, sy=(T.sy?val(T.sy,p):1)*s, r=T.r?val(T.r,p):0;
    var key=o.toFixed(3)+x.toFixed(1)+y.toFixed(1)+sx.toFixed(3)+sy.toFixed(3)+r.toFixed(2);
    if(key===it.last) continue; it.last=key;
    if(it.svg){
      var tr='';
      if(x||y) tr+='translate('+x.toFixed(1)+' '+y.toFixed(1)+')';
      if(r||sx!==1||sy!==1){ tr+='translate('+it.cx+' '+it.cy+')'; if(r) tr+='rotate('+r.toFixed(2)+')'; if(sx!==1||sy!==1) tr+='scale('+sx.toFixed(4)+' '+sy.toFixed(4)+')'; tr+='translate('+(-it.cx)+' '+(-it.cy)+')'; }
      if(tr) it.el.setAttribute('transform',tr); else it.el.removeAttribute('transform');
      if(T.o){ it.el.setAttribute('opacity',o.toFixed(3)); it.el.style.visibility=o<.002?'hidden':''; }
    } else {
      it.el.style.transform=(x||y?'translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px) ':'')+(r?'rotate('+r.toFixed(2)+'deg) ':'')+(sx!==1||sy!==1?'scale('+sx.toFixed(4)+','+sy.toFixed(4)+')':'');
      if(T.o){ it.el.style.opacity=o.toFixed(3); it.el.style.visibility=o<.002?'hidden':''; }
    }
  }
  for(i=0;i<S.m.length;i++){
    it=S.m[i]; var ts=it.ts, te=it.te, a=0, b=0, u=0, last=ts.length-1;
    if(p>=te[last]){ a=b=last; }
    else { for(var j=0;j<=last;j++){ if(p<=te[j]){ if(p>=ts[j]||j===0){ a=b=j; } else { a=j-1; b=j; u=E.i((p-te[j-1])/(ts[j]-te[j-1])); } break; } } }
    var kk=a*1000+b+u; if(kk===it.last) continue; it.last=kk;
    var A=it.nums[a], B=it.nums[b], out=it.tpl[0];
    for(var q=0;q<A.length;q++){ out+=(A[q]+(B[q]-A[q])*u).toFixed(1)+it.tpl[q+1]; }
    it.el.setAttribute('d',out);
  }
  for(i=0;i<S.dr.length;i++){
    it=S.dr[i]; var v=it.v, e;
    e=E.i(clamp((p-v[0])/(v[1]-v[0]),0,1));
    if(v.length>3) e=e*(1-E.i(clamp((p-v[2])/(v[3]-v[2]),0,1)));
    if(e===it.last) continue; it.last=e;
    it.el.style.strokeDashoffset=(1-e).toFixed(4);
    it.el.style.visibility=e<.001?'hidden':'';
  }
  for(i=0;i<S.tx.length;i++){
    it=S.tx[i]; var cur=it.v[0][1];
    for(var z=0;z<it.v.length;z++) if(p>=it.v[z][0]) cur=it.v[z][1];
    if(cur!==it.last){ it.el.textContent=cur; it.last=cur; }
  }
  for(i=0;i<S.n.length;i++){
    it=S.n[i]; var w=it.v, u2=E.i(clamp((p-w[0])/(w[1]-w[0]),0,1)), nv=Math.round(w[2]+(w[3]-w[2])*u2);
    if(nv===it.last) continue; it.last=nv;
    it.el.textContent=it.fmt==='c'?nv.toLocaleString('en-US'):String(nv);
  }
  /* words: drop in one by one with a small wobble */
  for(i=0;i<S.nw;i++){
    it=S.w[i];
    var w0=.045+i*(.10/Math.max(S.nw,6)), uu=RM?1:clamp((p-w0)/.05,0,1);
    var key2=uu.toFixed(3); if(it.last===key2) continue; it.last=key2;
    if(uu>=1){ it.el.style.opacity=''; it.el.style.transform=''; continue; }
    var eb=E.b(uu);
    it.el.style.opacity=Math.min(1,uu*1.8).toFixed(3);
    it.el.style.transform='translateY('+((1-eb)*-.55).toFixed(3)+'em) rotate('+(Math.sin(uu*Math.PI*2)*(1-uu)*9).toFixed(2)+'deg)';
  }
}

/* layout of the scroll spacer */
var offs=[], hs=[], total=0, vh=window.innerHeight;
function fit(){
  vh=window.innerHeight; phone=phoneMQ.matches;
  ST.forEach(function(S){ S.p=-1; S.k.forEach(function(it){it.last='';}); S.m.forEach(function(it){it.last=-1;}); });
  if(RM){ offs=[]; return; }
  total=0;
  MK.forEach(function(m,i){ var h=Math.round(ST[i].dur/5.2*2.1*vh); m.style.height=h+'px'; offs[i]=total; hs[i]=h; total+=h; });
  spacer.style.height=(total+vh)+'px';
}

var cur=-1, curP=0, shown={};
function locate(y){
  if(y<=0) return [0,0];
  for(var i=NSC-1;i>=0;i--){ if(y>=offs[i]) return [i, clamp((y-offs[i])/hs[i],0,1)]; }
  return [0,0];
}
var head=$('reelHead'), cnt=$('reelCnt');
function setHead(i){
  var h=SC[i].getAttribute('data-h');
  if(head && head.textContent!==h){ head.textContent=h; head.classList.remove('swap'); void head.offsetWidth; head.classList.add('swap'); }
  if(cnt) cnt.textContent=(i<9?'0':'')+(i+1)+'/'+NSC;
  var cs=getComputedStyle(SC[i]);
  root.style.setProperty('--hw',cs.getPropertyValue('--wall')); root.style.setProperty('--ht',cs.getPropertyValue('--tx'));
  root.style.setProperty('--sw',cs.getPropertyValue('--strip')); root.style.setProperty('--sl',cs.getPropertyValue('--letters'));
}
function vis(i,on,z){
  var el=SC[i];
  if(on){ if(!shown[i]){ el.classList.add('on'); shown[i]=1; } el.style.zIndex=z; }
  else if(shown[i]){ el.classList.remove('on'); el.style.clipPath=''; el.style.transform=''; el.style.opacity=''; el.style.zIndex=''; delete shown[i]; }
}
function artPoint(S,x,y){
  var svg=S.art; if(!svg) return [innerWidth/2,innerHeight/2];
  var r=svg.getBoundingClientRect(); return [r.left+x/1000*r.width, r.top+y/1000*r.height];
}
var lastHead=-1;
function update(){
  if(tab!=='reel') return;
  if(RM){ rmUpdate(); return; }
  var L=locate(window.scrollY), i=L[0], p=L[1];
  if(i!==lastHead){ setHead(i); lastHead=i; hydrate(i); closeSrc(); }
  cur=i; curP=p;
  clips(i,p);
  var inTr=(i>0&&p<TR);
  for(var k=0;k<NSC;k++){ if(k!==i&&!(inTr&&k===i-1)) vis(k,false); }
  vis(i,true,2); render(ST[i],p);
  var el=SC[i];
  if(inTr){
    var prev=SC[i-1], P=ST[i-1]; vis(i-1,true,1); render(P,1);
    var u=E.i(p/TR), typ=ST[i].tr;
    if(typ==='zoom'){
      var fp=artPoint(P,P.fx,P.fy), R=Math.hypot(Math.max(fp[0],innerWidth-fp[0]),Math.max(fp[1],innerHeight-fp[1]));
      prev.style.transformOrigin=fp[0]+'px '+fp[1]+'px'; prev.style.transform='scale('+(1+u*u*3.2).toFixed(3)+')';
      el.style.clipPath='circle('+(u*R*1.05).toFixed(1)+'px at '+fp[0].toFixed(0)+'px '+fp[1].toFixed(0)+'px)';
      el.style.transform='scale('+(1.35-.35*u).toFixed(3)+')'; el.style.transformOrigin=fp[0]+'px '+fp[1]+'px';
    } else if(typ==='mat'){
      el.style.clipPath='inset(0 '+((1-u)*100).toFixed(2)+'% 0 0)'; el.style.transform=''; prev.style.transform='translateX('+(-u*6).toFixed(2)+'vw)';
    } else if(typ==='leaf'){
      el.style.clipPath='inset('+((1-u)*100).toFixed(2)+'% 0 0 0)'; el.style.transform=''; prev.style.transform='translateY('+(-u*5).toFixed(2)+'vh)';
    } else {
      el.style.clipPath=''; el.style.opacity=u.toFixed(3); el.style.transform='';
    }
    prop(typ,u);
  } else {
    el.style.clipPath=''; el.style.opacity=''; el.style.transform='';
    if(i>0){ SC[i-1].style.transform=''; }
    prop('',0);
  }
  strip(i,p);
  pulli(i,p);
}
/* images: lazy. A scene's images get their href when it is within one scene of the current one. */
function hydrateSc(k){
  var el=SC[k]; if(!el||el._hyd) return; el._hyd=1;
  [].forEach.call(el.querySelectorAll('[data-href]'),function(im){ im.setAttribute('href',im.getAttribute('data-href')); im.removeAttribute('data-href'); });
}
function hydrate(i){ for(var k=i-1;k<=i+2;k++) if(k>=0&&k<NSC) hydrateSc(k); }

/* scroll-scrubbed clips: a muted, inline video whose currentTime follows the scene progress inside its window.
   A keyed WebM plays with its own alpha; an MP4 on chroma green is keyed into a canvas. If the file is missing
   or fails, the scene keeps its image and SVG morph. */
var VC=[].map.call(SC,function(el){
  var fo=el.querySelector('foreignObject.vclip'); if(!fo) return null;
  var w=fo.getAttribute('data-win').split(',').map(Number);
  return {el:el, fo:fo, src:fo.getAttribute('data-src'), keyed:fo.getAttribute('data-keyed')==='1', t0:w[0], t1:w[1], v:null, cv:null, ok:false, dead:false, want:-1, busy:false};
});
function clipInit(c){
  if(c.v||c.dead) return;
  var v=document.createElement('video');
  v.muted=true; v.defaultMuted=true; v.playsInline=true; v.setAttribute('playsinline',''); v.setAttribute('muted',''); v.preload='auto';
  v.setAttribute('aria-hidden','true'); v.tabIndex=-1;
  v.addEventListener('loadeddata',function(){ c.ok=true; seek(c); });
  v.addEventListener('seeked',function(){ c.busy=false; draw(c); if(c.want>=0&&Math.abs(v.currentTime-c.want)>.02) seek(c); });
  v.addEventListener('error',function(){ c.dead=true; c.ok=false; c.el.classList.remove('vplay'); if(c.fo) c.fo.innerHTML=''; });
  if(c.keyed){ c.fo.appendChild(v); }
  else { c.cv=document.createElement('canvas'); c.fo.appendChild(c.cv); }
  v.src=c.src; c.v=v; try{ v.load(); }catch(e){}
}
function seek(c){
  var v=c.v; if(!c.ok||c.want<0||c.busy) return;
  var t=Math.min(Math.max(c.want,0),Math.max(0,(v.duration||0)-.04));
  if(Math.abs(v.currentTime-t)<.015){ draw(c); return; }
  c.busy=true; try{ v.currentTime=t; }catch(e){ c.busy=false; }
}
function draw(c){
  if(c.keyed||!c.cv) return;
  var v=c.v, vw=v.videoWidth, vh=v.videoHeight; if(!vw) return;
  var s=Math.min(vw,vh), sx=(vw-s)/2, sy=(vh-s)/2, n=Math.min(s,720), cv=c.cv;
  if(cv.width!==n){ cv.width=n; cv.height=n; }
  var g=cv.getContext('2d',{willReadFrequently:true});
  g.drawImage(v,sx,sy,s,s,0,0,n,n);
  var im=g.getImageData(0,0,n,n), d=im.data;
  for(var i=0;i<d.length;i+=4){ var r=d[i],gg=d[i+1],b=d[i+2],m=r>b?r:b, ex=gg-m;
    if(ex>40){ var a=ex>=110?0:1-(ex-40)/70; d[i+3]=a*255; d[i+1]=m+(gg-m)*0; } else if(ex>0){ d[i+1]=m; } }
  g.putImageData(im,0,0);
}
function clips(i,p){
  for(var k=0;k<VC.length;k++){
    var c=VC[k]; if(!c) continue;
    if(Math.abs(k-i)<=1) clipInit(c);
    if(k!==i||c.dead){ if(c.el.classList.contains('vplay')) c.el.classList.remove('vplay'); continue; }
    var inw=p>=c.t0&&p<=c.t1;
    c.el.classList.toggle('vplay',inw&&c.ok);
    if(inw&&c.ok){ c.want=(p-c.t0)/(c.t1-c.t0)*(c.v.duration||0); seek(c); }
  }
}

/* the wipe props: a rolling mat and a rising leaf */
var matEl=$('wipeMat'), leafEl=$('wipeLeaf');
function prop(typ,u){
  if(matEl){ if(typ==='mat'&&u>0&&u<1){ matEl.style.display='block'; matEl.style.transform='translateX('+(u*innerWidth-matEl.offsetWidth*.5).toFixed(1)+'px)'; matEl.style.backgroundPositionY=(u*900).toFixed(0)+'px'; matEl.style.setProperty('--d',(1-u*.6).toFixed(3)); } else matEl.style.display='none'; }
  if(leafEl){ if(typ==='leaf'&&u>0&&u<1){ leafEl.style.display='block'; leafEl.style.transform='translateY('+((1-u)*innerHeight-leafEl.offsetHeight*.5).toFixed(1)+'px)'; } else leafEl.style.display='none'; }
}

/* the ledger strip: one line per category, earned in the scene that carries it */
var stripEl=$('strip'), slots=stripEl?[].slice.call(stripEl.querySelectorAll('.sl')):[], card=$('ledCard'), cardT=$('ledCardT');
function strip(i,p){
  if(!stripEl) return;
  var on=(i>0||p>.84)&&i<NSC-1;
  stripEl.classList.toggle('on',on);
  var earned=0, showing=null;
  for(var k=0;k<=i;k++){ var L=ST[k].led; if(L){ if(k<i||p>.9) earned=Math.max(earned,L); if(k===i&&p>.74) showing=L; } }
  slots.forEach(function(s,j){ s.classList.toggle('w',j<earned); });
  if(card){
    if(showing&&p<.995){ var t=SC[i].getAttribute('data-ledt'); if(cardT.textContent!==t) cardT.textContent=t;
      var u=clamp((p-.74)/.05,0,1), v=clamp((p-.9)/.06,0,1);
      card.style.opacity=(u*(1-v)).toFixed(3); card.style.transform='translate('+(v*30).toFixed(1)+'vw,'+(-v*10).toFixed(1)+'vh) scale('+(1-v*.7).toFixed(3)+')'; card.style.visibility='';
    } else { card.style.opacity='0'; card.style.visibility='hidden'; }
  }
}

/* the pulli: the dot that travels. Cursor, full stop, kolam dot, star. */
var pu=$('pulli'), px=-99, py=-99, ptx=-99, pty=-99, praf=0, pvis=0;
function pulli(i,p){
  if(!pu) return;
  var S=ST[i], tgt=null;
  for(var k=0;k<S.pu.length;k++){ var w=S.pu[k]; if(p>=w[0]&&p<w[1]){ tgt=artPoint(S,w[2],w[3]); break; } }
  if(!tgt&&S.stop){ var r=S.stop.getBoundingClientRect(); if(r.width||r.height) tgt=[r.left+r.width*.5, r.bottom-r.height*.24]; }
  if(!tgt){ pvis=0; } else { pvis=1; ptx=tgt[0]; pty=tgt[1]; }
  if(!praf) praf=requestAnimationFrame(pstep);
}
var pt0=0;
function pstep(t){
  praf=0;
  if(px<-90){ px=ptx; py=pty; }
  var dx=ptx-px, dy=pty-py, d=Math.hypot(dx,dy);
  px+=dx*.22; py+=dy*.22;
  var hop=Math.min(d*.35,60);
  pu.style.transform='translate('+px.toFixed(1)+'px,'+(py-hop*.4).toFixed(1)+'px) scale('+(1+Math.min(d,80)/240).toFixed(3)+','+(1-Math.min(d,80)/400).toFixed(3)+')';
  pu.style.opacity=pvis?'1':'0';
  if(d>.5) praf=requestAnimationFrame(pstep);
}

/* reduced motion: a static stack of completed scenes */
function rmUpdate(){
  var y=window.scrollY+innerHeight*.4, i=0;
  for(var k=0;k<NSC;k++){ if(SC[k].offsetTop<=y) i=k; }
  if(i!==lastHead){ setHead(i); lastHead=i; closeSrc(); }
}
if(RM){ ST.forEach(function(S){ S.el.classList.add('on'); render(S,1); });
  if('IntersectionObserver' in window){ var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting) hydrateSc(SC.indexOf(e.target)); }); },{rootMargin:'100% 0px'}); SC.forEach(function(el){ io.observe(el); }); }
  else SC.forEach(function(el,k){ hydrateSc(k); }); }

/* frame loop */
var raf=0;
function req(){ if(!raf) raf=requestAnimationFrame(function(){ raf=0; update(); }); }
window.addEventListener('scroll',req,{passive:true});
window.addEventListener('resize',function(){ fit(); req(); });
if(phoneMQ.addEventListener) phoneMQ.addEventListener('change',function(){ fit(); req(); });

/* tabs, routed by location.hash: #reel (default) and #file; any id inside the file opens the file */
var tab=null, reelY=0, tabR=$('tabReel'), tabF=$('tabFile');
function jump(y){ try{ window.scrollTo({top:y,left:0,behavior:'instant'}); }catch(e){ window.scrollTo(0,y); } }
function show(which,target){
  if(which==='reel'){
    if(tab!=='reel'){ file.hidden=true; reel.hidden=false; root.classList.add('reel-on'); var was=tab; tab='reel'; fit(); lastHead=-1; if(was==='file') jump(reelY); }
  } else {
    if(tab==='reel'){ reelY=window.scrollY; stop(); }
    var first=tab!=='file';
    reel.hidden=true; file.hidden=false; root.classList.remove('reel-on'); tab='file';
    if(first){ try{ window.dispatchEvent(new Event('resize')); }catch(e){} }
    if(target==='top'){ if(first) jump(0); }
    else if(target){ var t=$(target); if(t&&first) t.scrollIntoView(); }
  }
  tabR.setAttribute('aria-current',tab==='reel'?'page':'false');
  tabF.setAttribute('aria-current',tab==='file'?'page':'false');
  var idx=$('idx'), ib=$('idxBtn'); if(idx&&!idx.hidden&&tab==='reel'){ idx.hidden=true; ib.setAttribute('aria-expanded','false'); }
  req();
}
function route(){
  var h=''; try{ h=decodeURIComponent(location.hash.slice(1)); }catch(e){ h=location.hash.slice(1); }
  if(!h||h==='reel') return show('reel');
  if(h==='file') return show('file','top');
  var t=$(h);
  if(t&&file.contains(t)) return show('file',h);
  show('reel');
}
window.addEventListener('hashchange',route);
tabF.addEventListener('click',function(e){ if(location.hash==='#file'){ e.preventDefault(); show('file','top'); jump(0); } });
tabR.addEventListener('click',function(e){ if(location.hash==='#reel'){ e.preventDefault(); show('reel'); } });
var brand=document.querySelector('.bar .brand');
if(brand) brand.addEventListener('click',function(e){ if(tab==='reel'){ e.preventDefault(); stop(); jump(0); } });

/* watch: plays every scene at its own duration, pauses on any input */
var wBtn=$('watchBtn'), wLbl=$('watchLbl'), playing=false, wraf=0, wlast=0, pos=0, rmT=0;
function label(){ wBtn.setAttribute('aria-pressed',playing?'true':'false'); wLbl.textContent=playing?'pause':'watch'; }
function wframe(t){
  if(!playing) return;
  var dt=wlast?Math.min(.1,(t-wlast)/1000):0; wlast=t;
  var L=locate(pos), i=L[0];
  pos+=hs[i]/ST[i].dur*dt;
  if(pos>=total){ pos=total; jump(pos); stop(); return; }
  jump(pos);
  wraf=requestAnimationFrame(wframe);
}
function rmTick(){
  if(!playing) return;
  var y=window.scrollY+8, nx=null;
  for(var k=0;k<NSC;k++){ if(SC[k].offsetTop>y){ nx=SC[k]; break; } }
  if(!nx){ stop(); return; }
  jump(nx.offsetTop); var i=SC.indexOf(nx); rmT=setTimeout(rmTick,ST[i].dur*1000);
}
function play(){
  if(tab!=='reel') return;
  playing=true; label();
  if(RM){ rmT=setTimeout(rmTick,1500); return; }
  pos=window.scrollY; if(pos>=total-2){ pos=0; jump(0); }
  wlast=0; cancelAnimationFrame(wraf); wraf=requestAnimationFrame(wframe);
}
function stop(){ if(!playing) return; playing=false; cancelAnimationFrame(wraf); clearTimeout(rmT); label(); }
wBtn.addEventListener('click',function(){ if(playing) stop(); else play(); });
var again=$('watchAgain'); if(again) again.addEventListener('click',function(){ stop(); jump(0); play(); });
['wheel','touchstart'].forEach(function(ev){ window.addEventListener(ev,function(){ stop(); },{passive:true}); });
window.addEventListener('pointerdown',function(e){ if(!e.target.closest||(!e.target.closest('#watchBtn')&&!e.target.closest('#watchAgain'))) stop(); });

/* keyboard: Space and the arrows step scene by scene (to each scene's settled FUTURE) */
var anim=0;
function anchors(){
  if(RM) return SC.map(function(s){ return s.offsetTop; });
  return offs.map(function(o,i){ return Math.round(o+hs[i]*.86); });
}
function glide(y){
  cancelAnimationFrame(anim);
  if(RM){ jump(y); return; }
  var y0=window.scrollY, t0=0, dur=Math.min(2200,700+Math.abs(y-y0)*.35);
  function f(t){ if(!t0) t0=t; var k=Math.min(1,(t-t0)/dur), e=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2; jump(y0+(y-y0)*e); if(k<1) anim=requestAnimationFrame(f); }
  anim=requestAnimationFrame(f);
}
document.addEventListener('keydown',function(e){
  if(tab!=='reel'||e.defaultPrevented||e.altKey||e.ctrlKey||e.metaKey) return;
  var t=e.target, tg=t&&t.tagName||'';
  if(/^(INPUT|TEXTAREA|SELECT)$/.test(tg)||(t&&t.isContentEditable)) return;
  if(srcP&&!srcP.hidden&&srcP.contains(t)&&e.key!=='Escape') return;
  var k=e.key, dir=0;
  if(k==='ArrowDown'||k==='ArrowRight'||k==='PageDown'||(k===' '&&!e.shiftKey)) dir=1;
  else if(k==='ArrowUp'||k==='ArrowLeft'||k==='PageUp'||(k===' '&&e.shiftKey)) dir=-1;
  if(!dir){ if(k!=='Tab'&&k!=='Shift') stop(); return; }
  if(k===' '&&(tg==='BUTTON'||tg==='A'||tg==='SUMMARY')) return;
  e.preventDefault(); stop();
  var a=anchors(), y=window.scrollY, i;
  if(dir>0){ for(i=0;i<a.length&&a[i]<=y+8;i++); if(i<a.length) glide(a[i]); }
  else { for(i=a.length-1;i>=0&&a[i]>=y-8;i--); glide(i>=0?a[i]:0); }
});

/* the source chip: the Tamil anchor, its reading and the margin open in a panel (a bottom sheet on phones) */
var srcP=$('srcPanel'), srcB=$('srcB'), srcT=$('srcT'), srcX=$('srcX'), srcBtn=null;
function openSrc(btn){
  var tp=$(btn.getAttribute('data-src')); if(!tp||!srcP) return;
  if(srcBtn===btn&&!srcP.hidden){ closeSrc(true); return; }
  closeSrc(); srcB.innerHTML=''; srcB.appendChild(tp.content.cloneNode(true));
  var sc=btn.closest('.sc3'); srcT.textContent='source · '+(sc?sc.getAttribute('data-n').padStart(2,'0'):'');
  srcP.hidden=false; srcBtn=btn; btn.setAttribute('aria-expanded','true'); srcP.scrollTop=0;
  try{ srcX.focus({preventScroll:true}); }catch(e){ srcX.focus(); }
}
function closeSrc(refocus){
  if(!srcP||srcP.hidden) return;
  srcP.hidden=true;
  if(srcBtn){ srcBtn.setAttribute('aria-expanded','false'); if(refocus){ try{ srcBtn.focus({preventScroll:true}); }catch(e){} } }
  srcBtn=null;
}
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('.srcchip');
  if(b){ e.preventDefault(); stop(); openSrc(b); return; }
  if(srcP&&!srcP.hidden&&!srcP.contains(e.target)) closeSrc();
});
if(srcX) srcX.addEventListener('click',function(){ closeSrc(true); });
document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&srcP&&!srcP.hidden){ e.preventDefault(); closeSrc(true); } },true);

/* debugging hook: ?s=12&p=.5 jumps to scene 12 at progress .5 */
function deb(){
  var ms=Q.match(/[?&]s=(\d+)/), mp=Q.match(/[?&]p=([\d.]+)/);
  if(ms&&!RM){ var i=clamp(+ms[1]-1,0,NSC-1), p=mp?+mp[1]:.5; jump(Math.round(offs[i]+hs[i]*p)); }
}
window.nilaiGo=function(s,p){ var i=clamp(s-1,0,NSC-1); jump(Math.round(offs[i]+hs[i]*p)); update(); return [i+1,p]; };

route(); fit(); deb(); hydrate(Math.max(0,cur)); update(); label();

/* ?check=1: colour self-test against the scene tokens */
if(CHECK){
  var run=function(){
    function rgb(s){ var m=String(s).match(/rgba?\(([^)]+)\)/); if(!m) return null; var v=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); if(v.length>3&&v[3]===0) return null; return v.slice(0,3); }
    function hex(h){ h=h.trim(); if(h[0]!=='#') return rgb(h); return [parseInt(h.substr(1,2),16),parseInt(h.substr(3,2),16),parseInt(h.substr(5,2),16)]; }
    function lum(c){ var a=c.map(function(v){ v/=255; return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4); }); return .2126*a[0]+.7152*a[1]+.0722*a[2]; }
    function cr(a,b){ var x=lum(a), y=lum(b); return (Math.max(x,y)+.05)/(Math.min(x,y)+.05); }
    function same(a,b){ return a&&b&&Math.abs(a[0]-b[0])<3&&Math.abs(a[1]-b[1])<3&&Math.abs(a[2]-b[2])<3; }
    var fails=[], n=0;
    function chk(sc,what,r,min){ n++; if(r<min-1e-6){ fails.push(sc+' '+what+' '+r.toFixed(2)+' < '+min); } }
    SC.forEach(function(el,i){
      var sid=i+1;
      var wasOn=el.classList.contains('on'); el.classList.add('on');
      var cs=getComputedStyle(el), tok={};
      ['wall','floor','tx','ink','col','acc','dk','pp','strip','letters'].forEach(function(k){ tok[k]=hex(cs.getPropertyValue('--'+k)); });
      chk(sid,'wall:floor',cr(tok.wall,tok.floor),1.6);
      chk(sid,'ink:colour',cr(tok.ink,tok.col),1.5);
      chk(sid,'text:wall',cr(tok.tx,tok.wall),4.5);
      chk(sid,'text:floor',cr(tok.tx,tok.floor),4.5);
      chk(sid,'accent:ink',cr(tok.acc,tok.ink),3);
      chk(sid,'strip letters',cr(tok.strip,tok.letters),4.5);
      ['ink','col'].forEach(function(k){ chk(sid,k+':wall',cr(tok[k],tok.wall),3); chk(sid,k+':floor',cr(tok[k],tok.floor),3); });
      /* html text */
      var hz=el.querySelector('.floor').getBoundingClientRect().top;
      [].forEach.call(el.querySelectorAll('.tx, .tx *'),function(t){
        if(!t.childNodes.length||![].some.call(t.childNodes,function(c){return c.nodeType===3&&c.textContent.trim();})) return;
        var c=rgb(getComputedStyle(t).color); if(!c) return;
        var r=t.getBoundingClientRect(), bg=(r.top+r.height/2)>hz?tok.floor:tok.wall;
        if(t.closest('.chip')) bg=tok.tx&&same(c,tok.wall)?tok.tx:bg;
        chk(sid,'text "'+t.textContent.trim().slice(0,24)+'"',cr(c,bg),4.5);
      });
      /* svg text: data-bg names the token behind it */
      [].forEach.call(el.querySelectorAll('svg.art text'),function(t){
        var c=rgb(getComputedStyle(t).fill); if(!c) return; var bgk=t.getAttribute('data-bg')||'pp', bg=tok[bgk]||tok.pp;
        chk(sid,'svg text "'+t.textContent.slice(0,18)+'"',cr(c,bg),4.5);
      });
      /* art fills and strokes, including gradient stops */
      var seen={};
      [].forEach.call(el.querySelectorAll('svg.art *'),function(t){
        if(t.closest('.sh,.fx,defs,clipPath,mask,[data-nochk],[data-stone]')||/^(text|tspan|g|use|clipPath|image|foreignObject)$/.test(t.tagName)) return;
        var st=getComputedStyle(t);
        ['fill','stroke'].forEach(function(pr){
          var v=st[pr]; if(!v||v==='none') return;
          var cols=[];
          var m=v.match(/url\("?#([^")]+)"?\)/);
          if(m){ var gr=document.getElementById(m[1]); if(!gr) return; [].forEach.call(gr.querySelectorAll('stop'),function(s){ var sc=getComputedStyle(s); if(+sc.stopOpacity>.5) cols.push(rgb(sc.stopColor)); }); }
          else cols.push(rgb(v));
          cols.forEach(function(c){
            if(!c||same(c,tok.wall)||same(c,tok.floor)) return;
            var key=pr+c.join(','); if(seen[key]) return; seen[key]=1;
            if(same(c,tok.acc)){ chk(sid,'accent on ink',cr(c,tok.ink),3); return; }
            chk(sid,'art '+pr+' rgb('+c.join(',')+') vs wall',cr(c,tok.wall),3);
            chk(sid,'art '+pr+' rgb('+c.join(',')+') vs floor',cr(c,tok.floor),3);
          });
        });
      });
      /* stone: the architecture (and the plinths) is background, so text keeps 4.5 and both art fills keep 3 on every shade */
      var sseen={};
      [].forEach.call(el.querySelectorAll('svg.arch *, svg.art [data-stone] *'),function(t){
        if(t.closest('[data-nochk],defs')&&!t.closest('linearGradient,radialGradient,pattern')) return;
        if(/^(g|defs|svg|pattern|linearGradient|radialGradient)$/.test(t.tagName)) return;
        var st=getComputedStyle(t), cols=[];
        if(t.tagName==='stop'){ if(+st.stopOpacity>.3) cols.push(rgb(st.stopColor)); }
        else ['fill','stroke'].forEach(function(pr){ var v=st[pr]; if(!v||v==='none'||/url\(/.test(v)) return; cols.push(rgb(v)); });
        cols.forEach(function(c){ if(!c) return; var key=c.join(','); if(sseen[key]) return; sseen[key]=1;
          chk(sid,'stone rgb('+key+') text',cr(tok.tx,c),4.5); chk(sid,'stone rgb('+key+') ink',cr(tok.ink,c),3); chk(sid,'stone rgb('+key+') colour',cr(tok.col,c),3); });
      });
      /* lighting: the darkest edge of the vignette, with the grain on top, still holds text 4.5 and art 3 on wall and floor */
      var vig=+cs.getPropertyValue('--vig')||0, noi=+cs.getPropertyValue('--noise')||0;
      function dk(c,a){ return c.map(function(v){ return v*(1-a); }); }
      [['wall',tok.wall],['floor',tok.floor]].forEach(function(b){ var c=dk(dk(b[1],vig),noi);
        chk(sid,'vignette '+b[0]+' text',cr(tok.tx,c),4.5); chk(sid,'vignette '+b[0]+' ink',cr(tok.ink,c),3); chk(sid,'vignette '+b[0]+' colour',cr(tok.col,c),3); });
      if(!wasOn&&!RM) el.classList.remove('on');
    });
    var msg='nilai check: '+n+' ratios, '+fails.length+' below threshold';
    if(fails.length){ console.warn(msg); fails.forEach(function(f){ console.warn('  '+f); }); } else console.log(msg);
    var box=document.createElement('pre'); box.id='chk'; box.textContent=msg+(fails.length?'\n'+fails.slice(0,40).join('\n'):'');
    document.body.appendChild(box); window.nilaiCheck={n:n,fails:fails};
    update();
  };
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(function(){ setTimeout(run,300); }); else setTimeout(run,800);
}
})();
