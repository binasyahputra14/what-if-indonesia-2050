"""Uji kepekaan: selisih kinerja vs kedekatan kalau efek institusi ke produktivitas lebih kecil."""
from model import run,P,BASE
kin=P[2][1:];ked=P[4][1:];now=P[1][1:]
for m in (0,0.25,0.5,1,1.5):
  p=dict(BASE);p['BA']=BASE['BA']*m
  print(f"efek x{m}: kinerja vs kedekatan {run(*ked,p=p)['hit']-run(*kin,p=p)['hit']:.1f} th, kinerja vs sekarang {run(*now,p=p)['hit']-run(*kin,p=p)['hit']:.1f} th")
