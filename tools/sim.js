// Balance simulator for Feedback Loop. Load it into the running game page (served over http):
//   await new Promise(r=>{const s=document.createElement('script');s.src='/tools/sim.js?'+Date.now();s.onload=r;document.body.appendChild(s)})
// then  __sims([{name:'fresh',skill:0.6}, {name:'rig4',skill:0.6,lv:{rig:4}}], 3)  starts the runs (3 seeds each) in the background;
// read  __simOut  (results so far) and  __simDone.  The player is the demo AI (see DEMO in index.html) on a fake clock, so a
// 10-minute show takes a few seconds. Nothing is saved: the demo copies the save in and puts it back.
(function(){
  const runOne=(cfg)=>new Promise(res=>{
    saveMeta=()=>{};saveSet=()=>{};
    const meta0=JSON.stringify(META);
    META=JSON.parse(JSON.stringify(META_DEF));Object.assign(META.own,{pad:1,ghost:1},cfg.own||{});Object.assign(META.lv,cfg.lv||{});
    META.earned=cfg.earned||0;META.band=cfg.band||'four';META.venue=cfg.venue||'basement';META.shows=cfg.shows||0;Object.assign(META.venues,cfg.venues||{});
    const set0=SET.devSet,all0=SET.allTiers;if(cfg.tier){SET.devSet=cfg.tier;SET.allTiers=true}applySound();
    const demoObj={real:!!cfg.ai,meta:meta0,skill:cfg.skill??0.6,lastB:-1,wait:0,head:Math.random()*6.283,want:null,frame:0,mx:null,my:null};DEMO=null;   // set after start(), so the show gets a real venue setlist (not the demo's theme set)
    const out={dash:0,dashOn:0,req:0,reqDone:0,reqHits:0,pus:0,drops:0,dropKills:0,dareOffers:0,dares:[],daresKept:0,cause:'',name:cfg.name,won:false,t:0,lvl:0,minHp:1,dir:[],judge:{PERFECT:0,GOOD:0,MISS:0},clipBars:0,hits:0,secs:0,maxHype:1};let ended=false;
    // telemetry: judgements, clipping bars, damage taken; a late or early headphone offset shifts every press (cfg.bias, s)
    const realJudge=judge;judge=function(r,...a){if(!a[1])out.judge[r]=(out.judge[r]||0)+1;return realJudge(r,...a)};
    const realHit=hit;if(cfg.bias)hit=function(h){return realHit(h===undefined?h:h+cfg.bias)};
    const realDmg=damagePlayer;damagePlayer=function(d){out.hits++;if(REQ&&REQ.inR)out.reqHits++;return realDmg(d)};
    // telemetry: level-ups in a row that offered no new instrument (while one was left), and which power-ups were picked up
    out.dry=0;out.pu={};let dry=0;
    const realOpen=openLevelUp;openLevelUp=function(){realOpen();const left=Object.keys(INST).some(id=>!trackOf(id)&&(!LOCKED_INST[id]||owns(id))&&instHere(id));
      if(choices.some(o=>o.k==='new')||!left)dry=0;else out.dry=Math.max(out.dry,++dry)};
    const realPU=applyPU;applyPU=function(id){out.pu[id]=(out.pu[id]||0)+1;return realPU(id)};
    const realEnd=endRun;endRun=function(won){out.kills=kills;out.cause=won?'':deathCause;out.daresKept=daresKept+(won&&DARE?1:0);out.reqDone=reqDone;out.pus=puGot;out.won=won;out.avgHype=+(hypeN?hypeAcc/hypeN:1).toFixed(2);out.clipEver=out.clipBars>0;out.t=Math.round(t);out.lvl=P.lvl;ended=true;endRun=realEnd;realEnd(won)};
    DIR_ON=cfg.dirOff?false:true;
    const realRoll=rollShow;if(cfg.twist)rollShow=function(l){realRoll(l);TWIST=cfg.twist==='none'?null:cfg.twist;if(cfg.twistBand)TWIST_BAND=cfg.twistBand};   // cfg.twist: force a show twist (or 'none')
    start();DEMO=demoObj;musicOn=false;
    // cfg.ai: how a playtester uses the new systems
    //   dash: chance per second to dash when 2+ noise are close · onBeat: chance the dash is timed on the beat
    //   req: 'always' | 'near' (under 380 px and HP over reqHp) | 'never' · drop: 'asap' | 'crowd' (12+ close) | 'never'
    //   dare: 'risky' (SWARM/LOUD first) | 'safe' (FAST/NO DASH first) | 'none'
    let lastReq=null,dropK0=0;
    const aiStep=ai=>{
      if(REQ&&REQ!==lastReq){lastReq=REQ;out.req++}
      if(dareOffer&&!out._offered){out._offered=dareOffer;out.dareOffers++;
        if(ai.dare&&ai.dare!=='none'){const pref=ai.dare==='risky'?['swarm','loud','fast','nodash']:['fast','nodash','loud','swarm'];const k=pref.find(x=>dareOffer.includes(x));out.dares.push(k);takeDare(k)}}
      if(!dareOffer)out._offered=null;
      // requests: head for the ring, then keep moving inside it (standing still builds feedback)
      if(REQ&&ai.req!=='never'){const dx=REQ.x-P.x,dy=REQ.y-P.y,d=Math.hypot(dx,dy)||1;
        const go=ai.req==='always'||(d<380&&P.hp>P.maxHp*(ai.reqHp??0.5))||REQ.inR;
        if(go){let vx,vy;if(d>REQ_R*0.55){vx=dx/d;vy=dy/d}else{vx=-dy/d;vy=dx/d}
          let fx=0,fy=0;for(const e of enemies){if(e.dead)continue;const ex=P.x-e.x,ey=P.y-e.y,d2=ex*ex+ey*ey+1;if(d2<120*120){fx+=ex/d2*60;fy+=ey/d2*60}}
          const m=Math.hypot(vx+fx,vy+fy)||1;joy.on=true;joy.ox=0;joy.oy=0;joy.x=(vx+fx)/m*60;joy.y=(vy+fy)/m*60}}
      // dash: out of trouble when crowded
      if(ai.dash&&feat('dash')&&dashCd<=0&&!P.dash){let close=0,ex=0,ey=0;for(const e of enemies){if(e.dead)continue;const dx=P.x-e.x,dy=P.y-e.y,d=Math.hypot(dx,dy);if(d<95){close++;ex+=dx/(d||1);ey+=dy/(d||1)}}
        if(close>=2&&Math.random()<ai.dash/40){const m=Math.hypot(ex,ey)||1;joy.on=true;joy.ox=0;joy.oy=0;joy.x=ex/m*60;joy.y=ey/m*60;
          const now=AU.now()-AU.lat();let nb=now;for(const b of beatTimes)if(Math.abs(b-now)<Math.abs(nb-now)||nb===now)nb=b;
          const heard=Math.random()<(ai.onBeat??0.5)?nb+gauss()*0.02:now+0.18;dash(heard);if(P.dash){out.dash++;if(P.dash.on)out.dashOn++}}}
      // the drop
      if(ai.drop&&ai.drop!=='never'&&dropReady()&&!revel()){let close=0;for(const e of enemies)if(!e.dead&&Math.hypot(e.x-P.x,e.y-P.y)<300)close++;
        if(ai.drop==='asap'||close>=12){dropGo();if(DROP.armed){out.drops++;dropK0=kills}}}
      if(DROP.on||DROP.armed)out.dropKills+=0;if(out._dropWas&&!DROP.on&&!DROP.armed)out.dropKills+=kills-dropK0;out._dropWas=DROP.on||DROP.armed;
    };
    let fake=AU.ctx?AU.ctx.currentTime:performance.now()/1000;const rn=AU.now;AU.now=()=>fake;
    const step=()=>{
      try{
        for(let f=0;f<1200&&!ended;f++){
          if(!DEMO){ended=true;break}
          fake+=1/40;demoStep(1/40);
          if(cfg.mover==='player'&&state==='play'&&P){   // a player-like mover: dodges what's close, otherwise goes for the nearest pickup (as the old balance bot did)
            let fx=0,fy=0;for(const e of enemies){if(e.dead)continue;const dx=P.x-e.x,dy=P.y-e.y,d2=dx*dx+dy*dy+1;if(d2<220*220){const w=(e.type==='boss'?4:1)/d2;fx+=dx*w;fy+=dy*w}}
            for(const b of ebullets){const dx=P.x-b.x,dy=P.y-b.y,d2=dx*dx+dy*dy+1;if(d2<120*120){fx+=dx*3/d2;fy+=dy*3/d2}}
            let n=null,nd=1e9;for(const q of gems){const d=Math.hypot(q.x-P.x,q.y-P.y)*(q.vac||q.pu?0.3:1);if(d<nd){nd=d;n=q}}
            const danger=Math.hypot(fx,fy);if(n&&nd<500){const w=Math.max(0.002,0.012-danger*0.5),dd=Math.hypot(n.x-P.x,n.y-P.y)||1;fx+=(n.x-P.x)/dd*w;fy+=(n.y-P.y)/dd*w}
            const m=Math.hypot(fx,fy)||1;joy.on=true;joy.ox=0;joy.oy=0;joy.x=fx/m*60;joy.y=fy/m*60}
          if(cfg.ai&&state==='play'&&P)aiStep(cfg.ai);
          if(cfg.twitch&&DEMO&&DEMO.want!=null){DEMO.head=DEMO.want;joy.x=Math.cos(DEMO.head)*60;joy.y=Math.sin(DEMO.head)*60}   // cfg.twitch: instant turning (a sharper dodger than the demo's smooth steering)
          if(state==='play'||state==='levelup'||state==='edit')pump();
          if(state==='play')update(1/40);
          if(P&&!out.bad&&(!isFinite(P.hp)||!isFinite(P.x)||!isFinite(P.y)||!isFinite(P.xp)||!isFinite(DIR)||P.maxHp<=0))out.bad=`t=${t.toFixed(1)} hp=${P.hp} x=${P.x} xp=${P.xp} dir=${DIR}`;   // a bug: state that should never happen
          if(P)out.minHp=Math.min(out.minHp,P.hp/P.maxHp);if(clipping&&HE&&HE.ib===0&&out._cb!==HE.t){out._cb=HE.t;out.clipBars++}out.maxHype=Math.max(out.maxHype,DIR);
          if(Math.floor(t)%30===0&&out.dir.length<Math.floor(t)/30+1)out.dir.push(+DIR.toFixed(2));
          if(t>=(cfg.maxT||900)){out.t=Math.round(t);out.lvl=P.lvl;out.timeout=true;ended=true;exitDemo();break}
        }
      }catch(e){out.err=e.stack.slice(0,300);ended=true;if(DEMO)exitDemo()}
      if(ended){AU.now=rn;endRun=realEnd;judge=realJudge;hit=realHit;damagePlayer=realDmg;openLevelUp=realOpen;applyPU=realPU;rollShow=realRoll;out.twist=TWIST;out.leans=Object.values(LEANS);DIR_ON=true;SET.devSet=set0;SET.allTiers=all0;applySound();out.minHp=+out.minHp.toFixed(2);out.secs=sectionsPlayed;out.tracks=tracks.map(x=>x.id+':'+placed(x));out.bands=[...new Set(tracks.map(x=>BAND_INST[x.id]))];out.maxHype=+out.maxHype.toFixed(2);res(out)}else setTimeout(step,0);
    };
    setTimeout(step,0);
  });
  window.__sims=async function(cfgs,seeds=3){
    window.__simOut=[];window.__simDone=false;
    for(const c of cfgs)for(let i=0;i<seeds;i++)__simOut.push(await runOne(c));
    window.__simDone=true;
  };
  window.__simTable=()=>{const g={};for(const r of __simOut){(g[r.name]=g[r.name]||[]).push(r)}
    return Object.entries(g).map(([n,rs])=>`${n}: won ${rs.filter(r=>r.won).length}/${rs.length} · t ${rs.map(r=>r.t).join(',')} · lvl ${rs.map(r=>r.lvl).join(',')} · minHp ${rs.map(r=>r.minHp).join(',')} · DIR max ${rs.map(r=>Math.max(...r.dir)).join(',')}${rs.some(r=>r.err)?' ERR '+rs.find(r=>r.err).err:''}`).join('\n')};
})();
