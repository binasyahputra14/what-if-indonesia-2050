"""Indeks lembaga untuk posisi "Kondisi sekarang" di simulator bagian 08.

Prinsip:
1. Posisi saklar = ARAH PERUBAHAN institusi sejak garis dasar 2025, bukan tingkatnya.
   Tingkat institusi 2025 sudah tertanam di pertumbuhan 5,11% yang jadi titik awal model,
   jadi memakai tingkat akan menghitungnya dua kali.
2. Semua sumber diubah ke persentil global, dari peringkat: persentil = (N - peringkat) / (N - 1) x 100.
3. Skala saklar: perubahan 40 poin persentil = saklar penuh (100).
   40 poin = jarak dari median (persentil 50) ke persentil 90, sekitar 1,28 simpangan baku.
   Di jarak itulah literatur memberi besaran yang dipakai simulator
   (Mauro 1995 untuk investasi; Acemoglu, Naidu, Restrepo & Robinson 2019 untuk produktivitas).
4. Hanya perubahan yang sudah terukur yang dipakai. Tidak diekstrapolasi.

Jalankan: python3 indeks.py  ->  indeks.json
"""
import json,statistics as st

def pct(rank,n):return (n-rank)/(n-1)*100

# ---- Tingkat 2025/2026 (konteks: posisi Indonesia di dunia) ----
LEVEL=[
 # nama, lembaga, tahun data, peringkat, jumlah negara, tuas
 ('Pengendalian korupsi','Bank Dunia, WGI',2025,134,207,'saklar'),
 ('Supremasi hukum','Bank Dunia, WGI',2025,114,207,'saklar'),
 ('Kualitas regulasi','Bank Dunia, WGI',2025,85,205,'saklar'),
 ('Indeks Persepsi Korupsi','Transparency International',2025,109,180,'saklar'),
 ('Indeks Negara Hukum','World Justice Project',2026,75,143,'saklar'),
 ('Efektivitas pemerintah','Bank Dunia, WGI',2025,82,205,'belanja'),
 ('Pengawasan anggaran','International Budget Partnership, OBS',2023,46,125,'belanja'),
 ('Keterbukaan anggaran','International Budget Partnership, OBS',2023,20,125,'konteks'),
]
# ---- Perubahan yang terukur sejak garis dasar ----
CHANGE=[
 # nama, lembaga, (tahun, peringkat, N) sebelum, (tahun, peringkat, N) sesudah
 ('Indeks Persepsi Korupsi','Transparency International',(2024,99,180),(2025,109,180)),
 ('Indeks Negara Hukum','World Justice Project',(2025,69,142),(2026,75,143)),
]
# Pemeriksa arah (skor 0-100 Bank Dunia, bukan peringkat): Supremasi hukum 56,9 (2023) -> 55,1 (2024) -> 54,4 (2025).
RL_SCORE={2023:56.9,2024:55.1,2025:54.4}
TAX={2024:10.08,2025:9.31}   # rasio perpajakan, % PDB (Kemenkeu, via DDTC News)
SCALE=40.0

lv=[dict(nama=a,lembaga=b,tahun=c,peringkat=d,n=e,tuas=f,persentil=round(pct(d,e),1)) for a,b,c,d,e,f in LEVEL]
ch=[]
for a,b,(y0,r0,n0),(y1,r1,n1) in CHANGE:
  p0,p1=pct(r0,n0),pct(r1,n1);ch.append(dict(nama=a,lembaga=b,dari=[y0,r0,n0,round(p0,1)],ke=[y1,r1,n1,round(p1,1)],delta=round(p1-p0,1)))
dm=st.mean(c['delta'] for c in ch)
k=round(100*dm/SCALE)
out=dict(
 tingkat=lv,
 tingkat_saklar=round(st.mean(x['persentil'] for x in lv if x['tuas']=='saklar'),1),
 tingkat_belanja=round(st.mean(x['persentil'] for x in lv if x['tuas']=='belanja'),1),
 perubahan=ch,perubahan_rata=round(dm,2),
 saklar=k,saklar_rentang_sd=6,
 kualitas_belanja=50,kualitas_belanja_sd=8,
 celah_pajak_tertutup=0,celah_pajak_rentang=[0,5],
 pemeriksa_arah_supremasi_hukum=RL_SCORE,rasio_pajak=TAX,
 catatan=['Saklar: rata-rata perubahan persentil dua indeks yang sebanding (TI dan WJP), diskalakan 40 poin = saklar penuh. Arahnya dikonfirmasi skor supremasi hukum Bank Dunia yang turun 2023-2025.',
          'Kualitas belanja: belum ada pengukuran perubahan yang sebanding sejak 2025, jadi posisi tengah (50). IMF (2026) menyebut celah efisiensi investasi publik melebar dalam beberapa tahun terakhir, tanpa angka; arah itu ditampung lewat rentang.',
          'Celah pajak: rasio perpajakan turun dari 10,08% (2024) ke 9,31% (2025), jadi belum ada bukti celah kepatuhan mulai tertutup. Nilai 0; rentang 0-5% untuk kemungkinan penurunan rasio itu disebabkan harga komoditas, bukan kepatuhan.'])
json.dump(out,open('indeks.json','w'),indent=1,ensure_ascii=False)
for x in lv:print(f"{x['nama']:26s} {x['lembaga']:38s} {x['tahun']} #{x['peringkat']}/{x['n']} -> persentil {x['persentil']}")
print('tingkat saklar',out['tingkat_saklar'],'| tingkat belanja',out['tingkat_belanja'])
for c in ch:print(c)
print('perubahan rata-rata',out['perubahan_rata'],'-> saklar',k)
