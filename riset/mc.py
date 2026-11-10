import random,json,statistics as st
from model import run,P,BASE
N=10000;rng=random.Random(2026)
def draw():
  p=dict(BASE);p['AL']=rng.uniform(.40,.60);p['DEP']=rng.uniform(.04,.06)
  for k in('BA','BS','BQ'):p[k]=BASE[k]*rng.uniform(.5,1.5)
  p['TAU']=rng.uniform(5,12);p['popm']=rng.uniform(.8,1.2);p['labm']=rng.uniform(.8,1.2);p['pc0']=rng.uniform(4900,5100);return p
def shocks():
  s={}
  for y in range(2026,2095):
    u=rng.random()
    if u<1/30:  # berat, mirip 1998
      s[y]=s.get(y,0)-0.13
      for j in (1,2,3):s[y+j]=s.get(y+j,0)+0.13/3*0.3/1  # pulih ~30%
    elif u<2/30: # sedang, mirip 2020 (sama dengan tombol di simulator)
      s[y]=s.get(y,0)-0.07
      for j in (1,2,3):s[y+j]=s.get(y+j,0)+0.035/3
  return s
def q(a,pr):a=sorted(a);return a[min(len(a)-1,int(pr*len(a)))]
def main():
 res={}
 for mode in('mulus','krisis'):
   H={p[0]:[] for p in P};AVG={p[0]:[] for p in P};GAP=[];GAP2=[]
   for i in range(N):
     p=draw();s=shocks() if mode=='krisis' else None
     hs={}
     for sc in P:
       r=run(*sc[1:],p=p,shocks=s);h=r['hit'] if r['hit'] else 2095
       H[sc[0]].append(h);AVG[sc[0]].append(r['avg']);hs[sc[0]]=h
     GAP.append(hs['Kedekatan penuh']-hs['Dieksekusi lewat kinerja']);GAP2.append(hs['Kondisi sekarang']-hs['Dieksekusi lewat kinerja'])
   out={}
   for sc in P:
     h=H[sc[0]];out[sc[0]]=dict(p10=q(h,.1),p50=q(h,.5),p90=q(h,.9),pr45=sum(x<=2045 for x in h)/N,pr50=sum(x<=2050 for x in h)/N,never=sum(x>=2095 for x in h)/N,avg50=q(AVG[sc[0]],.5),avg10=q(AVG[sc[0]],.1),avg90=q(AVG[sc[0]],.9))
   out['gap_kin_ked']=dict(p10=q(GAP,.1),p50=q(GAP,.5),p90=q(GAP,.9),pos=sum(g>0 for g in GAP)/N)
   out['gap_kin_now']=dict(p10=q(GAP2,.1),p50=q(GAP2,.5),p90=q(GAP2,.9))
   res[mode]=out
 json.dump(res,open('mc.json','w'),indent=1)
 for m,o in res.items():
   print('==',m)
   for k,v in o.items():print(f"  {k:26s}",{a:(round(b,1) if isinstance(b,float) and b>1 else round(b,3)) for a,b in v.items()})

if __name__=="__main__":main()
