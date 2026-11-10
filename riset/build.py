import json,re
J=json.load(open('mc/mc2.json'));R=J['mc'];S=J['sobol'];D=json.load(open('mc/decomp.json'))
N=['Dieksekusi lewat kinerja','Netral (tren 2025)','Kondisi sekarang','Dieksekusi lewat kroni','Kedekatan penuh']
SH={'Dieksekusi lewat kinerja':'Lewat kinerja','Netral (tren 2025)':'Netral','Kondisi sekarang':'Kondisi sekarang','Dieksekusi lewat kroni':'Lewat kroni','Kedekatan penuh':'Kedekatan penuh'}
yr=lambda v:'setelah 2094' if v>=2095 else str(int(v+0.5))
pc=lambda v:f"{v*100:.0f}%"
def chart(modes,cls,lab):
  x0,x1,L,Rm,W=2040,2080,150,24,640;iw=W-L-Rm;X=lambda y:L+(min(y,x1)-x0)/(x1-x0)*iw
  g=''.join(f'<line x1="{X(y):.1f}" x2="{X(y):.1f}" y1="28" y2="296" class="mcg"/><text x="{X(y):.1f}" y="316" text-anchor="middle" class="m">{y}</text>' for y in range(2040,2081,10))
  g+=f'<line x1="{X(2045):.1f}" x2="{X(2045):.1f}" y1="22" y2="296" class="mc45"/><text x="{X(2045):.1f}" y="16" text-anchor="middle" class="m" style="fill:var(--accent)">2045</text>'
  for i,n in enumerate(N):
    y=40+i*52;g+=f'<text x="{L-10}" y="{y+14}" text-anchor="end">{SH[n]}</text>'
    for j,(m,c) in enumerate(zip(modes,cls)):
      v=R[m][n];yy=y+j*14;h=10 if j==0 else 14
      g+=f'<rect class="mcb {c}" x="{X(v["p10"]):.1f}" y="{yy}" width="{max(3,X(v["p90"])-X(v["p10"])):.1f}" height="{h}" rx="{h/2}"/>'
      if v['p90']>=x1:g+=f'<text x="{X(x1)+4:.1f}" y="{yy+h}" class="m">›</text>'
      g+=f'<circle cx="{X(v["p50"]):.1f}" cy="{yy+h/2}" r="5" class="mcd {c}"/>'
  return f'<svg viewBox="-40 0 680 326" role="img" aria-label="{lab}">{g}</svg>'
def table(m):
  h='<table class="mct"><thead><tr><th>Skenario</th><th>Rentang 80%</th><th>Tengah</th><th>Tembus ≤2050</th></tr></thead><tbody>'
  for n in N:v=R[m][n];h+=f'<tr><td>{SH[n]}</td><td>{yr(v["p10"])}–{yr(v["p90"])}</td><td><b>{yr(v["p50"])}</b></td><td>{pc(v["pr50"])}</td></tr>'
  return h+'</tbody></table>'
PL={'AL':'Porsi modal (α)','DEP':'Penyusutan modal','BA':'Efek kinerja → produktivitas','BS':'Efek kinerja → investasi','BQ':'Efek kualitas belanja','TAU':'Jeda efek institusi','popm':'Pertumbuhan penduduk','labm':'Pertumbuhan tenaga kerja','pc0':'Pendapatan per kapita 2025'}
def sbars(o,title):
  st=S[o]['ST'];ks=sorted(st,key=lambda k:-st[k]);W=640;L=230;iw=W-L-60
  g=''
  for i,k in enumerate(ks):
    v=max(0,st[k]);y=10+i*30
    g+=f'<text x="{L-10}" y="{y+16}" text-anchor="end">{PL[k]}</text><rect x="{L}" y="{y+4}" width="{iw}" height="16" rx="8" fill="#F3E9DC"/><rect x="{L}" y="{y+4}" width="{max(2,iw*min(1,v)):.1f}" height="16" rx="8" class="{"sbh" if v>=.2 else "sbl"}"/><text x="{L+iw*min(1,v)+8:.1f}" y="{y+17}" class="m">{v*100:.0f}%</text>'
  return f'<div class="vz vz-tx mcw"><h4>{title}</h4><svg viewBox="-70 0 {W+70} {10+len(ks)*30}">{g}</svg></div>'
