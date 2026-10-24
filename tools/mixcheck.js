// Mix check for Feedback Loop: renders each part offline in every sound set and measures its loudness, so levels can be
// compared across sets. Load it into a freshly loaded game page (served over http, audio not started yet):
//   await new Promise(r=>{const s=document.createElement('script');s.src='/tools/mixcheck.js?'+Date.now();s.onload=r;document.body.appendChild(s)})
//   await __mixcheck()          // -> {table, rows}; table is text, rows are {set, part, lufs}
// Each part plays a typical 4 s pattern at 120 bpm through its mixer channel (trims, pan and stereo included). Loudness is
// K-weighted mean square of the mix bus (AU.out, before the master tilt, glue compressor and limiter), roughly LUFS.
// It swaps window.AudioContext for an OfflineAudioContext while it runs, so reload the page afterwards.
(function(){
  const SR=48000,LEN=4.5,B=0.5;
  const PATTERNS={   // part -> list of [beat, event fields]
    kick:   [0,1,2,3,4,5,6,7].map(b=>[b,{vel:0.9,hz:45}]),
    snare:  [1,3,5,7].map(b=>[b,{vel:0.9}]),
    hat:    [...Array(16).keys()].map(i=>[i/2,{vel:0.8,len:0.045}]),
    crash:  [[0,{vel:1}]],
    bass:   [...Array(16).keys()].map(i=>[i/2,{m:40,dur:0.22}]),
    lead:   [0,1,2,3,4,5,6,7].map(b=>[b,{m:72}]),
    leadHold:[[0,{m:72,dur:1.8,hold:1,part:'lead'}],[4,{m:74,dur:1.8,hold:1,part:'lead'}]],
    pad:    [[0,{m:[60,64,67],dur:1.9,att:0.05}],[4,{m:[62,65,69],dur:1.9,att:0.05}]],
    melody: [0,1,2,3,4,5,6,7].map(b=>[b,{m:72,dur:0.45,vel:0.8}]),
    backing:[[0,{m:[60,64,67],dur:1.9,vel:1}],[4,{m:[62,65,69],dur:1.9,vel:1}]],
    sparkle:[...Array(16).keys()].map(i=>[i/2,{m:84}])
  };
  const SETS=['chip','fm16','rave','trance','vapor'];
  function freshAU(){for(const k of Object.keys(AU)){const v=AU[k];if(v instanceof AudioNode||v instanceof AudioBuffer||v instanceof BaseAudioContext||(v&&typeof v==='object'&&!Array.isArray(v)&&Object.values(v).some(x=>x instanceof AudioNode)))AU[k]=null}}
  async function kWeighted(buf){   // K-weighting (high shelf +4 dB at 1.68 kHz, high-pass 38 Hz), then mean square over both channels
    const o=new OfflineAudioContext(2,buf.length,SR),s=o.createBufferSource();s.buffer=buf;
    const hs=o.createBiquadFilter();hs.type='highshelf';hs.frequency.value=1681;hs.gain.value=4;const hp=o.createBiquadFilter();hp.type='highpass';hp.frequency.value=38;hp.Q.value=0.5;
    s.connect(hs);hs.connect(hp);hp.connect(o.destination);s.start();const r=await o.startRendering();
    let e=0;for(let c=0;c<2;c++){const d=r.getChannelData(c);for(let i=0;i<d.length;i++)e+=d[i]*d[i]}return -0.691+10*Math.log10(e/r.length+1e-12)}
  async function renderPart(set,part){
    const RealAC=window.AudioContext;let off;
    window.AudioContext=function(){off=new OfflineAudioContext(2,Math.round(SR*LEN),SR);return off};
    try{
      freshAU();SET.devSet=set;SET.allTiers=true;SOUND='';applySound();AU.init();
      // measure the mix bus: AU.out straight to the output, around the master chain
      AU.out.disconnect();AU.out.connect(off.destination);
      const si=SETLIST.findIndex(s=>!s.amb);ENG.set=null;ENG.enter(si,0);
      for(const [b,f] of PATTERNS[part])ENG.note(f.part||part,{t:0.05+b*B,si,qn:b,vel:1,dur:0.2,...f});
      const buf=await off.startRendering();return await kWeighted(buf);
    }finally{window.AudioContext=RealAC}
  }
  window.__mixcheck=async function(sets=SETS,parts=Object.keys(PATTERNS)){
    const muted=SET.muted,set0=SET.devSet,all0=SET.allTiers;SET.muted=false;const rows=[];
    try{for(const part of parts)for(const set of sets)rows.push({set,part,lufs:+(await renderPart(set,part)).toFixed(1)})}
    finally{SET.muted=muted;SET.devSet=set0;SET.allTiers=all0}
    const head='part'.padEnd(10)+sets.map(s=>s.padStart(8)).join('')+'   median   spread';
    const lines=parts.map(p=>{const v=sets.map(s=>rows.find(r=>r.part===p&&r.set===s).lufs),srt=[...v].sort((a,b)=>a-b),med=srt[srt.length>>1];
      return p.padEnd(10)+v.map(x=>(x<-90?'   -inf':x.toFixed(1).padStart(8))).join('')+med.toFixed(1).padStart(9)+(Math.max(...v)-Math.min(...v)).toFixed(1).padStart(9)});
    window.__mixRows=rows;return {table:[head,...lines].join('\n'),rows};
  };
})();
