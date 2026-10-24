// ten playtesters (8 shows in, so twists exist), used for the twist and ambient comparisons
const base=[{skill:0.5},{skill:0.6,ai:{dash:1,onBeat:0.5,req:'near',drop:'crowd',dare:'safe'}},{skill:0.7},{skill:0.7,ai:{dash:2,onBeat:0.8,req:'always',drop:'crowd',dare:'risky'}},{skill:0.8,mover:'player'},
  {skill:0.8,band:'synth'},{skill:0.9,ai:{dash:2,onBeat:0.8,req:'always',drop:'asap',dare:'risky'}},{skill:0.6,band:'rhythm'},{skill:0.75,venue:'club'},{skill:0.85,band:'dream',venue:'club'}]
 .map((c,i)=>({name:'t'+i,shows:8,earned:2000,band:'four',venue:'basement',venues:{basement:{best:9,cleared:true},observatory:{best:9,cleared:true}},lv:{rig:1},...c}));
const mode=process.argv[2],seeds=+process.argv[3],out=[];
for(let s=0;s<seeds;s++)for(const c of base){
  if(mode==='twist')for(const tw of ['none','mix','packed','roadie','glass','hot'])out.push({...c,tag:tw,twist:tw,twistBand:['low','mid','high'][s%3]});
  if(mode==='amb'){out.push({...c,tag:'default',twist:'none'});out.push({...c,tag:'ambient',twist:'none',tier:'ambient'})}}
console.log(JSON.stringify(out));
