# Playtest swarm

Simulated playtesters for bug and balance sweeps. Serve the project on port 8765 (`python3 -m http.server 8765`), then from this folder:

```sh
DL=$(( $(date +%s%3N) + 20*60*1000 ))                 # run for 20 minutes
for w in 0 1 2; do node swarm.js $w 3 $DL out.jsonl & done   # 3 workers cycle through the 50 personas in personas.js
node monkey.js $DL monkey.jsonl &                      # random keyboard / controller / touch input through the real menus
node -e "console.log(JSON.stringify(require('./personas.js')))" > personas.json
python3 summary.py out.jsonl personas.json             # bugs first, then win rates by career stage, venue, sound, band, twist, skill
```

`swarm.js` plays full shows through `tools/sim.js` (the demo AI on a fake clock, about 8 s a show) and logs one JSON line per show,
including errors and impossible states (NaN HP or position). `monkey.js` uses Playwright's Chromium and a fake gamepad.
