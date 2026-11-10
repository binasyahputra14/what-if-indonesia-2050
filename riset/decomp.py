import random,json
from model import run,P,BASE
from mc import draw,q
import mc
kin=P[2][1:];ked=P[4][1:]
def share(p):
  full=run(*ked,p=p)['hit']-run(*kin,p=p)['hit']
  p2=dict(p);p2['BA']=0;p2['BQ']=0   # matikan jalur produktivitas
  inv=run(*ked,p=p2)['hit']-run(*kin,p=p2)['hit']
  return full,inv,(full-inv)/full
f,i,s=share(dict(BASE));print('pusat: gap %.1f, tanpa jalur produktivitas %.1f, porsi produktivitas %.0f%%'%(f,i,s*100))
mc.rng.seed(7);S=[]
for _ in range(5000):S.append(share(draw())[2])
print('rentang porsi produktivitas: p10 %.0f%% p50 %.0f%% p90 %.0f%%'%(q(S,.1)*100,q(S,.5)*100,q(S,.9)*100))
json.dump(dict(center=s,p10=q(S,.1),p50=q(S,.5),p90=q(S,.9)),open('decomp.json','w'))
