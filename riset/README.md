# Simulasi ketidakpastian

Kode untuk Ruang mesin bagian 9 di halaman utama. Python 3, tanpa library tambahan.

- `model.py`: port Python dari simulator bagian 08 (model Solow). Hasil pusatnya identik: 2046, 2050, 2051, 2054, 2059.
- `mc2.py`: versi yang dipakai di halaman. Monte Carlo 10.000 simulasi untuk tiga versi (jalan mulus, dengan krisis, krisis bergantung institusi), plus analisis sensitivitas global Sobol (estimator Saltelli 2010 dan Jansen 1999). Krisis berat dikalibrasi ke 1998 (produktivitas −18%, PDB ±−13%). Hasil di `mc2.json`.
- `decomp.py`: uji porsi selisih kinerja vs kedekatan yang datang dari produktivitas. Hasil di `decomp.json`.
- `build.py`: menyusun bagian 9 halaman dari hasil JSON.
- `mc.py` / `mc.json`: versi awal (krisis berat masih −13%, terlalu ringan). Disimpan sebagai jejak revisi.

Jalankan: `python3 mc2.py`, lalu `python3 decomp.py`.
