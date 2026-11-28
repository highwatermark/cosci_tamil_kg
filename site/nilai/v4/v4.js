/* Nilai v4 prototype. One fixed grid (text column | stage), a scroll timeline T in units of one viewport.
   Every visual state is a pure function of T, so scrubbing is reversible; watch mode scrolls at a steady rate;
   reduced motion snaps each beat to its settled state. */
(function(){
"use strict";
var D=JSON.parse(document.getElementById('data').textContent);
var Q=location.search;
var RM=(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)||/[?&]motion=reduce\b/.test(Q);
var $=function(id){return document.getElementById(id);};
var app=$('app'), stage=$('stage'), objs=$('objs'), shadows=$('shadows'), caps=$('caps'), thr=$('threads'), teach=$('teach'), gsvg=$('graph'), spacer=$('spacer');
var cards=[].slice.call(document.querySelectorAll('.card'));
var NS='http://www.w3.org/2000/svg';
function clamp(v,a,b){return v<a?a:v>b?b:v;}
function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;}
function seg(T,a,b){return b<=a?(T>=b?1:0):clamp((T-a)/(b-a),0,1);}
function lerp(a,b,t){return a+(b-a)*t;}

/* ---------- sprites ---------- */
var EL={}, SH={}, CP={};
var ORDER=['hands','stone','pillar','shrine','speaker'];
ORDER.forEach(function(id){
  var s=D.sprites[id]; if(!s) return;
  var im=new Image(); im.src=s.src; im.alt=''; im.className='obj'; im.decoding='async'; im.draggable=false;
  objs.appendChild(im); EL[id]=im;
  var sh=document.createElement('div'); sh.className='sh'; shadows.appendChild(sh); SH[id]=sh;
  if(D.captions[id]){ var c=document.createElement('div'); c.className='cap'+(/imagined/.test(D.captions[id])?' imag':''); c.textContent=D.captions[id]; caps.appendChild(c); CP[id]=c; }
});
function track(id,T){
  var k=D.tracks[id]; if(!k) return null;
  if(T<=k[0][0]) return {x:k[0][1],s:k[0][2],r:k[0][3]};
  for(var i=1;i<k.length;i++){ if(T<=k[i][0]){ var a=k[i-1], b=k[i], u=ease(seg(T,a[0],b[0])); return {x:lerp(a[1],b[1],u),s:lerp(a[2],b[2],u),r:lerp(a[3],b[3],u)}; } }
  var z=k[k.length-1]; return {x:z[1],s:z[2],r:z[3]};
}

/* ---------- threads ---------- */
var TH={};
D.threads.forEach(function(t){
  var rc=null; var p=document.createElementNS(NS,'path'); p.setAttribute('fill','none'); p.setAttribute('stroke','var(--thread)'); p.setAttribute('stroke-width','2.2'); p.setAttribute('stroke-linecap','round'); p.setAttribute('pathLength','1'); p.setAttribute('stroke-dasharray','1 1');
  var a=document.createElementNS(NS,'circle'), b=document.createElementNS(NS,'circle'); [a,b].forEach(function(c){c.setAttribute('r','4.5'); c.setAttribute('fill','var(--thread)');});
  if(t.dash){ var cp=document.createElementNS(NS,'clipPath'); cp.id='clip-'+t.id; var rc=document.createElementNS(NS,'rect'); cp.appendChild(rc); thr.appendChild(cp);
    p.removeAttribute('pathLength'); p.setAttribute('stroke-dasharray','7 7'); p.setAttribute('stroke-width','1.8'); p.setAttribute('clip-path','url(#clip-'+t.id+')'); }
  thr.appendChild(p); thr.appendChild(a); thr.appendChild(b);
  TH[t.id]={t:t,p:p,a:a,b:b,rc:rc};
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

/* ---------- graph ---------- */
var GD=document.createElementNS(NS,'g'), GE=document.createElementNS(NS,'g'), GR=document.createElementNS(NS,'g'), GL=document.createElementNS(NS,'g'), GS=document.createElementNS(NS,'g');
gsvg.appendChild(GE); gsvg.appendChild(GD); gsvg.appendChild(GR); gsvg.appendChild(GS); gsvg.appendChild(GL);
var maxc=1; D.edges.forEach(function(e){ if(e[4]>maxc) maxc=e[4]; });
var edgeEls=D.edges.map(function(e){
  var p=document.createElementNS(NS,'path'), mx=(e[0]+e[2])/2, my=(e[1]+e[3])/2, cx=lerp(mx,500,.55), cy=lerp(my,500,.55);
  p.setAttribute('d','M'+e[0]+' '+e[1]+' Q'+cx.toFixed(1)+' '+cy.toFixed(1)+' '+e[2]+' '+e[3]);
  p.setAttribute('fill','none'); p.setAttribute('stroke','var(--thread)');
  var w=Math.log(1+e[4])/Math.log(1+maxc);
  p.setAttribute('stroke-width',(0.5+1.6*w).toFixed(2)); p.setAttribute('stroke-opacity',(0.10+0.38*w).toFixed(3));
  GE.appendChild(p); return p;
});
var NG=9, groupEls=[];
for(var gi=0;gi<NG;gi++){ var g=document.createElementNS(NS,'g'); GD.appendChild(g); groupEls.push(g); }
D.dots.forEach(function(d){ var c=document.createElementNS(NS,'circle'); c.setAttribute('cx',d[0]); c.setAttribute('cy',d[1]); c.setAttribute('r','2.6'); c.setAttribute('fill','var(--ink2)'); groupEls[d[2]].appendChild(c); });
var labEls=D.labels.map(function(l){ var t=document.createElementNS(NS,'text'); t.setAttribute('class','gl'); t.setAttribute('x',l.x); t.setAttribute('y',l.y); t.setAttribute('text-anchor',l.anchor); t.setAttribute('dominant-baseline','middle'); t.textContent=l.t; GL.appendChild(t); return t; });
var SP=D.special;
var routeEls=D.route.map(function(r){
  var a=SP[r[0]], b=SP[r[1]], mx=(a[0]+b[0])/2, my=(a[1]+b[1])/2, cx=lerp(mx,500,.55), cy=lerp(my,500,.55);
  var p=document.createElementNS(NS,'path'); p.setAttribute('d','M'+a[0]+' '+a[1]+' Q'+cx+' '+cy+' '+b[0]+' '+b[1]);
  p.setAttribute('fill','none'); p.setAttribute('stroke','var(--thread)'); p.setAttribute('stroke-linecap','round'); p.setAttribute('pathLength','1'); p.setAttribute('stroke-dasharray','1 1');
  GR.appendChild(p); return p;
});
var spEls={}, spLab={};
Object.keys(SP).forEach(function(id){
  var c=document.createElementNS(NS,'circle'); c.setAttribute('cx',SP[id][0]); c.setAttribute('cy',SP[id][1]); c.setAttribute('fill','var(--thread)'); c.setAttribute('stroke','var(--ink)'); GS.appendChild(c); spEls[id]=c;
  var t=document.createElementNS(NS,'text'); t.setAttribute('class','rl'); t.textContent=id; GS.appendChild(t); spLab[id]=t;
});

/* ---------- layout ---------- */
var L={}, phone=false;
function layout(){
  phone=matchMedia('(max-width:700px),(max-aspect-ratio:9/10)').matches;
  if(phone){
    // the text band fits its tallest card
    var col=$('col'), hd=$('hd'), cw=col.clientWidth-32, mx=0;
    cards.forEach(function(c){ c.style.position='static'; c.style.visibility='hidden'; c.style.display='block'; c.style.width=cw+'px'; });
    var probe=document.createElement('div'); probe.style.cssText='position:absolute;left:-9999px;top:0;width:'+cw+'px'; document.body.appendChild(probe);
    cards.forEach(function(c){ var k=c.cloneNode(true); k.style.cssText='position:static;display:block;visibility:hidden;opacity:1;padding-top:8px'; probe.appendChild(k); mx=Math.max(mx,k.offsetHeight); probe.removeChild(k); });
    document.body.removeChild(probe);
    cards.forEach(function(c){ c.style.position=''; c.style.display=''; c.style.width=''; c.style.visibility=''; });
    var band=Math.min(Math.ceil(hd.offsetHeight+mx+22), Math.round(innerHeight*.62));
    document.documentElement.style.setProperty('--band',band+'px');
  }
  var W=stage.clientWidth, H=stage.clientHeight;
  L.W=W; L.H=H;
  L.fy=Math.round(H*(phone?.84:.8));
  document.documentElement.style.setProperty('--fy',L.fy+'px');
  // teaching text block at the top of the stage: measure the taller of the two
  L.tx=Math.round(W*(phone?.05:.08)); L.tw=Math.round(W*(phone?.9:.84)); L.ty=Math.round(H*(phone?.035:.06));
  teach.style.left=L.tx+'px'; teach.style.top=L.ty+'px'; teach.style.width=L.tw+'px';
  var th=0; Object.keys(TE).forEach(function(id){ var e=TE[id].el; e.style.display='block'; th=Math.max(th,e.offsetHeight); e.style.display='none'; });
  L.apex=L.ty+th+Math.round(H*.035);
  var S=D.slots.S;
  var hmax=Math.min(H*(phone?.56:.58), (L.fy-L.apex-H*.05)/S);
  // widths: centre hero within 46% of the stage, side heroes within 44%
  var hero=hmax;
  Object.keys(D.sprites).forEach(function(id){ var s=D.sprites[id], a=s.w/s.h, side=(id==='stone'||id==='pillar'||id==='shrine');
    hero=Math.min(hero, (W*(id==='hands'?.86:.6))/(a*s.k)); if(side) hero=Math.min(hero,(W*.42)/(a*s.k*S)); });
  L.hero=Math.max(60,Math.floor(hero));
  Object.keys(EL).forEach(function(id){ var s=D.sprites[id], h=L.hero*s.k, w=h*s.w/s.h; EL[id].style.height=h+'px'; EL[id].style.width=w+'px'; EL[id]._w=w; EL[id]._h=h; });
  thr.setAttribute('viewBox','0 0 '+W+' '+H);
  spacer.style.height=(D.total*unit()+innerHeight)+'px';
  render(curT(),true);
}
function unit(){ return innerHeight; }

/* ---------- render ---------- */
function vis(el,o){ el.style.opacity=o.toFixed(3); el.style.visibility=o>0.001?'visible':'hidden'; }
function beatAt(T){ for(var i=0;i<D.beats.length;i++){ var b=D.beats[i]; if(T<b.start+b.len) return b; } return D.beats[D.beats.length-1]; }
var lastKey='';
function render(T,force){
  if(RM){ var bb=beatAt(T); T=bb.start+bb.len-1e-4; }
  var key=T.toFixed(4); if(key===lastKey&&!force) return; lastKey=key;
  var W=L.W, H=L.H;
  var objState={};
  // objects
  Object.keys(EL).forEach(function(id){
    var st=track(id,T), el=EL[id];
    if(!st||st.r<=0.0005){ el.style.visibility='hidden'; vis(SH[id],0); if(CP[id]) vis(CP[id],0); objState[id]=null; return; }
    var w=el._w, h=el._h, cx=st.x*W, sink=(1-st.r)*(h*st.s+12);
    el.style.visibility='visible';
    el.style.transform='translate('+(cx-w/2).toFixed(1)+'px,'+sink.toFixed(1)+'px) scale('+st.s.toFixed(4)+')';
    var sh=SH[id]; sh.style.left=(cx-w*st.s*.47).toFixed(1)+'px'; sh.style.width=(w*st.s*.94).toFixed(1)+'px'; vis(sh,Math.pow(st.r,3));
    if(CP[id]){ var c=CP[id]; c.style.left=cx.toFixed(1)+'px'; vis(c,seg(st.r,.94,1)); }
    objState[id]={cx:cx, top:L.fy-h*st.s+sink, r:st.r, s:st.s};
  });
  // hands are only ever shown with the speaker, so the speaker caption covers both
  // threads
  D.threads.forEach(function(t){
    var o=TH[t.id], a=objState[t.a], b=objState[t.b];
    var draw=seg(T,t.d0,t.d1), fade=1-seg(T,t.f0,t.f1);
    if(!a||!b||draw<=0||fade<=0||a.r<.99||b.r<.99){ [o.p,o.a,o.b].forEach(function(e){e.style.opacity=0;}); }
    else{
      var x1=a.cx, y1=a.top-10, x2=b.cx, y2=b.top-10, ap=Math.min(L.apex, Math.min(y1,y2)-24);
      o.p.setAttribute('d','M'+x1.toFixed(1)+' '+y1.toFixed(1)+' C'+x1.toFixed(1)+' '+ap.toFixed(1)+' '+x2.toFixed(1)+' '+ap.toFixed(1)+' '+x2.toFixed(1)+' '+y2.toFixed(1));
      if(o.rc){ var ex=Math.min(x1,x2)-12, ew=Math.abs(x2-x1)*ease(draw)+12; o.rc.setAttribute('x',ex); o.rc.setAttribute('y',0); o.rc.setAttribute('width',ew); o.rc.setAttribute('height',H); }
      else o.p.setAttribute('stroke-dashoffset',(1-ease(draw)).toFixed(4));
      o.p.style.opacity=fade; o.a.setAttribute('cx',x1); o.a.setAttribute('cy',y1); o.a.style.opacity=fade;
      o.b.setAttribute('cx',x2); o.b.setAttribute('cy',y2); o.b.style.opacity=fade*seg(draw,.96,1);
    }
    var te=TE[t.id];
    if(!te) return;
    if(draw>0&&fade>0){
      te.el.style.display='block';
      var n=te.w.length, pr=draw*(n+2);
      te.w.forEach(function(s,i){ s.style.opacity=clamp(pr-i,0,1).toFixed(2); });
      te.el.style.opacity=fade;
    } else te.el.style.display='none';
  });
  teach.style.opacity=1;
  // graph
  var G=D.graph, go;
  var gin=seg(T,G.dots[0],G.dots[1]), gout=seg(T,G.out[0],G.out[1]), gback=seg(T,G.back[0],G.back[1]);
  go=T<G.back[0]?(gin>0?1-gout:0):gback;
  vis(gsvg,go);
  $('floor').style.opacity=(1-seg(go,0,.4)).toFixed(3);
  if(go>0){
    groupEls.forEach(function(g){ g.style.opacity=1; });
    var ein=seg(T,G.edges[0],G.edges[1]);
    GE.style.opacity=(T<G.back[0]?ease(ein):.55).toFixed(3);
    // camera: full view -> close on siddhar:1458, and back out at the close
    var zin=ease(seg(T,G.zoom[0],G.zoom[1])), zout=ease(seg(T,G.unzoom[0],G.unzoom[1]));
    var z=T<G.back[0]?zin:1-zout;
    var f=SP['siddhar:1458'], asp=W/H, fw=1000, fh=1000;
    if(asp>1) fw=1000*asp; else fh=1000/asp;
    var cw=lerp(fw,fw*.28,z), chh=lerp(fh,fh*.28,z), ccx=lerp(500,f[0],z), ccy=lerp(500,f[1],z);
    gsvg.setAttribute('viewBox',(ccx-cw/2).toFixed(1)+' '+(ccy-chh/2).toFixed(1)+' '+cw.toFixed(1)+' '+chh.toFixed(1));
    var ppu=W/cw;   // pixels per unit
    var fs=(13/ppu);
    var routeP=seg(T,G.route[0],G.route[1]);
    labEls.forEach(function(t,i){ var l=D.labels[i], rr=l.r+fs*.9*Math.abs(Math.sin(l.a))+fs*.3; t.setAttribute('x',(500+rr*Math.cos(l.a)).toFixed(1)); t.setAttribute('y',(500+rr*Math.sin(l.a)).toFixed(1)); t.setAttribute('font-size',fs.toFixed(2)); t.style.opacity=((1-z)*(1-routeP)).toFixed(3); });
    hideOverlaps(labEls);
    // dimming others while zoomed
    GD.style.opacity=(1-.72*Math.max(z,seg(T,G.route[0],G.route[1]))).toFixed(3);
    // special dots
    var route=seg(T,G.route[0],G.route[1]);
    Object.keys(spEls).forEach(function(id){
      var on=(id==='siddhar:1458')?Math.max(zin*(T<G.back[0]?1:0),route):route;
      var c=spEls[id];
      c.setAttribute('r',(Math.max(2.6,(4+6*on)/ppu)).toFixed(2)); c.setAttribute('stroke-width',(1/ppu).toFixed(2)); c.style.opacity=on>0?1:0;
      var t=spLab[id]; t.setAttribute('font-size',fs.toFixed(2)); t.setAttribute('stroke-width',(5/ppu).toFixed(2));
      var dx=SP[id][0]<500?-1:1;
      t.setAttribute('x',(SP[id][0]+dx*12/ppu).toFixed(1)); t.setAttribute('y',(SP[id][1]+(id==='civaka_cintamani:2058'?16:id==='manimekalai:21:112-129'?-16:0)/ppu).toFixed(1));
      t.setAttribute('text-anchor',dx<0?'end':'start'); t.setAttribute('dominant-baseline','middle');
      t.style.opacity=on>.6?seg(on,.6,1):0;
    });
    routeEls.forEach(function(p){ p.setAttribute('stroke-width',(3.2/ppu).toFixed(2)); p.setAttribute('stroke-dashoffset',(1-ease(route)).toFixed(4)); p.style.opacity=route>0?1:0; });
    edgeEls.forEach(function(p){ p.setAttribute('vector-effect','non-scaling-stroke'); });
  }
  // cards: a card shows only once its beat has settled, and leaves as the next beat begins
  cards.forEach(function(c){
    var b=c._b; if(!b) return;
    var s0=b.start+b.settle*b.len, e0=b.start+b.len;
    var o=(b.settle===0&&b.start===0?1:seg(T,s0,s0+.08))*(1-seg(T,e0,e0+.08));
    vis(c,o);
  });
}
var ovKey='';
function hideOverlaps(els){
  var k=L.W+'x'+L.H+':'+els[0].getAttribute('font-size'); if(k===ovKey) return; ovKey=k;
  var boxes=[];
  els.forEach(function(t){ t.style.display=''; });
  els.forEach(function(t){
    var r=t.getBoundingClientRect(), s=stage.getBoundingClientRect(), hit=false;
    if(r.left<s.left+4||r.right>s.right-4||r.top<s.top+4||r.bottom>s.bottom-4) hit=true;
    boxes.forEach(function(b){ if(!(r.right<b.left-6||r.left>b.right+6||r.bottom<b.top-2||r.top>b.bottom+2)) hit=true; });
    if(hit) t.style.display='none'; else boxes.push(r);
  });
}
var byId={}; D.beats.forEach(function(b){byId[b.id]=b;});
cards.forEach(function(c){ c._b=byId[c.getAttribute('data-beat')]; });

/* ---------- scroll + watch ---------- */
function curT(){ return clamp(scrollY/unit(),0,D.total-1e-4); }
var raf=0;
function onScroll(){ if(!raf) raf=requestAnimationFrame(function(){ raf=0; render(curT()); }); }
addEventListener('scroll',onScroll,{passive:true});
var rt; addEventListener('resize',function(){ clearTimeout(rt); rt=setTimeout(layout,60); });
var watching=false, lastTs=0, SPEED=1/4.2;   // units per second
var wb=$('watch');
function step(ts){
  if(!watching) return;
  var dt=lastTs?Math.min(.05,(ts-lastTs)/1000):0; lastTs=ts;
  var T=curT();
  if(RM){
    // reduced motion: hold each settled beat, then jump to the next
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
['wheel','touchstart','keydown'].forEach(function(ev){ addEventListener(ev,function(e){ if(watching&&!(ev==='keydown'&&e.target===wb)) stop(); },{passive:true}); });

window.__v4={D:D, unit:unit, layout:layout, render:render, T:curT, goto:function(T){ scrollTo(0,T*unit()); render(T,true); }};
if(document.fonts&&document.fonts.ready) document.fonts.ready.then(layout);
layout();
if(/[?&]watch=1\b/.test(Q)) wb.click();
var tq=Q.match(/[?&]t=([\d.]+)/); if(tq){ var TT=+tq[1]; var go=function(){ layout(); window.__v4.goto(TT); }; go(); setTimeout(go,300); if(document.fonts) document.fonts.ready.then(go); }
})();
