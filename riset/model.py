import math
P=[('Netral (tren 2025)',0,0,50,50),('Kondisi sekarang',-15,5,50,45),('Dieksekusi lewat kinerja',80,60,60,70),('Dieksekusi lewat kroni',-50,40,20,30),('Kedekatan penuh',-100,0,50,20)]
BASE=dict(AL=0.5,DEP=0.05,BA=0.0075,BS=0.02,BQ=0.0025,TAU=8,RAMP=5,popm=1.0,labm=1.0,pc0=5000)
S0,G0,GAPC,THR,Y0,Y1=0.2877,0.0511,6.4*0.58,14000,2025,2050
def lgr(y,m):return m*(0.008-0.0075*(y-2025)/20 if y<2045 else 0.0002)
def pgr(y,m):return m*(0.0095-0.006*(y-2025)/20 if y<2045 else 0.003)
def run(k,rec,inv,q,p=BASE,shocks=None,horizon=70):
  kk=k/100;qq=(q-50)/50;AL=p['AL'];DEP=p['DEP']
  GA0=((1+G0)/(1+lgr(2025,p['labm'])))**(1-AL)-1
  Y=1.0;K=S0/(G0+DEP);L=1.0;A=Y/K**AL;pc=p['pc0'];hit=None;gs=[]
  for t in range(horizon):
    y=Y0+t;phi=1-math.exp(-t/p['TAU']);rho=min(1,t/p['RAMP'])
    ds=GAPC/100*(rec/100)*(inv/100)*rho;sv=S0+p['BS']*kk*phi+ds
    gA=GA0+p['BA']*kk*phi+p['BQ']*qq*phi
    if shocks and y in shocks: gA+=shocks[y]
    lg=lgr(y,p['labm']);pg=pgr(y,p['popm'])
    Kn=sv*Y+(1-DEP)*K;An=A*(1+gA);Ln=L*(1+lg);Yn=An*Kn**AL*Ln**(1-AL);g=Yn/Y-1
    pcn=pc*(1+g)/(1+pg)
    if hit is None and pcn>=THR:hit=y+(THR-pc)/(pcn-pc)
    pc=pcn;gs.append(g);K,A,L,Y=Kn,An,Ln,Yn
  n=Y1-Y0;prod=1
  for g in gs[:n]:prod*=1+g
  return dict(hit=hit,avg=(prod**(1/n)-1)*100)
if __name__=='__main__':
  for p in P: r=run(*p[1:]);print(f"{p[0]:28s} avg {r['avg']:.2f}%  hit {r['hit']:.1f}")
