// Run from tools/playtest with the game served on :8765 (python3 -m http.server 8765 in the project folder). See README.md here.
// node monkey.js <deadline> <out.log>: drives the real UI with random keyboard / controller / touch input
const {chromium}=require('playwright'),fs=require('fs');
(async()=>{const [dl,outp]=[+process.argv[2],process.argv[3]];const log=s=>fs.appendFileSync(outp,s+'\n');let sess=0;
  while(Date.now()<dl){sess++;const mode=['keys','pad','touch'][sess%3];const b=await chromium.launch();
    const ctx=await b.newContext(mode==='touch'?{viewport:{width:390,height:844},hasTouch:true,isMobile:true}:{viewport:{width:1280,height:800}});const p=await ctx.newPage();
    const errs=new Set();p.on('pageerror',e=>errs.add('pageerror: '+e.message));p.on('console',m=>{if(m.type()==='error')errs.add('console: '+m.text().slice(0,200))});
    await p.addInitScript(()=>{const mk=()=>({id:'fake',connected:true,mapping:'standard',timestamp:performance.now(),axes:[0,0,0,0],buttons:Array.from({length:17},()=>({pressed:false,value:0}))});
      window.__gp=mk();navigator.getGamepads=()=>[window.__gp];window.__press=(i,on)=>{__gp.buttons[i]={pressed:on,value:on?1:0};__gp.timestamp=performance.now()};window.__axes=(x,y)=>{__gp.axes=[x,y,0,0]}});
    await p.goto('http://localhost:8765/index.html'+(mode==='touch'?'?touch':''));await p.waitForTimeout(1200);
    const shows=[0,1,3,6,9,30][sess%6];await p.evaluate(s=>{META.shows=s;META.earned=s*900;META.fans=5000;for(const v of ['basement','observatory','club'])META.venues[v]={best:9,cleared:true};saveMeta()},shows);
    const states={};const t0=Date.now(),until=Math.min(dl,t0+150000);
    const tap=async i=>{await p.evaluate(i=>__press(i,true),i);await p.waitForTimeout(60);await p.evaluate(i=>__press(i,false),i)};
    try{while(Date.now()<until){
      const st=await p.evaluate(()=>state);states[st]=(states[st]||0)+1;const r=Math.random();
      if(mode==='pad'){
        if(st==='play'){await p.evaluate(([x,y])=>__axes(x,y),[Math.random()*2-1,Math.random()*2-1]);await tap(r<0.6?0:r<0.7?1:r<0.75?2:r<0.8?3:r<0.85?4:r<0.9?5:r<0.93?6:r<0.95?9:7)}
        else{await p.evaluate(()=>__axes(0,0));await tap(r<0.4?[12,13,14,15][Math.random()*4|0]:r<0.85?0:r<0.95?1:9)}}
      else if(mode==='keys'){
        if(st==='play'){const k=r<0.5?'Space':r<0.6?'ShiftLeft':r<0.65?'KeyE':r<0.7?'Tab':r<0.75?'Digit1':r<0.78?'Digit2':r<0.8?'Escape':['KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowLeft'][Math.random()*6|0];
          if(k.startsWith('Key')&&'WASD'.includes(k[3])||k.startsWith('Arrow')){await p.keyboard.down(k);await p.waitForTimeout(250);await p.keyboard.up(k)}else await p.keyboard.press(k)}
        else if(st==='levelup')await p.keyboard.press(['Digit1','Digit2','Digit3'][Math.random()*3|0]);
        else if(st==='edit'){if(r<0.6){const c=await p.$$('#grid button');if(c.length)await c[Math.random()*c.length|0].click({timeout:500}).catch(()=>{})}else await p.keyboard.press('Enter')}
        else if(st==='paused')await p.keyboard.press(r<0.8?'Escape':'Tab');
        else{const bs=await p.$$('.ov:not(.hidden) button');if(r<0.5)await p.keyboard.press('Enter');else if(bs.length)await bs[Math.random()*bs.length|0].click({timeout:500}).catch(()=>{})}}
      else{   // touch: taps on the right half, drags on the left, buttons in menus
        if(st==='play'){if(r<0.6)await p.touchscreen.tap(250+Math.random()*130,200+Math.random()*500);else{await p.touchscreen.tap(60+Math.random()*100,300+Math.random()*300)}
          if(Math.random()<0.05)await p.click('#seqBtn',{timeout:500}).catch(()=>{});if(Math.random()<0.03)await p.click('#pauseBtn',{timeout:500}).catch(()=>{})}
        else{const bs=await p.$$('.ov:not(.hidden) button, .ov:not(.hidden) .card');if(bs.length)await bs[Math.random()*bs.length|0].tap({timeout:500}).catch(()=>{})}}
      await p.waitForTimeout(80+Math.random()*200);
      const le=await p.evaluate(()=>typeof loopErrs!=='undefined'?[...loopErrs]:[]);for(const e of le)errs.add('loopErr: '+e);
    }}catch(e){errs.add('driver: '+String(e).slice(0,200))}
    log(JSON.stringify({sess,mode,shows,states,errs:[...errs]}));await b.close()}})();
