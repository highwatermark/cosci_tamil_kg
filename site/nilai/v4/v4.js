/* Nilai v4. One fixed grid (text column | stage), a scroll timeline T in units of one viewport.
   Every visual state is a pure function of T, so scrubbing is reversible; watch mode scrolls at a steady rate;
   reduced motion snaps each beat to its settled state. */
(function(){
"use strict";
var D=JSON.parse(document.getElementById('data').textContent);
var Q=location.search;
var RM=(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)||/[?&]motion=reduce\b/.test(Q);
var $=function(id){return document.getElementById(id);};
var stage=$('stage'), objs=$('objs'), shadows=$('shadows'), caps=$('caps'), thr=$('threads'), teach=$('teach'), gsvg=$('graph'), spacer=$('spacer'), seam=$('seam');
var cards=[].slice.call(document.querySelectorAll('.card'));
var NS='http://www.w3.org/2000/svg';
function clamp(v,a,b){return v<a?a:v>b?b:v;}
function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;}
function seg(T,a,b){return b<=a?(T>=b?1:0):clamp((T-a)/(b-a),0,1);}
function lerp(a,b,t){return a+(b-a)*t;}
function svg(tag,attrs,parent){ var e=document.createElementNS(NS,tag); for(var k in attrs) e.setAttribute(k,attrs[k]); if(parent) parent.appendChild(e); return e; }
function chOf(iid){ var m=/^c(\d+)_/.exec(iid); return m?+m[1]:-1; }

/* ---------- sprites: one element per instance; images load only near the current chapter ---------- */
var EL={}, SH={}, CP={};
var IDS=Object.keys(D.inst);
IDS.forEach(function(id){
  var it=D.inst[id], s=D.sprites[it.asset], el;
  if(s.missing){ el=document.createElement('div'); el.className='obj miss'; el.textContent=it.asset; }
  else { el=new Image(); el.alt=''; el.className='obj'; el.decoding='async'; el.draggable=false; el._src=s.src; }
  el._asset=it.asset; objs.appendChild(el); EL[id]=el;
  var sh=document.createElement('div'); sh.className='sh'; shadows.appendChild(sh); SH[id]=sh;
  var c=document.createElement('div'); c.className='cap'+(it.imag?' imag':''); c.textContent=it.cap; caps.appendChild(c); CP[id]=c;
});
var hydrated={};
function hydrate(ci){
  for(var k=ci-1;k<=ci+1;k++){ if(k<0||k>=D.chapters.length||hydrated[k]) continue; hydrated[k]=1;
    IDS.forEach(function(id){ if(chOf(id)===k&&EL[id]._src&&!EL[id].src) EL[id].src=EL[id]._src; });
    D.morphs.forEach(function(m){ if(m.clip&&chOf(m.then)===k) clipInit(m); });
    if(D.chapters[k].scene){ var im=new Image(); im.src=D.chapters[k].scene; } }
}
function track(id,T){
  var k=D.tracks[id]; if(!k) return null;
  if(T<=k[0][0]) return {x:k[0][1],s:k[0][2],r:k[0][3]};
  for(var i=1;i<k.length;i++){ if(T<=k[i][0]){ var a=k[i-1], b=k[i], u=ease(seg(T,a[0],b[0])); return {x:lerp(a[1],b[1],u),s:lerp(a[2],b[2],u),r:lerp(a[3],b[3],u)}; } }
  var z=k[k.length-1]; return {x:z[1],s:z[2],r:z[3]};
}

/* ---------- threads: drawn from the source verse; a symmetric link draws from both ends to meet at the top ---------- */
var TH={};
D.threads.forEach(function(t){
  var o={t:t};
  o.p1=svg('path',{fill:'none',stroke:'var(--thread)','stroke-width':'2.2','stroke-linecap':'round',pathLength:'1','stroke-dasharray':'1 1'},thr);
  o.p2=svg('path',{fill:'none',stroke:'var(--thread)','stroke-width':'2.2','stroke-linecap':'round',pathLength:'1','stroke-dasharray':'1 1'},thr);
  o.a=svg('circle',{r:'4.5',fill:'var(--thread)'},thr); o.b=svg('circle',{r:'4.5',fill:'var(--thread)'},thr);
  TH[t.id]=o;
});
var TE={};
Object.keys(D.teach).forEach(function(id){
  var d=document.createElement('div'); d.className='tblock'; d.style.display='none';
  var h=document.createElement('p'); h.className='th'; h.textContent=D.teach[id].head; d.appendChild(h);
  var p=document.createElement('p'); p.className='tt';
  var words=D.teach[id].text.split(' ');
  words.forEach(function(w,i){ var s=document.createElement('span'); s.className='w'; s.textContent=w+(i<words.length-1?' ':''); p.appendChild(s); });
  d.appendChild(p); teach.appendChild(d);
  TE[id]={el:d,w:[].slice.call(p.children)};
});
function cubicSplit(p0,p1,p2,p3){   // de Casteljau at t=.5: two halves, each from its outer end inward
  function m(a,b){return [(a[0]+b[0])/2,(a[1]+b[1])/2];}
  var a=m(p0,p1), b=m(p1,p2), c=m(p2,p3), d=m(a,b), e=m(b,c), f=m(d,e);
  return [[p0,a,d,f],[p3,c,e,f]];
}
function pd(q){ return 'M'+q[0][0].toFixed(1)+' '+q[0][1].toFixed(1)+' C'+q[1][0].toFixed(1)+' '+q[1][1].toFixed(1)+' '+q[2][0].toFixed(1)+' '+q[2][1].toFixed(1)+' '+q[3][0].toFixed(1)+' '+q[3][1].toFixed(1); }

/* ---------- graph ---------- */
var GE=svg('g',{},gsvg), GD=svg('g',{},gsvg), GR=svg('g',{},gsvg), GS=svg('g',{},gsvg), GL=svg('g',{},gsvg);
var maxc=1; D.edges.forEach(function(e){ if(e[4]>maxc) maxc=e[4]; });
var NE=D.edges.length;
var edgeEls=D.edges.map(function(e,i){
  var mx=(e[0]+e[2])/2, my=(e[1]+e[3])/2, cx=lerp(mx,500,.55), cy=lerp(my,500,.55);
  var w=Math.log(1+e[4])/Math.log(1+maxc);
  var p=svg('path',{d:'M'+e[0]+' '+e[1]+' Q'+cx.toFixed(1)+' '+cy.toFixed(1)+' '+e[2]+' '+e[3],fill:'none',stroke:'var(--thread)','stroke-width':(0.5+1.6*w).toFixed(2),'vector-effect':'non-scaling-stroke'},GE);
  p._o=0.10+0.38*w; p._rank=(NE-1-i)/Math.max(1,NE-1);   // heaviest first
  return p;
});
var NG=9, groupEls=[];
for(var gi=0;gi<NG;gi++) groupEls.push(svg('g',{},GD));
D.dots.forEach(function(d){ svg('circle',{cx:d[0],cy:d[1],r:'2.6',fill:'var(--ink2)'},groupEls[d[2]]); });
var labEls=D.labels.map(function(l){ var t=svg('text',{'class':'gl','text-anchor':l.anchor,'dominant-baseline':'middle'},GL); t.textContent=l.t; return t; });
/* every book named, small, beside its cluster: the first look at the graph should say what is in it */
var bookEls=D.books.map(function(b){ var t=svg('text',{'class':'bl','text-anchor':b.anchor,'dominant-baseline':'middle',x:b.x,y:b.y},GL); t.textContent=b.t; return t; });
function qpath(a,b){ var mx=(a[0]+b[0])/2, my=(a[1]+b[1])/2, cx=lerp(mx,500,.45), cy=lerp(my,500,.45); return 'M'+a[0]+' '+a[1]+' Q'+cx.toFixed(1)+' '+cy.toFixed(1)+' '+b[0]+' '+b[1]; }
var CHG=D.chapters.map(function(c){
  var g=svg('g',{},GR), o={g:g,routes:[],dots:{},labs:{}};
  c.route.forEach(function(r){ o.routes.push(svg('path',{d:qpath(c.dots[r[0]],c.dots[r[1]]),fill:'none',stroke:'var(--thread)','stroke-linecap':'round',pathLength:'1','stroke-dasharray':'1 1'},g)); });
  Object.keys(c.dots).forEach(function(id){
    o.dots[id]=svg('circle',{cx:c.dots[id][0],cy:c.dots[id][1],fill:'var(--thread)',stroke:'var(--ink)'},g);
    var t=svg('text',{'class':'rl'},GS); t.textContent=(c.labs&&c.labs[id])||id; o.labs[id]=t;
  });
  return o;
});

/* ---------- clips: a muted video scrubbed by T, keyed off chroma green into a canvas ---------- */
function clipInit(m){
  var c=m.clip; if(c.v||c.dead) return;
  var v=document.createElement('video');
  v.muted=true; v.defaultMuted=true; v.playsInline=true; v.setAttribute('playsinline',''); v.setAttribute('muted',''); v.preload='auto';
  v.setAttribute('aria-hidden','true'); v.tabIndex=-1;
  v.addEventListener('loadeddata',function(){ c.ok=true; seek(c); });
  v.addEventListener('seeked',function(){ c.busy=false; draw(c); if(c.want>=0&&Math.abs(v.currentTime-c.want)>.02) seek(c); });
  v.addEventListener('error',function(){ c.dead=true; c.ok=false; if(c.cv) c.cv.style.visibility='hidden'; });
  c.cv=document.createElement('canvas'); c.cv.className='clip'; objs.appendChild(c.cv);
  v.src=c.src; c.v=v; c.want=-1; try{ v.load(); }catch(e){}
}
function seek(c){
  var v=c.v; if(!c.ok||c.want<0||c.busy) return;
  var t=Math.min(Math.max(c.want,0),Math.max(0,(v.duration||0)-.04));
  if(Math.abs(v.currentTime-t)<.015){ draw(c); return; }
  c.busy=true; try{ v.currentTime=t; }catch(e){ c.busy=false; }
}
function draw(c){
  var v=c.v, vw=v.videoWidth, vh=v.videoHeight; if(!vw) return;
  var s=Math.min(vw,vh), sx=(vw-s)/2, sy=(vh-s)/2, n=Math.min(s,640), cv=c.cv;
  if(cv.width!==n){ cv.width=n; cv.height=n; }
  var g=c.g||(c.g=cv.getContext('2d',{willReadFrequently:true}));
  g.drawImage(v,sx,sy,s,s,0,0,n,n);
  var im=g.getImageData(0,0,n,n), d=im.data, L=d.length, i, r, gg, b, mm, ex, a;
  /* alpha from the green excess over max(r,b), a soft ramp, then despill (green clamped to max(r,b)) */
  for(i=0;i<L;i+=4){ r=d[i]; gg=d[i+1]; b=d[i+2]; mm=r>b?r:b; ex=gg-mm;
    if(ex>18){ a=ex>=78?0:1-(ex-18)/60; a=a*a*(3-2*a); d[i+3]=a*255; d[i+1]=mm; }
    else if(ex>0){ d[i+1]=mm; } }
  var A=c.A&&c.A.length===L/4?c.A:(c.A=new Uint8Array(L/4)), j, w=n;
  for(j=0,i=3;i<L;i+=4,j++) A[j]=d[i];
  for(j=w;j<A.length-w;j++){ if(A[j]===0||A[j]===255&&A[j-1]===255&&A[j+1]===255&&A[j-w]===255&&A[j+w]===255) continue;
    var mn=A[j]; if(A[j-1]<mn) mn=A[j-1]; if(A[j+1]<mn) mn=A[j+1]; if(A[j-w]<mn) mn=A[j-w]; if(A[j+w]<mn) mn=A[j+w]; d[j*4+3]=mn; }
  g.putImageData(im,0,0);
  /* the encoded frames carry a dark edge row the key cannot see as green: drop a thin border */
  var e=Math.ceil(n*.006)+1; g.clearRect(0,0,n,e); g.clearRect(0,n-e,n,e); g.clearRect(0,0,e,n); g.clearRect(n-e,0,e,n);
  c.drawn=true;
}

/* ---------- layout ---------- */
var L={}, phone=false;
var colEl=$('col'), cardsEl=$('cards'), hd=$('hd');
function layout(){
  phone=matchMedia('(max-width:700px),(max-aspect-ratio:9/10)').matches;
  if(phone){ document.documentElement.style.setProperty('--band',Math.max(250,Math.round(innerHeight*.42))+'px'); }
  var W=stage.clientWidth, H=stage.clientHeight;
  L.W=W; L.H=H;
  L.fy=Math.round(H*(phone?.86:.82));
  document.documentElement.style.setProperty('--fy',L.fy+'px');
  // teaching text at the top of the stage: measure the tallest
  L.tx=Math.round(W*(phone?.05:.08)); L.tw=Math.round(W*(phone?.9:.84)); L.ty=Math.round(H*(phone?.03:.05));
  teach.style.left=L.tx+'px'; teach.style.top=L.ty+'px'; teach.style.width=L.tw+'px';
  var th=0; Object.keys(TE).forEach(function(id){ var e=TE[id].el; e.style.display='block'; th=Math.max(th,e.offsetHeight); e.style.display='none'; });
  L.apex=L.ty+th+Math.round(H*.03);
  var S=D.slots.S;
  // heights by visual weight: equal outline area, capped by the room under the teaching text and by width
  var hc=Math.min(L.fy-H*.07, (L.fy-L.apex-H*.035)/S), At=hc*hc*.42;
  L.hc=hc;
  var size={};
  Object.keys(D.sprites).forEach(function(a){ var s=D.sprites[a], r=s.w/s.h;
    var h=Math.min(hc, Math.sqrt(At/r)*s.k, (W*.40/S)/r, W*(phone?.80:.62)/r);
    size[a]=[Math.max(40,h)*r, Math.max(40,h)]; });
  IDS.forEach(function(id){ var el=EL[id], z=size[el._asset]; el.style.width=z[0].toFixed(1)+'px'; el.style.height=z[1].toFixed(1)+'px'; el._w=z[0]; el._h=z[1]; });
  thr.setAttribute('viewBox','0 0 '+W+' '+H);
  spacer.style.height=(D.total*unit()+innerHeight)+'px';
  clampCards();
  render(curT(),true);
}
function unit(){ return innerHeight; }
function clampCards(){
  var avail=cardsEl.clientHeight;
  cards.forEach(function(c){
    var rd=c.querySelector('.rd.clamp'), mb=c.querySelector('.more'), ct=c.querySelector('.cite'); if(!rd) return;
    rd.style.webkitLineClamp=''; rd.style.display=''; rd.classList.remove('on'); if(mb) mb.style.display='none'; if(ct) ct.style.display='';
    [].forEach.call(c.querySelectorAll('.lab'),function(l){ l.style.display=''; });
    var over=c.scrollHeight-avail;
    if(over>1){ var lh=parseFloat(getComputedStyle(rd).lineHeight)||20, lines=Math.max(2,Math.floor((rd.offsetHeight-over-(mb?28:0))/lh));
      rd.classList.add('on'); rd.style.webkitLineClamp=String(lines); if(mb) mb.style.display='inline-block';
      // the id line repeats the source line above the verse: the first thing to go when the reading still does not fit
      if(ct&&c.scrollHeight>avail+1) ct.style.display='none';
      while(c.scrollHeight>avail+1&&lines>1){ lines--; rd.style.webkitLineClamp=String(lines); }
      // a verse too long for the band keeps only "read all", which opens the whole card
      var lb=rd.previousElementSibling&&rd.previousElementSibling.classList.contains('lab')?rd.previousElementSibling:null;
      if(c.scrollHeight>avail+1){ rd.style.display='none'; if(lb) lb.style.display='none'; } }
  });
}

/* ---------- render ---------- */
function vis(el,o){ el.style.opacity=o.toFixed(3); el.style.visibility=o>0.001?'visible':'hidden'; }
function beatAt(T){ for(var i=0;i<D.beats.length;i++){ var b=D.beats[i]; if(T<b.start+b.len) return b; } return D.beats[D.beats.length-1]; }
var MO={}; D.morphs.forEach(function(m){ MO[m.then]=MO[m.then]||[]; MO[m.then].push(m); MO[m.fut]=[m]; });
var lastKey='', curCh=-2;
function render(T,force){
  if(RM){ var bb=beatAt(T); T=bb.start+bb.len-1e-4; }
  var key=T.toFixed(4); if(key===lastKey&&!force) return; lastKey=key;
  var W=L.W, H=L.H, bt=beatAt(T);
  var ci=bt.ch!=null?bt.ch:(bt.id==='Z'?D.chapters.length-1:0);
  hydrate(ci);
  if(bt.ch!==curCh){ curCh=bt.ch; header(bt); }
  // morph state per morph
  var mst={}, seamOn=null;
  D.morphs.forEach(function(m){ var u=seg(T,m.a,m.b); mst[m.then+'>'+m.fut]=u; });
  var objState={};
  IDS.forEach(function(id){
    var st=track(id,T), el=EL[id];
    var op=1, mask=null;
    if(st&&st.r>0.0005&&MO[id]){
      MO[id].forEach(function(m){
        var u=mst[m.then+'>'+m.fut], isThen=(m.then===id), live=(u>0&&u<1);
        if(isThen&&T<m.a-1e-6) return;
        if(m.clip&&m.clip.ok&&!m.clip.dead){ op*=isThen?1-seg(u,0,.12):seg(u,.88,1); }
        else if(live){ mask={u:u,then:isThen,m:m}; }
        else op*=isThen?(u>=1?0:1):(u>0?1:0);
      });
    }
    if(!st||st.r<=0.0005||op<=0.001){ el.style.visibility='hidden'; vis(SH[id],0); vis(CP[id],0); objState[id]=null; return; }
    var w=el._w, h=el._h, cx=st.x*W, sink=(1-st.r)*(h*st.s+12);
    el.style.visibility='visible'; el.style.opacity=op.toFixed(3);
    el.style.transform='translate('+(cx-w/2).toFixed(1)+'px,'+sink.toFixed(1)+'px) scale('+st.s.toFixed(4)+')';
    objState[id]={cx:cx, top:L.fy-h*st.s+sink, r:st.r, s:st.s, h:h*st.s, w:w*st.s};
    if(mask){ el._mask=mask; } else if(el._masked){ el.style.webkitMaskImage=el.style.maskImage=''; el._masked=false; }
    var sh=SH[id]; sh.style.left=(cx-w*st.s*.47).toFixed(1)+'px'; sh.style.width=(w*st.s*.94).toFixed(1)+'px'; vis(sh,Math.pow(st.r,3)*op);
    var c=CP[id]; c.style.left=cx.toFixed(1)+'px';
    var co=seg(st.r,.94,1)*op;
    if(MO[id]){ MO[id].forEach(function(m){ var u=mst[m.then+'>'+m.fut]; if(u>0) co*=(m.then===id)?(1-seg(u,.3,.5)):seg(u,.5,.7); }); }
    vis(c,co);
  });
  // seam wipes: the then-object is cut away from the floor up along a gold seam that reveals the future one
  D.morphs.forEach(function(m){
    var u=mst[m.then+'>'+m.fut]; if(!(u>0&&u<1)||(m.clip&&m.clip.ok&&!m.clip.dead)) return;
    var a=objState[m.then], b=objState[m.fut]; if(!a||!b) return;
    var Hm=Math.max(a.h,b.h)+24, ys=ease(u)*Hm-12;
    [[m.then,true],[m.fut,false]].forEach(function(q){
      var el=EL[q[0]], o=objState[q[0]], y=clamp(ys/o.s,-20,el._h+20), g;
      g=q[1]?'linear-gradient(to top, transparent 0, transparent '+y.toFixed(1)+'px, #000 '+(y+16).toFixed(1)+'px)'
            :'linear-gradient(to top, #000 0, #000 '+(y-2).toFixed(1)+'px, transparent '+(y+14).toFixed(1)+'px)';
      el.style.webkitMaskImage=el.style.maskImage=g; el._masked=true;
    });
    var wmax=Math.max(a.w,b.w)*1.08;
    seamOn={x:(a.cx-wmax/2), y:L.fy-ys, w:wmax, o:Math.sin(Math.PI*u)};
  });
  if(seamOn){ seam.style.left=seamOn.x.toFixed(1)+'px'; seam.style.top=seamOn.y.toFixed(1)+'px'; seam.style.width=seamOn.w.toFixed(1)+'px'; vis(seam,seamOn.o); } else vis(seam,0);
  // clips
  D.morphs.forEach(function(m){
    var c=m.clip; if(!c||!c.cv) return;
    var u=mst[m.then+'>'+m.fut], o=c.ok&&!c.dead?seg(u,.04,.14)*(1-seg(u,.86,.96)):0;
    if(o<=0.001){ c.cv.style.visibility='hidden'; return; }
    var size=L.hc*c.size, cx=W*D.slots.C;
    c.cv.style.width=c.cv.style.height=size.toFixed(1)+'px';
    c.cv.style.transform='translate('+(cx-size/2).toFixed(1)+'px,'+(L.fy-size+c.drop*size).toFixed(1)+'px)';
    vis(c.cv,o);
    c.want=c.c0+seg(u,.08,.92)*(c.c1-c.c0); seek(c);
  });
  // threads
  D.threads.forEach(function(t){
    var o=TH[t.id], a=objState[t.a], b=objState[t.b];
    var dr=seg(T,t.d0,t.d1), fade=1-seg(T,t.f0,t.f1);
    if(!a||!b||dr<=0||fade<=0||a.r<.99||b.r<.99){ [o.p1,o.p2,o.a,o.b].forEach(function(e){e.style.opacity=0;}); }
    else{
      var src=t.sym?a:(t.s===t.a?a:b), dst=t.sym?b:(t.s===t.a?b:a);
      var x1=src.cx, y1=src.top-10, x2=dst.cx, y2=dst.top-10, ap=Math.min(L.apex, Math.min(y1,y2)-24);
      var q=[[x1,y1],[x1,ap],[x2,ap],[x2,y2]], e=ease(dr);
      if(t.sym){ var h=cubicSplit(q[0],q[1],q[2],q[3]);
        o.p1.setAttribute('d',pd(h[0])); o.p2.setAttribute('d',pd(h[1]));
        o.p1.setAttribute('stroke-dashoffset',(1-e).toFixed(4)); o.p2.setAttribute('stroke-dashoffset',(1-e).toFixed(4));
        o.p2.style.opacity=fade; o.b.style.opacity=fade; }
      else { o.p1.setAttribute('d',pd(q)); o.p1.setAttribute('stroke-dashoffset',(1-e).toFixed(4)); o.p2.style.opacity=0; o.b.style.opacity=fade*seg(dr,.96,1); }
      o.p1.style.opacity=fade; o.a.setAttribute('cx',x1); o.a.setAttribute('cy',y1); o.a.style.opacity=fade;
      o.b.setAttribute('cx',x2); o.b.setAttribute('cy',y2);
    }
    var te=TE[t.id];
    if(te){ if(dr>0&&fade>0){ te.el.style.display='block'; var n=te.w.length, pr=dr*(n+2);
        te.w.forEach(function(s,i){ s.style.opacity=clamp(pr-i,0,1).toFixed(2); }); te.el.style.opacity=fade; }
      else te.el.style.display='none'; }
  });
  renderGraph(T,W,H,bt);
  renderFuture(T,W,H);
  renderPro(T);
  // cards: a card shows once its beat has settled and stays until the next beat's card arrives,
  // so the column crossfades from text to text instead of standing empty while the stage moves
  cards.forEach(function(c){
    var b=c._b; if(!b) return;
    var s0=b.start+(b.card!=null?b.card:b.settle)*b.len, nb=D.beats[b._i+1];
    if(b.card===0&&b.start>0) s0-=.06;   // a card due at its beat's start crossfades with the one leaving
    // the imagined card leaves with its own chapter; every other card stays until the next card arrives
    var e0=!nb?1e9:b.kind==='imagined'?b.start+b.len-.08:nb.start+(nb.card!=null?nb.card:nb.settle)*nb.len-.08;
    var o=(b.start===0?1:seg(T,s0,s0+.08))*(1-seg(T,e0,e0+.08));
    vis(c,o);
  });
}
function renderGraph(T,W,H,bt){
  var G=D.graph, go=0, z=0, cz=null, C=D.chapters;
  var out0=C[0].g.out;
  if(T<C[0].g.out[1]) go=1-seg(T,out0[0],out0[1]);
  for(var i=1;i<C.length;i++){ var g=C[i].g; if(T>=g.in[0]&&T<=g.out[1]){ go=seg(T,g.in[0],g.in[1])*(1-seg(T,g.out[0],g.out[1])); } }
  if(T>=G.close[0]) go=seg(T,G.close[0],G.close[1]);
  if(T<C[0].start) go*=seg(T,G.intro_in[0],G.intro_in[1]);
  vis(gsvg,go);
  $('floor').style.opacity=(1-seg(go,0,.4)).toFixed(3);
  if(go<=0) return;
  var ci=-1;
  for(var k=0;k<C.length;k++){ var g2=C[k].g; if(T>=g2.in[0]&&T<=g2.out[1]){ ci=k; z=ease(seg(T,g2.zoom[0],g2.zoom[1])); } }
  if(T>=G.close[0]) { ci=-1; z=0; }
  var asp=W/H, fw=1000, fh=1000; if(asp>1) fw=1000*asp; else fh=1000/asp;
  var cw=fw, chh=fh, ccx=500, ccy=500;
  if(ci>=0&&z>0){ var bx=C[ci].box, bw=Math.max(bx[2]-bx[0],1), bh=Math.max(bx[3]-bx[1],1);
    var tw=Math.max(bw*1.9, bh*1.9*asp, 300*Math.max(1,asp)), thh=tw/asp;
    cw=lerp(fw,tw,z); chh=lerp(fh,thh,z); ccx=lerp(500,(bx[0]+bx[2])/2,z); ccy=lerp(500,(bx[1]+bx[3])/2,z); }
  gsvg.setAttribute('viewBox',(ccx-cw/2).toFixed(1)+' '+(ccy-chh/2).toFixed(1)+' '+cw.toFixed(1)+' '+chh.toFixed(1));
  var ppu=W/cw, fs=13/ppu;
  // the opening builds: groups of books appear one after another, then the bridges, heaviest first
  var dIn=G.dots, span=(dIn[1]-dIn[0]);
  groupEls.forEach(function(g,i){ var a=dIn[0]+i*span/12; g.style.opacity=seg(T,a,a+span/4).toFixed(3); });
  var ein=seg(T,G.edges[0],G.edges[1]), intro=T<C[0].start;
  edgeEls.forEach(function(p){ var f=intro?seg(ein,p._rank*.7,p._rank*.7+.3):1; p.setAttribute('stroke-opacity',(p._o*f).toFixed(3)); });
  GE.style.opacity=(intro?1:.5*(1-.5*z)).toFixed(3);
  GD.style.opacity=(1-.62*z).toFixed(3);
  labEls.forEach(function(t,i){ var l=D.labels[i], gi=i, a=dIn[0]+gi*span/12, rr=l.r+fs*.9*Math.abs(Math.sin(l.a))+fs*.3;
    t.setAttribute('x',(500+rr*Math.cos(l.a)).toFixed(1)); t.setAttribute('y',(500+rr*Math.sin(l.a)).toFixed(1)); t.setAttribute('font-size',fs.toFixed(2));
    t.style.opacity=((1-z)*seg(T,a,a+span/4)).toFixed(3); });
  var bo=(T<C[0].start||T>=G.close[0])?1:.8;
  bookEls.forEach(function(t,i){ var b=D.books[i], a=dIn[0]+b.g*span/12; t.setAttribute('font-size',(fs*.8).toFixed(2));
    t.style.opacity=(bo*seg(T,a+span/8,a+span/3)).toFixed(3); });
  hideOverlaps(labEls,bookEls);
  // routes: all thirteen in the G2 flash and the close; one chapter's in its title beat
  var flash=seg(T,G.flash[0],G.flash[1])*(T<C[0].start?1:0), close=seg(T,G.close_route[0],G.close_route[1])*(T>=G.close[0]?1:0);
  CHG.forEach(function(o,k){
    var own=(k===ci)?seg(T,C[k].g.route[0],C[k].g.route[1]):0, p=Math.max(own,flash,close), labOn=(k===ci)?own:0;
    o.g.style.opacity=p>0?1:0;
    o.routes.forEach(function(r){ r.setAttribute('stroke-width',((own>0?3.2:2.0)/ppu).toFixed(2)); r.setAttribute('stroke-dashoffset',(1-ease(p)).toFixed(4)); });
    Object.keys(o.dots).forEach(function(id){ var c=o.dots[id]; c.setAttribute('r',((own>0?3+(phone?2:4)*own:3)/ppu).toFixed(2)); c.setAttribute('stroke-width',(1/ppu).toFixed(2)); c.style.opacity=p>0?Math.min(1,p*2):0;
      var t=o.labs[id], P=C[k].dots[id], dx=P[0]>ccx?-1:1;
      t.setAttribute('font-size',fs.toFixed(2)); t.setAttribute('stroke-width',(5/ppu).toFixed(2));
      t.setAttribute('x',(P[0]+dx*12/ppu).toFixed(1)); t.setAttribute('y',P[1].toFixed(1)); t.setAttribute('text-anchor',dx<0?'end':'start'); t.setAttribute('dominant-baseline','middle');
      t.style.opacity=labOn>.5?seg(labOn,.5,1):0; });
  });
}
/* ---------- prologue: full screen, its own layout, before the page settles into column and stage ---------- */
var PRO=D.pro, proEl=$('pro'), heroA=$('heroA'), heroB=$('heroB'), scrim=$('scrim'), proYear=$('proYear'), proLine=$('proLine'), proObjs=$('proObjs'), proSt=$('proSt');
if(PRO.hero.past) heroA.src=PRO.hero.past; if(PRO.hero.future) heroB.src=PRO.hero.future;
var PT={}; [].forEach.call(proEl.querySelectorAll('.pt'),function(e){ PT[e.getAttribute('data-b')]=e; });
[].forEach.call(proEl.querySelectorAll('img[data-src]'),function(i){ i.src=i.getAttribute('data-src'); });
var PO=PRO.objs.map(function(o){ var w=document.createElement('div'); w.className='po'; var a=new Image(), b=new Image();
  a.src=o.a; b.src=o.b; a.alt=b.alt=''; w.appendChild(a); w.appendChild(b); proObjs.appendChild(w); return {w:w,a:a,b:b,o:o}; });
var stEls=[].slice.call(proSt.children);
var lineP=svg('path',{fill:'none',stroke:'#e9cf8f','stroke-width':'2',pathLength:'1','stroke-dasharray':'1 1'},proLine);
var lineF=svg('path',{fill:'none',stroke:'#e9cf8f','stroke-width':'2','stroke-dasharray':'6 8'},proLine);
$('proWatch').addEventListener('click',function(){ $('watch').click(); });
proEl.addEventListener('click',function(e){ var b=e.target.closest('button[data-act]'); if(!b) return;
  if(b.getAttribute('data-act')==='menu') setMenu(true); else { stop(); goto(0); } });
function inB(T,k){ var t=PRO.tl[k], n=t[1]-t[0]; return seg(T,t[0]+n*.04,t[0]+n*.22)*(1-seg(T,t[1]-n*.16,t[1]-n*.02)); }
var LED=PT.E1?[].slice.call(PT.E1.querySelectorAll('li')):[];
function renderPro(T){
  var tl=PRO.tl, end=tl.O6[1], n5=end-tl.O6[0], e0=tl.E0[0], epi=T>=e0-.6, inEp=0, out;
  if(!epi){ out=seg(T,tl.O6[0]+n5*.35,end);
    colEl.style.transform=out<1?'translateX('+((1-out)*-70).toFixed(1)+'px)':''; colEl.style.opacity=out<1?out.toFixed(3):'';
    if(T>=end){ proEl.style.visibility='hidden'; return; } }
  else { inEp=seg(T,e0-.6,e0+.2); out=1-inEp; colEl.style.transform=''; colEl.style.opacity=(1-inEp).toFixed(3); }
  proEl.style.visibility='visible'; proEl.style.opacity=(1-out).toFixed(3);
  proEl.classList.toggle('live',epi&&T>=tl.E2[0]);
  var W=proEl.clientWidth, H=proEl.clientHeight, ph=phone, n3=tl.O3[1]-tl.O3[0];
  // the paintings: pushing in through the prologue, easing back out through the epilogue
  var push=epi?1.12-.08*seg(T,e0,tl.E2[1]):1.02+.10*seg(T,0,tl.O6[0]);
  heroA.style.transform=heroB.style.transform='scale('+push.toFixed(4)+')';
  heroB.style.opacity=(epi?1:seg(T,tl.O3[0]+n3*.3,tl.O3[0]+n3*.7)).toFixed(3);
  scrim.style.opacity=(epi?.88:lerp(.18,.66,seg(T,tl.O0[1]-.5,tl.O1[0]+.3))).toFixed(3);
  // the panels and the ledger need an even ground, not the painting's bright corner
  $('scrim2').style.opacity=(epi?.64*seg(T,e0-.2,e0+.3):0).toFixed(3);
  // the words
  Object.keys(PT).forEach(function(k){ var o;
    if(k==='O0') o=1-seg(T,tl.O0[1]-.5,tl.O0[1]-.1);
    else if(k==='E2'){ var t=tl.E2, n=t[1]-t[0]; o=seg(T,t[0]+n*.04,t[0]+n*.22); }
    else o=inB(T,k);
    vis(PT[k],o); PT[k].style.transform='translateY('+((1-o)*16).toFixed(1)+'px)'; });
  // the ledger writes itself, one line at a time
  var n1=tl.E1[1]-tl.E1[0];
  LED.forEach(function(li,i){ var a=tl.E1[0]+n1*.14+i*n1*.038; li.style.opacity=seg(T,a,a+.18).toFixed(3); });
  // the line of two thousand years, and the dashed five hundred more
  var t1=tl.O1, l=seg(T,t1[0]+.25,t1[0]+1.35), lo=epi?0:inB(T,'O1');
  var y=H*(ph?.86:.80), x0=W*.10, x1=W*.90, xn=lerp(x0,x1,.78);
  lineP.setAttribute('d','M'+x0.toFixed(1)+' '+y.toFixed(1)+' L'+xn.toFixed(1)+' '+y.toFixed(1));
  lineP.setAttribute('stroke-dashoffset',(1-seg(l,0,.8)).toFixed(4));
  lineF.setAttribute('d','M'+xn.toFixed(1)+' '+y.toFixed(1)+' L'+x1.toFixed(1)+' '+y.toFixed(1)); lineF.style.opacity=seg(l,.8,1).toFixed(3);
  proLine.style.opacity=lo.toFixed(3);
  stEls.forEach(function(e,i){ var px=lerp(x0,x1,[0,.26,.52,.78,1][i]); e.style.left=px.toFixed(1)+'px'; e.style.top=(y+12).toFixed(1)+'px';
    vis(e,seg(l,i*.19,i*.19+.12)*lo); });
  // the thirteen things: they come in, they turn into 2526, they leave for the walks
  var t2=tl.O2, n2=t2[1]-t2[0], leave=epi?1:seg(T,tl.O6[0],tl.O6[0]+.35), rows=ph?3:2, per=Math.ceil(PO.length/rows);
  var ytop=H*(ph?.47:.44), ybot=H*(ph?.85:.93), hh=Math.min((ybot-ytop)/rows*.86, W/(per+1.2)/1.05);
  PO.forEach(function(p,i){
    var r=Math.floor(i/per), k=i-r*per, cnt=Math.min(per,PO.length-r*per);
    var e=seg(T,t2[0]+n2*.18+i*.06,t2[0]+n2*.18+i*.06+.35)*(1-leave);
    if(e<=.001){ p.w.style.visibility='hidden'; return; }
    var u=ease(seg(T,tl.O3[0]+n3*.28+i*.07,tl.O3[0]+n3*.28+i*.07+.3));
    var ar=Math.max(p.o.ar,p.o.br), w=hh*ar, cx=W*(k+1)/(cnt+1)+(r%2?W/(cnt+1)*.25:0), by=ytop+(r+1)*(ybot-ytop)/rows;
    var bob=Math.sin(T*2.6+i*1.7)*4*e;
    p.w.style.visibility='visible'; p.w.style.width=w.toFixed(1)+'px'; p.w.style.height=hh.toFixed(1)+'px';
    p.w.style.transform='translate('+(cx-w/2).toFixed(1)+'px,'+(by-hh+(1-ease(e))*40+bob).toFixed(1)+'px)';
    p.w.style.opacity=ease(e).toFixed(3); p.a.style.opacity=(1-u).toFixed(3); p.b.style.opacity=u.toFixed(3);
  });
  // the year runs while the things turn
  var yr=seg(T,tl.O3[0]+n3*.25,tl.O3[0]+n3*.85); vis(proYear,epi?0:inB(T,'O3')); proYear.textContent=String(Math.round(2026+500*ease(yr)));
}

/* ---------- the 2526 stage: the year runs forward, the room cools, a window opens on the imagined world ---------- */
var yearEl=$('year'), yearN=yearEl.querySelector('.yn'), sceneEl=$('scene'), wallEl=$('wall'), floorEl=$('floor');
function hx(c){ return [parseInt(c.substr(1,2),16),parseInt(c.substr(3,2),16),parseInt(c.substr(5,2),16)]; }
function mix(a,b,t){ var A=hx(a),B=hx(b); return 'rgb('+[0,1,2].map(function(i){return Math.round(lerp(A[i],B[i],t));}).join(',')+')'; }
function renderFuture(T,W,H){
  var f=0, yr=0, wn=0, ck=-1;
  D.chapters.forEach(function(c,k){ var u=c.fut; if(T>=u.yr[0]&&T<=u.out[1]){ ck=k; var o=1-seg(T,u.out[0],u.out[1]);
    f=ease(seg(T,u.yr[0],u.yr[1]))*o; yr=seg(T,u.yr[0],u.yr[1]); wn=(c.scene?seg(T,u.win[0],u.win[1]):0)*o; } });
  wallEl.style.background=f>0?mix(D.pal.wall,D.pal.fwall,f):'';
  floorEl.style.background=f>0?mix(D.pal.floor,D.pal.ffloor,f):'';
  vis(yearEl,f); if(f>0) yearN.textContent=String(Math.round(2026+500*ease(yr)));
  if(wn>0){ var c=D.chapters[ck]; if(sceneEl.getAttribute('src')!==c.scene) sceneEl.setAttribute('src',c.scene);
    var d=Math.min(W*(phone?.94:.80), L.fy*.92), cx=W*D.slots.C;
    sceneEl.style.width=sceneEl.style.height=d.toFixed(1)+'px';
    sceneEl.style.transform='translate('+(cx-d/2).toFixed(1)+'px,'+(L.fy-d*.97).toFixed(1)+'px) scale('+(0.94+0.06*ease(wn)).toFixed(4)+')';
    vis(sceneEl,ease(wn)*.96); }
  else vis(sceneEl,0);
}
var ovKey='';
function hideOverlaps(els,more){
  var k=L.W+'x'+L.H+':'+els[0].getAttribute('font-size')+':'+gsvg.getAttribute('viewBox'); if(k===ovKey) return; ovKey=k;
  var boxes=[], s=stage.getBoundingClientRect();
  els=els.concat(more||[]);
  els.forEach(function(t){ t.style.display=''; });
  els.forEach(function(t){
    var r=t.getBoundingClientRect(), hit=false;
    if(r.left<s.left+4||r.right>s.right-4||r.top<s.top+4||r.bottom>s.bottom-4) hit=true;
    boxes.forEach(function(b){ if(!(r.right<b.left-6||r.left>b.right+6||r.bottom<b.top-2||r.top>b.bottom+2)) hit=true; });
    if(hit) t.style.display='none'; else boxes.push(r);
  });
}
var byId={}; D.beats.forEach(function(b,i){byId[b.id]=b; b._i=i;});
cards.forEach(function(c){ c._b=byId[c.getAttribute('data-beat')]; });

/* ---------- header: the chapter in view ---------- */
var h1=$('h1'), chn=$('chn'), H1=h1.innerHTML;
function header(bt){
  var c=bt.ch!=null?D.chapters[bt.ch]:null;
  if(c){ h1.innerHTML='<span lang="ta"></span> · '; h1.firstChild.textContent=c.ta; h1.appendChild(document.createTextNode(c.sub)); chn.textContent=(bt.ch+1)+' / '+D.chapters.length; document.documentElement.style.setProperty('--acc',c.acc); }
  else { h1.innerHTML=H1; chn.textContent=''; document.documentElement.style.removeProperty('--acc'); }
}

/* ---------- menu, sheet, keys ---------- */
var menu=$('menu'), mb=$('menuB');
function setMenu(on){ menu.hidden=!on; mb.setAttribute('aria-expanded',String(on)); if(on){ var b=menu.querySelector('button'); if(b) b.focus(); } }
mb.addEventListener('click',function(){ setMenu(menu.hidden); });
menu.addEventListener('click',function(e){ var b=e.target.closest('button[data-ch]'); if(!b) return; var c=D.chapters[+b.getAttribute('data-ch')];
  setMenu(false); stop(); goto(c.g.route[1]+.05); });
var sheet=$('sheet'), sheetIn=$('sheetIn');
cards.forEach(function(c){ var b=c.querySelector('.more'); if(!b) return; b.addEventListener('click',function(){
  var k=c.cloneNode(true); k.removeAttribute('style'); k.className='sheetcard'; var rd=k.querySelector('.rd'); if(rd){ rd.className='rd'; rd.style.cssText=''; } var mm=k.querySelector('.more'); if(mm) mm.remove(); [].forEach.call(k.querySelectorAll('.lab,.cite'),function(e){ e.style.display=''; });
  sheetIn.innerHTML=''; sheetIn.appendChild(k); sheet.hidden=false; $('sheetX').focus(); stop(); }); });
$('sheetX').addEventListener('click',function(){ sheet.hidden=true; });
cardsEl.addEventListener('click',function(e){ var b=e.target.closest('button[data-act]'); if(!b) return;
  if(b.getAttribute('data-act')==='menu') setMenu(true); else { stop(); goto(0); } });
function settleT(b){ return b.start+Math.min(.98,b.settle+.12)*b.len; }
addEventListener('keydown',function(e){
  if(e.key==='Escape'){ if(!sheet.hidden){ sheet.hidden=true; return; } if(!menu.hidden){ setMenu(false); mb.focus(); return; } }
  if(e.altKey||e.ctrlKey||e.metaKey||!sheet.hidden||!menu.hidden) return;
  if(e.target&&(e.target.tagName==='BUTTON')&&(e.key===' '||e.key==='Enter')) return;
  var dir=0, k=e.key;
  if(k==='ArrowDown'||k==='ArrowRight'||k==='PageDown'||(k===' '&&!e.shiftKey)) dir=1;
  else if(k==='ArrowUp'||k==='ArrowLeft'||k==='PageUp'||(k===' '&&e.shiftKey)) dir=-1;
  if(!dir) return;
  e.preventDefault(); stop();
  var T=curT(), i=D.beats.indexOf(beatAt(T)), b=D.beats[i];
  if(dir>0){ if(T<settleT(b)-.02) goto(settleT(b)); else if(i<D.beats.length-1) goto(settleT(D.beats[i+1])); }
  else { if(i>0) goto(settleT(D.beats[i-1])); else goto(0); }
});

/* ---------- scroll + watch ---------- */
function curT(){ return clamp(scrollY/unit(),0,D.total-1e-4); }
function goto(T){ scrollTo(0,T*unit()); render(T,true); }
var raf=0;
function onScroll(){ if(!raf) raf=requestAnimationFrame(function(){ raf=0; render(curT()); }); }
addEventListener('scroll',onScroll,{passive:true});
var rt; addEventListener('resize',function(){ clearTimeout(rt); rt=setTimeout(layout,60); });
var watching=false, lastTs=0, SPEED=1/3.8;   // units per second
var wb=$('watch');
function step(ts){
  if(!watching) return;
  var dt=lastTs?Math.min(.05,(ts-lastTs)/1000):0; lastTs=ts;
  var T=curT();
  if(RM){
    step.hold=(step.hold||0)+dt;
    if(step.hold>5){ step.hold=0; var b=beatAt(T), i=D.beats.indexOf(b); if(i<D.beats.length-1){ scrollTo(0,(D.beats[i+1].start+.001)*unit()); } else stop(); }
  } else {
    T+=dt*SPEED; if(T>=D.total-1e-3){ T=D.total-1e-3; stop(); }
    scrollTo(0,T*unit());
  }
  requestAnimationFrame(step);
}
function stop(){ watching=false; wb.setAttribute('aria-pressed','false'); wb.textContent='Watch'; }
wb.addEventListener('click',function(){
  watching=!watching; wb.setAttribute('aria-pressed',String(watching)); wb.textContent=watching?'Pause':'Watch';
  if(watching){ if(curT()>=D.total-.01) scrollTo(0,0); lastTs=0; requestAnimationFrame(step); }
});
['wheel','touchstart'].forEach(function(ev){ addEventListener(ev,function(){ if(watching) stop(); },{passive:true}); });

window.__v4={D:D, unit:unit, layout:layout, render:render, T:curT, goto:goto};
if(document.fonts&&document.fonts.ready) document.fonts.ready.then(layout);
layout();
if(/[?&]watch=1\b/.test(Q)) wb.click();
var tq=Q.match(/[?&]t=([\d.]+)/); if(tq){ var TT=+tq[1]; var go=function(){ layout(); goto(TT); }; go(); setTimeout(go,300); if(document.fonts) document.fonts.ready.then(go); }
})();