mu,kr,rz=R['mulus'],R['krisis'],R['rezim']
gm,gk,gr=mu['gap_kin_ked'],kr['gap_kin_ked'],rz['gap_kin_ked'];nm,nk=mu['gap_kin_now'],kr['gap_kin_now']
stg=S['gap']['ST'];stn=S['now']['ST']
sec=f'''  <details class="rm"><summary><span>9 · Ketidakpastian: 10.000 simulasi<small>Monte Carlo, analisis sensitivitas Sobol, krisis yang bergantung institusi</small></span></summary>
  <section class="sec" id="ketidakpastian">
    <div class="num">RUANG MESIN · 9</div>
    <h2>Seberapa yakin angka-angka di halaman ini?</h2>
    <div class="prose">
      <p class="lead">Simulator di bagian 08 ngasih satu angka per skenario: 2046, 2051, 2059. Satu angka itu kelihatan pasti. Padahal di belakangnya ada beberapa angka yang cuma ditaksir.</p>
      <h3 style="font-size:19px">Kenapa pakai Monte Carlo</h3>
      <p>Bayangin ramalan cuaca. BMKG gak bilang "besok hujan jam 3 sore". Mereka bilang "peluang hujan 70%". Itu karena udara terlalu rumit buat ditebak pakai satu angka. Jadi mereka jalanin modelnya berkali-kali dengan kondisi awal yang sedikit beda-beda, lalu ngitung berapa kali hasilnya hujan.</p>
      <p>Monte Carlo persis begitu. Setiap angka yang cuma ditaksir di simulator gua acak dalam rentang yang masuk akal, terus modelnya dijalanin <b>10.000 kali per skenario</b>. Hasilnya bukan satu tahun, tapi <b>sebaran tahun</b>: paling mungkin tahun berapa, dan seberapa lebar kemungkinan melesetnya. Cara ini dipakai luas, dari kipas proyeksi inflasi bank sentral Inggris (Bank of England, sejak 1996) sampai panduan analisis sensitivitas model (Saltelli dkk., 2008).</p>
      <p>Ada tiga versi. <b>Jalan mulus</b>: cuma taksiran parameter yang diacak. <b>Dengan krisis</b>: ditambah guncangan acak dengan peluang sesuai sejarah Indonesia 30 tahun terakhir, yaitu satu krisis berat (1998) dan satu krisis sedang (2020). <b>Krisis bergantung institusi</b>: sama, tapi negara yang dijalankan lewat kedekatan lebih sering kena krisis. Versi ketiga ini uji kepekaan, bukan hasil utama.</p>
    </div>
    <div class="vz vz-tx mcw">
      <h4>Kapan tembus US$14.000: rentang 80% dari 10.000 simulasi</h4>
      <p class="tx-sub"><span class="mcl m"></span> jalan mulus &nbsp; <span class="mcl k"></span> dengan krisis &nbsp; titik = nilai tengah</p>
      {chart(['mulus','krisis'],['m','k'],'Rentang 80% tahun tembus US$14.000 per skenario')}
      <p class="tx-cap">Batang = 80% hasil simulasi jatuh di rentang ini (persentil 10–90). Tanda › berarti ujung kanan melewati 2080.</p>
    </div>
    <div class="mcgrid">
      <div><h3 style="font-size:17px">Jalan mulus</h3>{table('mulus')}</div>
      <div><h3 style="font-size:17px">Dengan krisis</h3>{table('krisis')}</div>
    </div>
    <h3 style="font-size:19px">Klaim utama halaman ini, diuji ulang</h3>
    <div class="table-wrap"><table class="mct"><thead><tr><th>Klaim</th><th>Angka di halaman</th><th>Jalan mulus (rentang 80%)</th><th>Dengan krisis (rentang 80%)</th></tr></thead><tbody>
      <tr><td>Selisih kinerja vs kedekatan penuh</td><td>±13 tahun</td><td><b>{gm["p10"]:.0f}–{gm["p90"]:.0f} tahun</b>, tengah {gm["p50"]:.0f}</td><td><b>{gk["p10"]:.0f}–{gk["p90"]:.0f} tahun</b>, tengah {gk["p50"]:.0f}</td></tr>
      <tr><td>Selisih kinerja vs kondisi sekarang</td><td>±5 tahun</td><td><b>{nm["p10"]:.0f}–{nm["p90"]:.0f} tahun</b>, tengah {nm["p50"]:.0f}</td><td><b>{nk["p10"]:.0f}–{nk["p90"]:.0f} tahun</b>, tengah {nk["p50"]:.0f}</td></tr>
      <tr><td>Porsi selisih yang datang dari produktivitas</td><td>±78%</td><td colspan="2"><b>{D["p10"]*100:.0f}–{D["p90"]*100:.0f}%</b>, tengah {D["p50"]*100:.0f}% (jalur produktivitas dimatikan untuk melihat sisa selisih yang datang dari investasi)</td></tr>
      <tr><td>Kinerja selalu lebih cepat dari kedekatan?</td><td>ya</td><td colspan="2"><b>Ya, di {pc(gm["pos"])} simulasi</b>, di ketiga versi</td></tr>
    </tbody></table></div>
    <div class="mcsum">
      <h3 style="font-size:19px;margin-top:0">Kesimpulannya, pakai bahasa sederhana</h3>
      <ol>
        <li><b>Urutannya pasti, jaraknya enggak.</b> Di 10.000 simulasi, kinerja selalu paling cepat dan kedekatan penuh selalu paling lambat. Yang gak pasti cuma selisihnya: {gm["p10"]:.0f}–{gm["p90"]:.0f} tahun kalau jalan mulus.</li>
        <li><b>Klaim "sebagian besar dari produktivitas" kokoh.</b> Di seluruh rentang, {D["p10"]*100:.0f}–{D["p90"]*100:.0f}% selisihnya datang dari produktivitas, bukan dari tambahan investasi.</li>
        <li><b>Krisis bikin jarak makin lebar, bukan makin sempit.</b> Kalau krisis dihitung sesuai peluang sejarahnya, selisih kinerja vs kedekatan melebar dari ±{gm["p50"]:.0f} ke ±{gk["p50"]:.0f} tahun. Ekonomi yang tumbuh lambat butuh lebih lama buat bangkit dari pukulan yang sama.</li>
        <li><b>2045 hampir mustahil, bahkan lewat kinerja.</b> Peluang skenario kinerja tembus di 2045: {pc(mu["Dieksekusi lewat kinerja"]["pr45"])} kalau jalan mulus, {pc(kr["Dieksekusi lewat kinerja"]["pr45"])} kalau krisis dihitung. Target Indonesia Emas 2045 butuh lebih dari skenario terbaik di simulator ini.</li>
        <li><b>Kedekatan penuh bisa gak pernah sampai.</b> Kalau krisis dihitung, {pc(kr["Kedekatan penuh"]["never"])} simulasi kedekatan penuh belum tembus sampai 2094.</li>
      </ol>
    </div>

    <h3 style="font-size:19px">Asal angka di setiap parameter</h3>
    <p class="fine">Kolom "asal angka" bilang dari mana nilai di simulator dan rentangnya datang. Kalau tertulis "penilaian", artinya angka itu taksiran gua, bukan hasil ukur. Justru angka-angka itulah yang paling perlu diacak.</p>
    <div class="table-wrap"><table class="mct mcm"><thead><tr><th>Parameter</th><th>Di simulator</th><th>Diacak dalam rentang</th><th>Asal angka</th><th>Alasan rentang</th></tr></thead><tbody>
      <tr><td><b>Porsi modal dalam output (α)</b><br><span class="fine">seberapa besar peran mesin dan bangunan dibanding pekerja</span></td><td>0,5</td><td>0,40–0,60</td><td>Penn World Table 11.0 mencatat porsi upah dalam PDB Indonesia ±0,51, jadi porsi modal ±0,49 (<a href="https://fred.stlouisfed.org/data/LABSHPIDA156NRUG" target="_blank" rel="noopener">PWT via FRED</a>).</td><td>Data PWT untuk Indonesia nyaris rata dari 1960 sampai 2016, tanda kemungkinan besar angka imputasi, bukan ukuran tahunan. Jadi diberi ruang ±0,1.</td></tr>
      <tr><td><b>Penyusutan modal per tahun</b><br><span class="fine">berapa persen mesin dan bangunan aus tiap tahun</span></td><td>5%</td><td>4–6%</td><td>Angka baku literatur pertumbuhan; Mankiw, Romer &amp; Weil (1992) memakai pertumbuhan teknologi + penyusutan = 5% untuk semua negara.</td><td>±1 poin di sekitar angka baku, karena komposisi aset tiap negara beda.</td></tr>
      <tr><td><b>Efek kinerja ke produktivitas</b><br><span class="fine">tambahan pertumbuhan produktivitas per tahun kalau saklar penuh ke kinerja</span></td><td>0,75 poin</td><td>0,375–1,125 poin (×0,5–1,5)</td><td><b>Penilaian.</b> Arahnya didukung riset Indonesia: audit menekan dana proyek yang hilang ±8 poin (Olken, 2007); perusahaan dekat kekuasaan lebih mudah dapat izin (Mobarak &amp; Purbasari, 2005). Tapi besarnya untuk skala nasional belum pernah diukur.</td><td>Karena gak ada ukuran langsung, rentangnya sengaja dibuat lebar: setengah sampai satu setengah kali nilai simulator.</td></tr>
      <tr><td><b>Efek kinerja ke investasi</b><br><span class="fine">tambahan porsi investasi kalau investor gak perlu bayar "premi takut"</span></td><td>2 poin PDB</td><td>1–3 poin (×0,5–1,5)</td><td><b>Penilaian</b>, dijangkarkan ke logika premi risiko di bagian 06.</td><td>Sama: lebar karena belum diukur.</td></tr>
      <tr><td><b>Efek kualitas belanja negara</b></td><td>0,25 poin</td><td>0,125–0,375 poin (×0,5–1,5)</td><td><b>Penilaian.</b> Arahnya dari riset belanja publik (Devarajan dkk., 1996).</td><td>Sama.</td></tr>
      <tr><td><b>Jeda efek institusi</b><br><span class="fine">berapa tahun sampai separuh efek reformasi terasa</span></td><td>±5,5 tahun</td><td>±3,5–8 tahun</td><td><b>Penilaian.</b> Reformasi institusi butuh waktu bertahun-tahun untuk terasa ke pertumbuhan.</td><td>Dari "cepat" (satu periode pemerintahan) sampai "lambat" (hampir dua periode).</td></tr>
      <tr><td><b>Pertumbuhan penduduk dan tenaga kerja</b></td><td>proyeksi BPS</td><td>80–120% dari proyeksi</td><td>Proyeksi penduduk BPS (disederhanakan, lihat bagian 6 Ruang mesin).</td><td><b>Penilaian:</b> proyeksi jangka panjang bisa meleset karena angka kelahiran dan migrasi.</td></tr>
      <tr><td><b>Pendapatan per kapita 2025</b></td><td>US$5.000</td><td>US$4.900–5.100</td><td>Titik awal halaman ini.</td><td>±2% untuk menampung revisi data PDB dan beda kurs rata-rata.</td></tr>
      <tr><td><b>Krisis berat, mirip 1998</b><br><span class="fine">versi dengan krisis</span></td><td>tidak ada</td><td>peluang 1/30 per tahun; produktivitas −18%, pulih 30% dalam 3 tahun</td><td>Dikalibrasi ke 1998: produktivitas −18% ditambah tren ±5% menghasilkan PDB ±−13%, mirip −13,1% (BPS). Pulih sebagian kecil saja karena kerugian output setelah krisis keuangan cenderung permanen (Cerra &amp; Saxena, 2008).</td><td>Satu kejadian dalam 30 tahun terakhir (1996–2025).</td></tr>
      <tr><td><b>Krisis sedang, mirip 2020</b><br><span class="fine">versi dengan krisis</span></td><td>tombol</td><td>peluang 1/30 per tahun; produktivitas −7%, pulih separuh dalam 3 tahun</td><td>Dikalibrasi ke 2020: −7% ditambah tren ±5% menghasilkan PDB ±−2%, mirip −2,07% (BPS). Sama dengan tombol krisis di simulator.</td><td>Satu kejadian dalam 30 tahun terakhir.</td></tr>
      <tr><td><b>Krisis bergantung institusi</b><br><span class="fine">versi ketiga saja</span></td><td>tidak ada</td><td>peluang krisis ×0,67 untuk kinerja penuh, sampai ×1,65 untuk kedekatan penuh</td><td><b>Penilaian.</b> Arahnya dari Acemoglu, Johnson, Robinson &amp; Thaicharoen (2003): institusi lemah membuat krisis lebih sering dan lebih parah. Besarnya belum diukur untuk Indonesia.</td><td>Dipakai sebagai uji kepekaan, bukan hasil utama.</td></tr>
    </tbody></table></div>
    <p class="fine">Setiap simulasi memakai parameter dan urutan krisis yang sama untuk kelima skenario, supaya selisih antarskenario murni datang dari pilihan kebijakan. Benih acak tetap (2026), jadi hasilnya bisa diulang persis. Model yang dipakai identik dengan simulator bagian 08 (hasil pusatnya sama: 2046, 2050, 2051, 2054, 2059). Kode lengkapnya terbuka di <a href="https://github.com/binasyahputra14/what-if-indonesia-2050/tree/main/riset" target="_blank" rel="noopener">folder riset di GitHub</a>.</p>

    <h3 style="font-size:19px">Uji lanjutan 1: angka mana yang paling bikin hasil goyah? (Sobol)</h3>
    <div class="prose"><p>Monte Carlo bilang seberapa lebar ketidakpastiannya. Tapi belum bilang <b>siapa biang keroknya</b>. Analisis sensitivitas global Sobol (Sobol', 2001; Saltelli dkk., 2010) menjawab itu: dari seluruh goyangan hasil, berapa persen yang disebabkan oleh tiap parameter, termasuk lewat interaksinya dengan parameter lain.</p></div>
    <div class="mcgrid">
      {sbars('now','Tahun tembus "kondisi sekarang": siapa yang bikin goyah')}
      {sbars('gap','Selisih kinerja vs kedekatan: siapa yang bikin goyah')}
    </div>
    <p class="fine">Indeks Sobol total (4.096 sampel dasar, ±45.000 kali jalan model per hasil). Jumlahnya bisa sedikit melewati 100% karena interaksi antarparameter ikut dihitung di tiap parameter.</p>
    <div class="inf"><h4>Inferensi</h4><p>Dua hasil ini bercerita beda. <b>Tahun tembus</b> "kondisi sekarang" paling banyak ditentukan hal yang relatif gak bisa diperdebatkan: pertumbuhan penduduk (±{stn["popm"]*100:.0f}%) dan titik awal pendapatan (±{stn["pc0"]*100:.0f}%). Tapi <b>selisih kinerja vs kedekatan</b>, inti argumen halaman ini, ±{stg["BA"]*100:.0f}% ditentukan satu angka saja: seberapa besar institusi menggeser produktivitas. Dan angka itu justru yang paling lemah dasarnya, karena masih penilaian. Jadi kalau ada satu angka yang harus diukur pakai data sungguhan berikutnya, ya angka itu.</p></div>

    <h3 style="font-size:19px">Uji lanjutan 2: kalau institusi lemah bikin krisis lebih sering</h3>
    <div class="table-wrap"><table class="mct"><thead><tr><th>Skenario</th><th>Rentang 80%</th><th>Tengah</th><th>Tembus ≤2050</th><th>Belum tembus s.d. 2094</th></tr></thead><tbody>
      {''.join(f'<tr><td>{SH[n]}</td><td>{yr(rz[n]["p10"])}–{yr(rz[n]["p90"])}</td><td><b>{yr(rz[n]["p50"])}</b></td><td>{pc(rz[n]["pr50"])}</td><td>{pc(rz[n]["never"])}</td></tr>' for n in N)}
    </tbody></table></div>
    <div class="inf"><h4>Inferensi</h4><p>Kalau kedekatan memang bikin krisis lebih sering, seperti arah temuan Acemoglu dkk. (2003), jaraknya jadi dramatis: skenario kinerja tembus di tengah-tengah {yr(rz["Dieksekusi lewat kinerja"]["p50"])}, sedangkan kedekatan penuh di {pc(rz["Kedekatan penuh"]["never"])} simulasi gak tembus sampai 2094. Ini menguatkan catatan di bagian 08 bahwa simulator utama kemungkinan <b>meremehkan</b> jarak kinerja vs kedekatan. Tapi besaran pengalinya penilaian, jadi angka di tabel ini jangan dikutip sebagai ramalan.</p></div>

    <div class="ctx"><h4>Batasan, dan apa yang harus dilakukan berikutnya</h4><p>Pertama, rentang parameter itu sebagian penilaian gua; kalau rentangnya diubah, hasilnya ikut berubah. Kedua, yang diacak cuma parameter, bukan bentuk modelnya: kalau model Solow-nya sendiri kurang tepat untuk Indonesia, simulasi ini gak bisa mendeteksinya. Ketiga, kurs gak dimodelkan; semua angka dalam dolar riil. Langkah berikutnya yang paling penting: mengganti "efek kinerja ke produktivitas" dari penilaian menjadi estimasi. Ada dua cara yang sahih secara ilmiah: <b>kalibrasi Bayesian</b> (mencocokkan model ke data pertumbuhan Indonesia 1990–2025 sehingga rentang parameter ditentukan data, bukan taksiran), dan <b>metode kontrol sintetis</b> (Abadie dkk., 2010: membandingkan Indonesia dengan "Indonesia tiruan" dari gabungan negara lain untuk mengukur efek perubahan institusi). Keduanya butuh data panel antarnegara dan belum dikerjakan di halaman ini.</p></div>
  </section>
  </details>
'''
p='whatif/what-if-indonesia.html';s=open(p).read()
i=s.index('  <details class="rm"><summary><span>9 · Ketidakpastian');j=s.index('  </details>\n',i)+len('  </details>\n')
s=s[:i]+sec+s[j:]
# update notes elsewhere
k=kr['Kondisi sekarang'];m=mu['Kondisi sekarang'];kin=kr['Dieksekusi lewat kinerja']
s=re.sub(r'"kondisi sekarang" tembus di \d{4}–\d{4} kalau jalan mulus, dan \d{4}–\d{4} kalau krisis seperti 1998 dan 2020 ikut dihitung sesuai peluang sejarahnya\. Lewat kinerja: \d{4}–\d{4} dengan krisis\.',
 f'"kondisi sekarang" tembus di {yr(m["p10"])}–{yr(m["p90"])} kalau jalan mulus, dan {yr(k["p10"])}–{yr(k["p90"])} kalau krisis seperti 1998 dan 2020 ikut dihitung sesuai peluang sejarahnya. Lewat kinerja: {yr(kin["p10"])}–{yr(kin["p90"])} dengan krisis.',s)
css='.mcsum{background:var(--accent-soft);border-radius:18px;padding:18px 20px;margin:18px 0}.mcsum ol{margin:8px 0 0;padding-left:20px}.mcsum li{margin:8px 0;line-height:1.55}\n.mcw .sbh{fill:var(--accent)}.mcw .sbl{fill:#D9CBB8}\n.mcm td{font-size:13.5px}\n'
if '.mcsum{' not in s:
  ii=s.index('.mcw svg text{');s=s[:ii]+css+s[ii:]
open(p,'w').write(s);print('ok')
