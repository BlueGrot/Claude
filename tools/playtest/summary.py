import json,sys,collections,statistics as st
rs=[json.loads(l) for l in open(sys.argv[1])]
PS={p['name']:p for p in json.loads(open(sys.argv[2]).read())}
ok=[r for r in rs if 'crash' not in r]
print('runs',len(rs),'crashes',len(rs)-len(ok),'errors',sum(1 for r in ok if r.get('err')),'bad state',sum(1 for r in ok if r.get('bad')),'timeouts',sum(1 for r in ok if r.get('timeout')),'page errors',sum(len(r.get('pageErrs',[])) for r in ok))
for r in ok:
  if r.get('err') or r.get('bad') or r.get('pageErrs'):print('  BUG',r['name'],r.get('err','')[:300],r.get('bad',''),r.get('pageErrs'))
for r in rs:
  if 'crash' in r:print('  CRASH',r['name'],r['crash'])
def grp(key,label):
  g=collections.defaultdict(list)
  for r in ok:g[key(r)].append(r)
  print('\n'+label)
  for k in sorted(g,key=str):
    v=g[k];print(f"  {str(k):14} n={len(v):3}  won {100*sum(x['won'] for x in v)/len(v):3.0f}%  t {st.mean(x['t'] for x in v):4.0f}s  lvl {st.mean(x['lvl'] for x in v):4.1f}  hits {st.mean(x['hits'] for x in v):4.1f}  clip {100*sum(1 for x in v if x.get('clipEver'))/len(v):3.0f}%  causes {dict(collections.Counter(x['cause'] for x in v if x['cause']))}")
P=lambda r:PS[r['name']]
grp(lambda r:P(r)['shows'],'by shows played')
grp(lambda r:P(r)['venue'] if P(r)['shows']>=3 else 'basement(new)','by venue')
grp(lambda r:P(r).get('tier','default'),'by sound')
grp(lambda r:P(r)['band'],'by band')
grp(lambda r:(r.get('twist') or 'none') if P(r)['shows']>=6 else 'n/a (<6)','by twist (shows>=6)')
grp(lambda r:'%.1f'%(round(P(r)['skill']*5)/5),'by skill')
grp(lambda r:'bias' if P(r).get('bias') else 'calibrated','by headphone offset')
g=collections.defaultdict(list)
for r in ok:g[r['name']].append(r)
print('\nper persona (won/n, lvl range, dry max)')
line=[]
for n in sorted(g):
  v=g[n];p=PS[n];line.append(f"{n} s{p['skill']} sh{p['shows']} {p['venue'][:4]} {p.get('tier','-')[:4]} {p.get('twist','') or ''}: {sum(x['won'] for x in v)}/{len(v)} lv{min(x['lvl'] for x in v)}-{max(x['lvl'] for x in v)} dry{max(x.get('dry',0) for x in v)}")
print('\n'.join(line))
