// 50 playtesters: varied skill, career stage, venue, band, sound, habits and twists (deterministic list)
let a=1;const R=()=>(a=(a*16807)%2147483647)/2147483647,P=x=>x[Math.floor(R()*x.length)];
const venues=['basement','basement','observatory','club','festival'],bands=['four','rhythm','synth','dream'],tiers=[null,null,'chip','fm16','rave','ambient','trance','vapor'];
const twists=[undefined,undefined,'mix','packed','roadie','glass','hot','none'];
const shows=[0,1,2,3,5,6,8,12,25,40],earned=[0,250,700,1600,4000,8000,20000];
const habits=[null,{dash:0.5,onBeat:0.3,req:'never',drop:'never',dare:'none'},{dash:1,onBeat:0.5,req:'near',drop:'crowd',dare:'safe'},{dash:2,onBeat:0.8,req:'always',drop:'crowd',dare:'risky'},{dash:3,onBeat:0.9,req:'always',drop:'asap',dare:'risky'},{dash:1,onBeat:0.6,req:'near',reqHp:0.8,drop:'asap',dare:'safe'}];
const out=[];
for(let i=0;i<50;i++){
  const sh=P(shows),v=sh<3?'basement':P(venues),c={name:'p'+String(i+1).padStart(2,'0'),skill:+(0.4+R()*0.55).toFixed(2),shows:sh,earned:sh<3?0:P(earned),band:P(bands),venue:v,
    venues:{basement:{best:9,cleared:true},observatory:{best:9,cleared:true},club:{best:9,cleared:true}},lv:{rig:Math.min(4,Math.floor(sh/6))},own:{}};
  const t=P(tiers);if(t)c.tier=t;const h=P(habits);if(h&&sh>=1)c.ai=h;
  if(sh>=6){const tw=P(twists);if(tw)c.twist=tw;if(tw==='mix')c.twistBand=P(['low','mid','high'])}
  if(R()<0.15)c.bias=P([-0.07,0.06,0.1]);   // uncalibrated headphones
  if(R()<0.2)c.mover='player';if(R()<0.1)c.twitch=true;if(sh>=12&&R()<0.4)c.own={chops:1,fanclub:1,roadcase:1,reroll:1};
  out.push(c)}
module.exports=out;
