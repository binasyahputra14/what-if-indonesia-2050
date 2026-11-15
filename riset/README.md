# Simulasi ketidakpastian

Kode untuk Ruang mesin bagian 9 di halaman utama. Python 3, tanpa library tambahan.

- `indeks.py`: menghitung posisi "Kondisi sekarang" dari indeks lembaga (WGI Bank Dunia, Transparency International, World Justice Project, International Budget Partnership, rasio pajak Kemenkeu). Saklar = perubahan persentil sejak garis dasar, 40 poin = saklar penuh. Hasil di `indeks.json`: saklar −12, belanja 50, celah pajak 0%.
- `model.py`: port Python dari simulator bagian 08 (model Solow). Hasil pusatnya identik: 2046, 2050, 2051, 2054, 2059.
- `mc2.py`: versi yang dipakai di halaman. Monte Carlo 10.000 simulasi untuk tiga versi (jalan mulus, dengan krisis, krisis bergantung institusi), plus analisis sensitivitas global Sobol (estimator Saltelli 2010 dan Jansen 1999). Krisis berat dikalibrasi ke 1998 (produktivitas −18%, PDB ±−13%). Hasil di `mc2.json`.
- `decomp.py`: uji porsi selisih kinerja vs kedekatan yang datang dari produktivitas. Hasil di `decomp.json`.
- `build.py`: menyusun bagian 9 halaman dari hasil JSON.
- `mc.py` / `mc.json`: versi awal (krisis berat masih −13%, terlalu ringan). Disimpan sebagai jejak revisi.

Galat ukur posisi "Kondisi sekarang" ikut diacak di `mc2.py`: saklar normal(−12; 6), belanja normal(50; 8), celah pajak 0–5%.

Jalankan: `python3 indeks.py`, `python3 mc2.py`, `python3 decomp.py`, lalu `python3 build.py` untuk menulis ulang bagian 9 di `index.html`.
