// node batch.js <port> <cfgs.json> <out.jsonl> <worker> <workers> [setup js]: runs each cfg once (cfg.tag is carried into the output)
const {chromium}=require('playwright'),fs=require('fs');
(async()=>{const [port,cf,outp,w,n,setup]=process.argv.slice(2);const cfgs=JSON.parse(fs.readFileSync(cf));const b=await chromium.launch();let p,runs=0;
  const fresh=async()=>{if(p)await p.close();p=await b.newPage();await p.goto(`http://localhost:${port}/index.html`);await p.waitForTimeout(1000);
    await p.evaluate(()=>new Promise(r=>{const s=document.createElement('script');s.src='/tools/sim.js?'+Date.now();s.onload=r;document.body.appendChild(s)}));if(setup)await p.evaluate(setup)};
  await fresh();
  for(let i=+w;i<cfgs.length;i+=+n){const c=cfgs[i];try{const r=await p.evaluate(async c=>{await __sims([c],1);return __simOut[0]},c);r.tag=c.tag;fs.appendFileSync(outp,JSON.stringify(r)+'\n')}catch(e){fs.appendFileSync(outp,JSON.stringify({tag:c.tag,name:c.name,crash:String(e).slice(0,200)})+'\n');await fresh()}
    if(++runs%8===0)await fresh()}
  await b.close()})();
