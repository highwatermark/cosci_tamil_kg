/* the reel: tabs routed by location.hash, scroll-driven scenes (--e, --p, --q, --b), watch, keyboard stepping */
(function(){
"use strict";
var root=document.documentElement;
function $(id){ return document.getElementById(id); }
var reel=$('reel'), file=$('top'), wBtn=$('watchBtn'), wLbl=$('watchLbl'), headEl=$('reelHead');
if(!reel||!file) return;
var RM=(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)||/[?&]motion=reduce\b/.test(location.search);
if(RM) reel.classList.add('static');
var NS='http://www.w3.org/2000/svg';
function clamp(v){ return v<0?0:v>1?1:v; }

/* ponderings cards: open on wide screens, an accordion on phones */
(function(){ if(!window.matchMedia) return; var mq=window.matchMedia('(max-width:699px)');
  function set(){ [].forEach.call(document.querySelectorAll('.pd-card'),function(d){ d.open=!mq.matches; }); }
  set(); if(mq.addEventListener) mq.addEventListener('change',set); })();

/* kolam: dots, then a rule (a line bouncing between the walls of an m×n grid), then one unbroken line */
function buildKolam(g){
  var m=+g.getAttribute('data-m'), n=+g.getAttribute('data-n'), s=+g.getAttribute('data-s');
  var ox=-m*s, oy=-n*s, x=1, y=0, dx=1, dy=1, pts=[[x,y]], guard=0;
  do{ x+=dx; y+=dy; if(x<=0||x>=2*m) dx=-dx; if(y<=0||y>=2*n) dy=-dy; pts.push([x,y]); }
  while(!(x===1&&y===0&&dx===1&&dy===1) && ++guard<4000);
  function P(i){ var q=pts[i%(pts.length-1)]; return [ox+q[0]*s, oy+q[1]*s]; }
  function mid(a,b){ return [(a[0]+b[0])/2,(a[1]+b[1])/2]; }
  var N=pts.length-1, m0=mid(P(0),P(1)), d='M'+m0[0]+' '+m0[1];
  for(var k=1;k<=N;k++){ var c=P(k), e=mid(c,P(k+1)); d+='Q'+c[0]+' '+c[1]+' '+e[0]+' '+e[1]; }
  var tip=g.querySelector('.ktip');
  for(var i=0;i<m;i++) for(var j=0;j<n;j++){
    var dot=document.createElementNS(NS,'circle');
    dot.setAttribute('class','kd'+(i===0&&j===0?' pulli':'')); dot.setAttribute('cx',ox+(2*i+1)*s); dot.setAttribute('cy',oy+(2*j+1)*s); dot.setAttribute('r',(s*.17).toFixed(1));
    dot.style.setProperty('--d',((i+j)/Math.max(1,m+n-2)).toFixed(3)); g.insertBefore(dot,tip);
  }
  var path=document.createElementNS(NS,'path');
  path.setAttribute('class','kl'); path.setAttribute('d',d); path.setAttribute('pathLength','1'); path.setAttribute('stroke-width',(s*.2).toFixed(1));
  g.insertBefore(path,tip);
  if(tip){ g._tip=tip; g._path=path; g._ka=+g.getAttribute('data-ka'); g._kb=+g.getAttribute('data-kb'); tip.setAttribute('transform','translate('+m0[0]+' '+m0[1]+')'); }
}
[].forEach.call(reel.querySelectorAll('.kolam'), buildKolam);

/* scenes */
var S=[].map.call(reel.querySelectorAll('.rs'), function(sec){
  var list=sec.querySelector('.r-list');
  return { el:sec, stage:sec.querySelector('.r-stage'), words:[].slice.call(sec.querySelectorAll('.r-line .r-w')), cur:-1, v:{},
    h:sec.getAttribute('data-h')||'', q:+sec.getAttribute('data-q')||0, b:+sec.getAttribute('data-b')||0,
    cnt:[].slice.call(sec.querySelectorAll('.cnt')), tips:[].filter.call(sec.querySelectorAll('.kolam'),function(g){ return g._tip; }),
    list:list, lis:list?[].slice.call(list.children):[], hand:sec.querySelector('.r-hand') };
});
var arts=[].slice.call(reel.querySelectorAll('.r-art'));
function fit(){ arts.forEach(function(sv){ var r=sv.getBoundingClientRect(); if(!r.width) return; var vb=(r.width/Math.max(1,r.height))<1.5?'180 0 640 500':'0 0 1000 500'; if(sv.getAttribute('viewBox')!==vb) sv.setAttribute('viewBox',vb); }); }
function setv(s,k,v){ v=Math.round(v*1000)/1000; if(s.v[k]!==v){ s.v[k]=v; s.el.style.setProperty(k,v); } }
function mark(s,e){
  var n=s.words.length; if(!n) return;
  var k=e<=0?-1:Math.max(0,Math.min(n-1,Math.floor(e*1.4*n)));
  if(k!==s.cur){ if(s.cur>=0) s.words[s.cur].classList.remove('cur'); if(k>=0) s.words[k].classList.add('cur'); s.cur=k; }
}
function counters(s,p){
  s.cnt.forEach(function(c){
    var max=+c.getAttribute('data-count'), suf=c.getAttribute('data-suf')||'', v=Math.round(clamp(p*1.4)*max*(c.hasAttribute('data-clock')?60:1)), t;
    if(c.hasAttribute('data-clock')){ var mm=Math.floor(v/60), ss=v%60; t=(mm<10?'0':'')+mm+':'+(ss<10?'0':'')+ss; } else t=v+suf;
    if(c.textContent!==t) c.textContent=t;
  });
}
function listHand(s,p){
  var n=s.lis.length, per=0.72/n, hx=-200, hy=window.innerHeight, done=true;
  s.lis.forEach(function(li,j){
    var a=.08+j*per, v=clamp((p-a)/(per*.8));
    li.style.setProperty('--s',v.toFixed(3));
    if(v>0&&v<1&&done){ done=false; var rr=li.querySelector('.r-it').getClientRects(), r=rr[rr.length-1], sr=s.stage.getBoundingClientRect();
      hx=r.left-sr.left+r.width*v-6; hy=r.top-sr.top+r.height*.55+Math.sin(p*90)*3; }
  });
  if(done){ var last=s.lis[n-1].querySelector('.r-it').getBoundingClientRect(), sr2=s.stage.getBoundingClientRect(); var pv=clamp((p-.08)/.05);
    if(p<.08){ hx=sr2.width*.55; hy=sr2.height*(1.05-pv*.3); } else { hx=last.right-sr2.left+30; hy=last.bottom-sr2.top+20+(p-.8)*400; } }
  s.hand.style.setProperty('--hx',hx.toFixed(1)+'px'); s.hand.style.setProperty('--hy',hy.toFixed(1)+'px');
}
var curHead='';
function update(){
  ticking=false;
  if(tab!=='reel') return;
  var vh=window.innerHeight;
  if(RM){ var hh=S[0].h; S.forEach(function(s){ if(s.el.getBoundingClientRect().top<=vh*.5) hh=s.h; if(!s.done){ s.done=1; mark(s,1); counters(s,1); s.lis.forEach(function(li){ li.style.setProperty('--s',1); }); } });
    if(hh!==curHead){ curHead=hh; headEl.textContent=hh; } return; }
  var rs=S.map(function(s){ return s.el.getBoundingClientRect(); }), head=S[0].h;
  S.forEach(function(s,i){
    var r=rs[i], sh=s.stage.offsetHeight||vh;
    var e=clamp((vh-r.top)/vh), p=clamp(-r.top/Math.max(1,r.height-sh));
    if(r.top<=vh*.5) head=s.h;
    var near=r.bottom>-vh*.2 && r.top<vh*1.2;
    if(!near && s.parked) return;
    s.parked=!near;
    setv(s,'--e',e); setv(s,'--p',p);
    if(s.q) setv(s,'--q',Math.sin(p*Math.PI*2*s.q));
    if(s.b) setv(s,'--b',(1-Math.cos(p*Math.PI*2*s.b))/2);
    mark(s,e);
    if(!near) return;
    counters(s,p);
    s.tips.forEach(function(g){ var kl=clamp((p-g._ka)/g._kb), L=g._path.getTotalLength(), pt=g._path.getPointAtLength(L*kl); g._tip.setAttribute('transform','translate('+pt.x.toFixed(1)+' '+pt.y.toFixed(1)+')'); g._tip.style.opacity=(kl>0&&kl<1)?1:0; });
    if(s.list) listHand(s,p);
  });
  if(head!==curHead){ curHead=head; headEl.textContent=head; headEl.classList.remove('swap'); void headEl.offsetWidth; headEl.classList.add('swap'); }
}
var ticking=false;
function req(){ if(!ticking){ ticking=true; requestAnimationFrame(update); } }
window.addEventListener('scroll',req,{passive:true});
window.addEventListener('resize',function(){ fit(); S.forEach(function(s){ s.parked=false; }); req(); });

/* tabs, routed by location.hash: #reel (default) and #file; any id inside the file opens the file */
var tab=null, reelY=0, tabR=$('tabReel'), tabF=$('tabFile');
function jump(y){ var sb=root.style.scrollBehavior; root.style.scrollBehavior='auto'; void root.offsetHeight; try{ window.scrollTo({top:y,left:0,behavior:'instant'}); }catch(e){ window.scrollTo(0,y); } root.style.scrollBehavior=sb; }
function show(which, target){
  if(which==='reel'){
    if(tab!=='reel'){ file.hidden=true; reel.hidden=false; root.classList.add('reel-on'); var was=tab; tab='reel'; fit(); S.forEach(function(s){ s.parked=false; }); if(was==='file') jump(reelY); }
  } else {
    if(tab==='reel'){ reelY=window.scrollY; stop(); }
    var first=tab!=='file';
    reel.hidden=true; file.hidden=false; root.classList.remove('reel-on'); tab='file';
    if(first){ try{ window.dispatchEvent(new Event('resize')); }catch(e){} }
    if(target==='top'){ if(first) jump(0); }
    else if(target){ var t=$(target); if(t && first) t.scrollIntoView(); }
  }
  tabR.setAttribute('aria-current', tab==='reel'?'page':'false');
  tabF.setAttribute('aria-current', tab==='file'?'page':'false');
  var idx=$('idx'), ib=$('idxBtn'); if(idx&&!idx.hidden&&tab==='reel'){ idx.hidden=true; ib.setAttribute('aria-expanded','false'); }
  req();
}
function route(){
  var h=''; try{ h=decodeURIComponent(location.hash.slice(1)); }catch(e){ h=location.hash.slice(1); }
  if(!h||h==='reel') return show('reel');
  if(h==='file') return show('file','top');
  var t=$(h);
  if(t && file.contains(t)) return show('file',h);
  show('reel');
}
window.addEventListener('hashchange',route);
tabF.addEventListener('click',function(e){ if(location.hash==='#file'){ e.preventDefault(); show('file','top'); jump(0); } });
tabR.addEventListener('click',function(e){ if(location.hash==='#reel'){ e.preventDefault(); show('reel'); } });
var brand=document.querySelector('.bar .brand');
if(brand) brand.addEventListener('click',function(e){ if(tab==='reel'){ e.preventDefault(); stop(); jump(0); } });

/* watch: a steady auto-scroll (about 3.5 s per line) that pauses on any input */
var playing=false, started=false, raf=0, last=0, pos=0, rmTimer=0;
function label(){ wLbl.textContent=playing?'pause':(started?'resume':'watch'); wBtn.setAttribute('aria-pressed',playing?'true':'false'); }
function reelEnd(){ return reel.offsetTop+reel.offsetHeight-window.innerHeight; }
function frame(t){
  if(!playing) return;
  if(!last) last=t;
  var dt=Math.min(64,t-last)/1000; last=t;
  var end=reelEnd(), speed=Math.max(80,window.innerHeight/2.05);
  pos=Math.min(end,pos+speed*dt); window.scrollTo(0,pos);
  if(pos>=end-1){ playing=false; started=false; label(); return; }
  raf=requestAnimationFrame(frame);
}
function anchors(){ return S.map(function(s){ var sh=s.stage.offsetHeight||window.innerHeight; return s.el.offsetTop+(RM?0:(s.el.offsetHeight-sh)*(s.el.classList.contains('k-whatif')||s.list?.75:.55)); }); }
function rmTick(){ if(!playing) return; var a=anchors(), y=window.scrollY, i=0; while(i<a.length&&a[i]<=y+4) i++; if(i>=a.length){ playing=false; started=false; label(); return; } jump(a[i]); rmTimer=setTimeout(rmTick,7000); }
function play(){
  if(tab!=='reel') return;
  if(window.scrollY>=reelEnd()-2) jump(0);
  playing=true; started=true; label();
  if(RM){ rmTimer=setTimeout(rmTick,1200); return; }
  pos=window.scrollY; last=0; cancelAnimationFrame(raf); raf=requestAnimationFrame(frame);
}
function stop(){ if(!playing) return; playing=false; cancelAnimationFrame(raf); clearTimeout(rmTimer); label(); }
wBtn.addEventListener('click',function(){ if(playing) stop(); else play(); });
var again=$('watchAgain'); if(again) again.addEventListener('click',function(){ stop(); jump(0); started=false; play(); });
['wheel','touchstart'].forEach(function(ev){ window.addEventListener(ev,function(){ stop(); },{passive:true}); });
window.addEventListener('pointerdown',function(e){ if(!e.target.closest||(!e.target.closest('#watchBtn')&&!e.target.closest('#watchAgain'))) stop(); });

/* keyboard: Space and the arrow keys move scene by scene */
var anim=0;
function glide(y){
  cancelAnimationFrame(anim);
  if(RM){ jump(y); return; }
  var y0=window.scrollY, t0=0, dur=Math.min(1100,400+Math.abs(y-y0)*.2);
  function f(t){ if(!t0) t0=t; var k=Math.min(1,(t-t0)/dur), e=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2; window.scrollTo(0,y0+(y-y0)*e); if(k<1) anim=requestAnimationFrame(f); }
  anim=requestAnimationFrame(f);
}
document.addEventListener('keydown',function(e){
  if(tab!=='reel'||e.defaultPrevented||e.altKey||e.ctrlKey||e.metaKey) return;
  var t=e.target, tag=t&&t.tagName||'';
  if(t&&t.closest&&(t.closest('#watchBtn')||t.closest('#watchAgain'))) return;
  if(/^(INPUT|TEXTAREA|SELECT)$/.test(tag)||(t&&t.isContentEditable)) return;
  var k=e.key, dir=0;
  if(k==='ArrowDown'||k==='ArrowRight'||k==='PageDown'||(k===' '&&!e.shiftKey)) dir=1;
  else if(k==='ArrowUp'||k==='ArrowLeft'||k==='PageUp'||(k===' '&&e.shiftKey)) dir=-1;
  if(!dir){ if(k!=='Tab'&&k!=='Shift') stop(); return; }
  if(k===' '&&(tag==='BUTTON'||tag==='A'||tag==='SUMMARY')) return;
  e.preventDefault(); stop();
  var a=anchors(), y=window.scrollY, i;
  if(dir>0){ for(i=0;i<a.length&&a[i]<=y+8;i++); if(i<a.length) glide(a[i]); }
  else { for(i=a.length-1;i>=0&&a[i]>=y-8;i--); glide(i>=0?a[i]:0); }
});

route();
fit(); update();
label();
})();
