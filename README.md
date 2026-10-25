# Sahabat KB — Sistem Pakar Informasi & Konseling Kontrasepsi

Sistem pakar berbasis web (Python + Flask) dengan metode **forward chaining**, dibangun dari
*Instrumen Akuisisi Pengetahuan Pakar* (wawancara Bidan Lisfebriani, Puskesmas Kutambaru).
Cakupan: KB suntik, pil KB, IUD/spiral, implan, keluhan/efek samping, dan rujukan.

> Sistem memberi **edukasi awal**, bukan diagnosis, dan tidak menentukan metode KB yang cocok
> tanpa penilaian individual oleh bidan atau tenaga kesehatan.

## Cara menjalankan

Butuh Python 3.9+.

- **Windows:** klik dua kali `run.bat`
- **Linux / macOS:** `bash run.sh`
- **Manual:**
  ```
  pip install -r requirements.txt
  python app.py
  ```

Buka http://127.0.0.1:5000

Mode terminal (tanpa web): `python cli.py`
Jalankan tes: `python -m unittest discover -s tests -t .`

## Fitur

| Fitur | Keterangan |
|---|---|
| Konsultasi 4 langkah | Kebutuhan, keluhan, tanda bahaya, kondisi. Ada jalan pintas topik di beranda |
| Mesin forward chaining | Siklus berulang sampai tidak ada aturan baru, dengan trace tiap siklus |
| Fasilitas penjelasan | Tiap kesimpulan punya pohon pembuktian ("Mengapa sistem menyimpulkan ini?") |
| Diagram inferensi | Grafik SVG fakta → aturan → kesimpulan yang dibuat dari proses nyata |
| Pagar pengaman | 3 tingkat urgensi: edukasi umum, konsultasi langsung, darurat |
| Metode KB | Perbandingan 4 metode dan kartu persiapan konsultasi (bisa dicetak) |
| Pengingat kunjungan | Hitung mundur dari tanggal bidan, ekspor `.ics`, data hanya di browser |
| Basis pengetahuan | Semua fakta/aturan beserta status validasi, dengan pencarian |
| Statistik anonim | Topik, urgensi, dan masukan terbanyak |
| Cetak / unduh hasil | Cetak rapi atau unduh `.txt` |
| Tema terang/gelap | Mengikuti pengaturan perangkat, bisa diganti manual |
| API JSON | `POST /api/inferensi` dengan `{"fakta": ["F01","F02"]}` |

## Struktur

```
app.py                 route Flask
cli.py                 mode terminal
pakar/knowledge.py     basis pengetahuan (fakta, aturan, teks rekomendasi)
pakar/engine.py        mesin inferensi + penjelasan
pakar/graph.py         pembuat diagram SVG
pakar/layanan.py       penghubung formulir -> mesin -> tampilan
pakar/db.py            SQLite anonim
templates/ static/     tampilan
tests/                 19 tes (engine + web)
```

## Catatan penting soal validasi pakar

Instrumen menyatakan rancangan aturan harus divalidasi pakar. Saat memetakan PDF ke kode,
ditemukan hal yang perlu Anda ketahui:

1. **Tabel 1 dan Tabel 2 tidak sinkron.** Tabel 1 hanya memuat fakta F01–F06, tetapi Tabel 2
   memakai F01–F08 (R04 memakai F05, R06 memakai F07, R07 memakai F08 yang tidak terdefinisi
   di Tabel 1). Sistem memakai 8 fakta agar R01–R07 berjalan **persis seperti tertulis**:
   F04 = IUD, F05 = implan, F06 = keluhan, F07 = tanda bahaya/penilaian individual,
   F08 = ingin memilih metode. Sebaiknya Tabel 1 di dokumen diperbarui agar sama.
2. **Ekstensi (label `ekstensi`):** aturan T01–T05 dan fakta K/D/G/U ditambahkan dari jawaban
   wawancara (C5, C6) supaya jawaban pengguna bisa dipetakan ke fakta dan batas konsultasi
   berjalan. Isinya bersumber dari pakar, tetapi **susunan aturannya belum divalidasi**.
   Tampil dengan label kuning di aplikasi.
3. Semua teks edukasi hanya memakai isi jawaban pakar. Tidak ada angka klinis tambahan
   (mis. batas hari terlambat suntik) karena pakar tidak menyebutkannya.
4. Daftar keluhan (perdarahan tidak teratur, dll.) di wawancara disebut untuk KB suntik;
   di sistem dipakai sebagai keluhan umum.

## Menambah atau mengubah aturan

Semua ada di `pakar/knowledge.py`. Contoh menambah fakta dan aturan:

```python
FACTS["F09"] = _f("Pengguna bertanya tentang ...", "Tanya ...", "ekstensi")
RULES.append(_r("R08", "P08", ["F01", "F09"], jenis="ekstensi"))
```

Engine tidak perlu diubah. Aturan baru harus divalidasi pakar sebelum dipakai nyata.

## Privasi

Konsultasi disimpan di `data/konsultasi.db` tanpa nama, kontak, atau IP. Pengingat kunjungan
hanya di `localStorage` browser pengguna.
