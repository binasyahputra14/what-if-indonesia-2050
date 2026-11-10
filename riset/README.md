# Simulasi ketidakpastian (Monte Carlo)

Kode untuk Ruang mesin bagian 9 di halaman utama.

- `model.py`: port Python dari simulator bagian 08 (model Solow). Hasil pusatnya identik dengan simulator: 2046, 2050, 2051, 2054, 2059.
- `mc.py`: 10.000 simulasi per versi (jalan mulus dan dengan krisis), benih acak 2026. Hasil di `mc.json`.
- `decomp.py`: uji porsi selisih kinerja vs kedekatan yang datang dari produktivitas (5.000 simulasi). Hasil di `decomp.json`.

Jalankan: `python3 mc.py` lalu `python3 decomp.py` (Python 3, tanpa library tambahan).

Rentang parameter dan batasannya dijelaskan di halaman, Ruang mesin bagian 9.
