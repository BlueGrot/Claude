// Run from tools/playtest with the game served on :8765 (python3 -m http.server 8765 in the project folder). See README.md here.
// node swarm.js <worker> <workers> <deadline ms epoch> <out.jsonl>
const {chromium}=require('playwright'),fs=require('fs'),PS=require('./personas.js');
(async()=>{const [w,n,dl,outp]=process.argv.slice(2).map((x,i)=>i<3?+x:x);let b=await chromium.launch(),p,runs=0,i=w,pageErrs=[];
  const fresh=async()=>{if(p)await p.close();p=await b.newPage({viewport:{width:1280,height:800}});p.on('pageerror',e=>pageErrs.push(e.message));
    await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(1200);
    await p.evaluate(()=>new Promise(r=>{const s=document.createElement('script');s.src='/tools/sim.js?'+Date.now();s.onload=r;document.body.appendChild(s)}))};
  await fresh();
  while(Date.now()<dl){const cfg=PS[i%PS.length];i+=n;
    try{const r=await p.evaluate(async c=>{await __sims([c],1);return __simOut[0]},cfg);r.pageErrs=pageErrs.splice(0);fs.appendFileSync(outp,JSON.stringify(r)+'\n')}
    catch(e){fs.appendFileSync(outp,JSON.stringify({name:cfg.name,crash:String(e).slice(0,300)})+'\n');await fresh()}
    if(++runs%8===0)await fresh()}
  await b.close()})();
