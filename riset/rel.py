from mc2 import mc
import json
out={}
for mode in ('mulus','krisis'):
  rows=[]
  for seed in (2026,1,42,777,31337):
    r=mc(mode,N=10000,seed=seed)
    rows.append(dict(seed=seed,now=(r['Kondisi sekarang']['p10'],r['Kondisi sekarang']['p50'],r['Kondisi sekarang']['p90']),gap=(r['gap_kin_ked']['p10'],r['gap_kin_ked']['p50'],r['gap_kin_ked']['p90']),pos=r['gap_kin_ked']['pos']))
  out[mode]=rows
  print('==',mode)
  for x in rows:print('  seed %6d  sekarang p10/50/90 %s  selisih p10/50/90 %s  kinerja>kedekatan %.3f'%(x['seed'],tuple(round(v,1) for v in x['now']),tuple(round(v,1) for v in x['gap']),x['pos']))
json.dump(out,open('rel.json','w'))
