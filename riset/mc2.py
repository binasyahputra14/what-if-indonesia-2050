"""Monte Carlo (dikalibrasi ulang), varian krisis bergantung institusi, dan analisis sensitivitas global Sobol."""
import random,json,math
from model import run,P,BASE
NAMES=[p[0] for p in P];KIN=P[2][1:];KED=P[4][1:];NOW=P[1][1:]
RANGES=dict(AL=(.40,.60),DEP=(.04,.06),BA=(.5,1.5),BS=(.5,1.5),BQ=(.5,1.5),TAU=(5,12),popm=(.8,1.2),labm=(.8,1.2),pc0=(4900,5100))
MULT=('BA','BS','BQ')
def params(u):  # u: dict nama->[0,1]
  p=dict(BASE)
  for k,(a,b) in RANGES.items():
    v=a+(b-a)*u[k];p[k]=BASE[k]*v if k in MULT else v
  return p
SEV=-0.18;SEV_REC=0.30;MOD=-0.07;MOD_REC=0.5;LAM=1/30
def shocks(rng,mult=1.0):
  s={}
  for y in range(2026,2095):
    u=rng.random()
    if u<LAM*mult:
      s[y]=s.get(y,0)+SEV
      for j in (1,2,3):s[y+j]=s.get(y+j,0)-SEV*SEV_REC/3
    elif u<2*LAM*mult:
      s[y]=s.get(y,0)+MOD
      for j in (1,2,3):s[y+j]=s.get(y+j,0)-MOD*MOD_REC/3
  return s
def crisis_mult(k):return math.exp(-0.5*k/100)   # kinerja 80 -> 0,67x ; kedekatan -100 -> 1,65x
def q(a,pr):a=sorted(a);return a[min(len(a)-1,int(pr*len(a)))]
def hit(sc,p,s):r=run(*sc,p=p,shocks=s);return r['hit'] if r['hit'] else 2095
def mc(mode,N=10000,seed=2026):
  rng=random.Random(seed);H={n:[] for n in NAMES};G=[];G2=[]
  for _ in range(N):
    p=params({k:rng.random() for k in RANGES})
    if mode=='rezim':
      st=rng.getstate();hs={}
      for sc in P:
        rng.setstate(st);s=shocks(rng,crisis_mult(sc[1]));hs[sc[0]]=hit(sc[1:],p,s)
    else:
      s=shocks(rng) if mode=='krisis' else None;hs={sc[0]:hit(sc[1:],p,s) for sc in P}
    for n in NAMES:H[n].append(hs[n])
    G.append(hs[NAMES[4]]-hs[NAMES[2]]);G2.append(hs[NAMES[1]]-hs[NAMES[2]])
  out={n:dict(p10=q(H[n],.1),p50=q(H[n],.5),p90=q(H[n],.9),pr45=sum(x<=2045 for x in H[n])/N,pr50=sum(x<=2050 for x in H[n])/N,never=sum(x>=2095 for x in H[n])/N) for n in NAMES}
  out['gap_kin_ked']=dict(p10=q(G,.1),p50=q(G,.5),p90=q(G,.9),pos=sum(g>0 for g in G)/N)
  out['gap_kin_now']=dict(p10=q(G2,.1),p50=q(G2,.5),p90=q(G2,.9))
  return out
def sobol(f,N=4096,seed=11):
  rng=random.Random(seed);ks=list(RANGES);d=len(ks)
  A=[[rng.random() for _ in ks] for _ in range(N)];B=[[rng.random() for _ in ks] for _ in range(N)]
  ev=lambda row:f(params(dict(zip(ks,row))))
  fA=[ev(r) for r in A];fB=[ev(r) for r in B]
  mean=sum(fA+fB)/(2*N);var=sum((x-mean)**2 for x in fA+fB)/(2*N-1)
  fA=[x-mean for x in fA];fB=[x-mean for x in fB]
  S1={};ST={}
  for i,k in enumerate(ks):
    fAB=[ev(A[j][:i]+[B[j][i]]+A[j][i+1:])-mean for j in range(N)]
    S1[k]=sum(fB[j]*(fAB[j]-fA[j]) for j in range(N))/N/var      # Saltelli 2010
    ST[k]=sum((fA[j]-fAB[j])**2 for j in range(N))/(2*N)/var     # Jansen 1999
  return dict(S1=S1,ST=ST,var=var)
if __name__=='__main__':
  import sys
  if 'sobol' in sys.argv:
    old=json.load(open('mc2.json'));R=old['mc']
  else:
    R={m:mc(m) for m in ('mulus','krisis','rezim')}
  S={'now':sobol(lambda p:hit(NOW,p,None)),'gap':sobol(lambda p:hit(KED,p,None)-hit(KIN,p,None))}
  json.dump(dict(mc=R,sobol=S),open('mc2.json','w'),indent=1)
  for m in R:
    print('==',m)
    for n in NAMES+['gap_kin_ked','gap_kin_now']:print('  ',n,{a:round(b,2) for a,b in R[m][n].items()})
  for o in S:
    print('== sobol',o);[print(f"   {k:5s} S1 {S[o]['S1'][k]:.2f}  ST {S[o]['ST'][k]:.2f}") for k in RANGES]
