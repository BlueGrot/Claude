import json,sys,collections,statistics as st
for f in sys.argv[1:]:
  rs=[json.loads(l) for l in open(f)];g=collections.defaultdict(list)
  for r in rs:g[r.get('tag')].append(r)
  print('==',f.split('/')[-1],len(rs),'runs','errors',sum(1 for r in rs if r.get('err') or r.get('crash') or r.get('bad')))
  for k,v in g.items():
    v=[x for x in v if 'crash' not in x]
    print(f"  {k:8} n={len(v):3} won {100*sum(x['won'] for x in v)/len(v):3.0f}%  t {st.mean(x['t'] for x in v):4.0f}s  lvl {st.mean(x['lvl'] for x in v):4.1f}  hits {st.mean(x['hits'] for x in v):4.1f}  kills {st.mean(x.get('kills',0) for x in v):5.0f}  minHp {st.mean(x['minHp'] for x in v):.2f}")
