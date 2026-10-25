# -*- coding: utf-8 -*-
"""
Basis pengetahuan Sistem Pakar Informasi & Konseling Kontrasepsi.

Sumber: Instrumen Akuisisi Pengetahuan Pakar (wawancara dengan Bidan Lisfebriani,
Puskesmas Kutambaru) beserta rancangan fakta & aturan Forward Chaining (Bagian D)
yang sudah ditandai "Sesuai" pada Bagian E.

Status setiap item:
  tervalidasi  -> diambil apa adanya dari instrumen pakar
  penyesuaian  -> kode fakta diselaraskan agar cocok dengan Tabel 2 (lihat README)
  ekstensi     -> ditambahkan pembuat sistem dari jawaban wawancara; WAJIB divalidasi ulang pakar
"""

APP = {
    "nama": "Sahabat KB",
    "subjudul": "Sistem Pakar Informasi & Konseling Kontrasepsi",
    "versi": "1.0.0",
}

SUMBER = {
    "pakar": "Bidan Lisfebriani",
    "lokasi": "Puskesmas Kutambaru",
    "tanggal": "12/10/2026",
    "knowledge_engineer": "Wina Jeninta br Sitepu",
    "institusi": "Teknik Informatika, STMIK Methodist Binjai",
}

VALIDASI = [
    "Fakta dan pertanyaan sudah sesuai dengan topik KB.",
    "Aturan IF–THEN sesuai untuk edukasi awal yang aman.",
    "Batas konsultasi dan rujukan sudah tepat.",
]

CATATAN_PENYESUAIAN = [
    "Tabel 1 (D.1) hanya memuat F01–F06, sedangkan Tabel 2 memakai F01–F08 "
    "(R04 memakai F05, R06 memakai F07, R07 memakai F08). Sistem memakai 8 fakta "
    "agar aturan R01–R07 dapat dijalankan persis seperti tertulis.",
    "F04 pada Tabel 1 (IUD/spiral atau implan) dipisah menjadi F04 (IUD/spiral) dan "
    "F05 (implan); keluhan menjadi F06; tanda bahaya/penilaian individual menjadi F07; "
    "F08 (ingin memilih metode) ditambahkan berdasarkan R07/P07.",
    "Aturan turunan T01–T05 serta fakta K/D/G/U ditambahkan dari jawaban wawancara "
    "(Bagian C no. 5 dan 6) agar masukan pengguna dapat dipetakan ke fakta dan batas "
    "konsultasi dapat dijalankan. Bagian ini perlu divalidasi ulang oleh pakar.",
]


def _f(teks, pendek, jenis, tipe="masukan", sumber=""):
    return {"teks": teks, "pendek": pendek, "jenis": jenis, "tipe": tipe, "sumber": sumber}


# tipe: masukan (boleh diberikan pengguna), kesimpulan, urgensi
FACTS = {
    "F01": _f("Pengguna membutuhkan informasi umum mengenai metode kontrasepsi.", "Butuh info umum KB", "tervalidasi", sumber="Tabel 1"),
    "F02": _f("Pengguna bertanya tentang KB suntik atau jadwal suntik.", "Tanya KB suntik", "tervalidasi", sumber="Tabel 1"),
    "F03": _f("Pengguna bertanya tentang pil KB atau lupa minum pil.", "Tanya pil KB", "tervalidasi", sumber="Tabel 1"),
    "F04": _f("Pengguna bertanya tentang IUD/spiral.", "Tanya IUD/spiral", "penyesuaian", sumber="Tabel 1 (F04), dipisah"),
    "F05": _f("Pengguna bertanya tentang implan.", "Tanya implan", "penyesuaian", sumber="Tabel 2 (R04)"),
    "F06": _f("Pengguna melaporkan keluhan setelah menggunakan kontrasepsi.", "Ada keluhan", "penyesuaian", sumber="Tabel 1 (F05), Tabel 2 (R05)"),
    "F07": _f("Pengguna menyampaikan tanda bahaya atau membutuhkan penilaian individual.", "Tanda bahaya / perlu nilai individual", "penyesuaian", sumber="Tabel 1 (F06), Tabel 2 (R06)"),
    "F08": _f("Pengguna ingin memilih metode kontrasepsi.", "Ingin memilih metode", "penyesuaian", sumber="Tabel 2 (R07)"),
    # keluhan (C5)
    "K01": _f("Perdarahan tidak teratur", "Perdarahan tidak teratur", "ekstensi", sumber="C5"),
    "K02": _f("Menstruasi tidak datang", "Menstruasi tidak datang", "ekstensi", sumber="C5"),
    "K03": _f("Sakit kepala", "Sakit kepala", "ekstensi", sumber="C5"),
    "K04": _f("Perubahan berat badan", "Perubahan berat badan", "ekstensi", sumber="C5"),
    "K05": _f("Keluhan lain yang mengganggu", "Keluhan lain mengganggu", "ekstensi", sumber="C5"),
    "K06": _f("Keluhan terasa berat atau mengkhawatirkan", "Keluhan berat/mengkhawatirkan", "ekstensi", sumber="C6"),
    # tanda bahaya (C5)
    "D01": _f("Perdarahan sangat banyak", "Perdarahan sangat banyak", "ekstensi", sumber="C5"),
    "D02": _f("Nyeri perut hebat", "Nyeri perut hebat", "ekstensi", sumber="C5"),
    "D03": _f("Sesak napas", "Sesak napas", "ekstensi", sumber="C5"),
    "D04": _f("Nyeri dada", "Nyeri dada", "ekstensi", sumber="C5"),
    "D05": _f("Sakit kepala hebat yang muncul mendadak", "Sakit kepala hebat mendadak", "ekstensi", sumber="C5"),
    # kondisi (C6)
    "G01": _f("Memiliki riwayat penyakit tertentu", "Riwayat penyakit tertentu", "ekstensi", sumber="C6"),
    "G02": _f("Efek samping berkepanjangan", "Efek samping berkepanjangan", "ekstensi", sumber="C6"),
    "G03": _f("Informasi belum lengkap atau ragu, perlu dinilai langsung", "Info belum lengkap / ragu", "ekstensi", sumber="C6"),
    # kesimpulan
    "P01": _f("Penggunaan KB Suntik", "Penggunaan KB Suntik", "tervalidasi", "kesimpulan", "Tabel 2"),
    "P02": _f("Penggunaan Pil KB", "Penggunaan Pil KB", "tervalidasi", "kesimpulan", "Tabel 2"),
    "P03": _f("Pemasangan atau Pelepasan IUD", "Pasang/Lepas IUD", "tervalidasi", "kesimpulan", "Tabel 2"),
    "P04": _f("Pemasangan atau Pelepasan Implan", "Pasang/Lepas Implan", "tervalidasi", "kesimpulan", "Tabel 2"),
    "P05": _f("Keluhan atau Efek Samping KB", "Keluhan / Efek Samping", "tervalidasi", "kesimpulan", "Tabel 2"),
    "P06": _f("Tanda Bahaya", "Tanda Bahaya", "tervalidasi", "kesimpulan", "Tabel 2"),
    "P07": _f("Pemilihan Metode Kontrasepsi", "Pemilihan Metode", "tervalidasi", "kesimpulan", "Tabel 2"),
    # urgensi
    "U2": _f("Perlu konsultasi langsung dengan bidan atau tenaga kesehatan", "Konsultasi langsung", "ekstensi", "urgensi", "C6"),
    "U3": _f("Perlu pertolongan medis segera", "Pertolongan segera", "ekstensi", "urgensi", "C5"),
}


def _r(rid, then, all_=None, any_=None, jenis="tervalidasi", sumber="Tabel 2", catatan=""):
    return {"id": rid, "then": then, "all": all_ or [], "any": any_ or [],
            "jenis": jenis, "sumber": sumber, "catatan": catatan}


RULES = [
    _r("R01", "P01", ["F01", "F02"]),
    _r("R02", "P02", ["F01", "F03"]),
    _r("R03", "P03", ["F01", "F04"], catatan="Pada tabel asli: F01 AND F04 (IUD)."),
    _r("R04", "P04", ["F01", "F05"], catatan="Pada tabel asli: F01 AND F05 (implan)."),
    _r("R05", "P05", ["F06"]),
    _r("R06", "P06", ["F07"]),
    _r("R07", "P07", ["F08"]),
    # aturan turunan (ekstensi, perlu validasi pakar)
    _r("T01", "F01", any_=["F02", "F03", "F04", "F05", "F08"], jenis="ekstensi", sumber="B1, C1",
       catatan="Bertanya tentang metode tertentu berarti membutuhkan informasi KB."),
    _r("T02", "F06", any_=["K01", "K02", "K03", "K04", "K05", "K06"], jenis="ekstensi", sumber="C5"),
    _r("T03", "F07", any_=["D01", "D02", "D03", "D04", "D05", "G01", "G02", "G03", "K06"], jenis="ekstensi", sumber="C5, C6"),
    _r("T04", "U3", any_=["D01", "D02", "D03", "D04", "D05"], jenis="ekstensi", sumber="C5"),
    _r("T05", "U2", any_=["G01", "G02", "G03", "K06"], jenis="ekstensi", sumber="C6"),
]


def rumus(rule):
    if rule["all"]:
        kiri = " AND ".join(rule["all"])
    else:
        kiri = "(" + " OR ".join(rule["any"]) + ")"
    return "IF %s THEN %s" % (kiri, rule["then"])


# ---------------------------------------------------------------- Kesimpulan
KESIMPULAN = {
    "P01": {
        "judul": "Penggunaan KB Suntik", "ikon": "💉",
        "rekomendasi": "Memberikan edukasi mengenai jadwal suntik, penggunaan, dan keterlambatan suntik sesuai jenis KB suntik yang digunakan.",
        "poin": [
            ("KB suntik digunakan secara berkala, jadi jadwal kunjungan ulang perlu diperhatikan.", "B1, C1"),
            ("Jika terlambat suntik, ikuti petunjuk sesuai jenis KB suntik yang digunakan.", "C3"),
            ("Jika ragu atau jadwal sudah terlewat, segera konsultasi dengan bidan atau tenaga kesehatan agar mendapat arahan yang tepat.", "C3"),
            ("Keluhan yang perlu dikonsultasikan: perdarahan tidak teratur, menstruasi tidak datang, sakit kepala, perubahan berat badan, atau keluhan lain yang mengganggu.", "C5"),
        ],
    },
    "P02": {
        "judul": "Penggunaan Pil KB", "ikon": "💊",
        "rekomendasi": "Memberikan edukasi mengenai aturan minum pil KB dan langkah yang perlu diperhatikan apabila lupa minum pil.",
        "poin": [
            ("Pil KB digunakan secara berkala, sesuai petunjuk jenis pil yang digunakan.", "C1"),
            ("Jika lupa minum pil, ikuti petunjuk sesuai jenis pil KB yang digunakan.", "C3"),
            ("Jika ragu atau sudah melewati jadwal, segera konsultasi dengan bidan atau tenaga kesehatan agar mendapat arahan yang tepat.", "C3"),
        ],
    },
    "P03": {
        "judul": "Pemasangan atau Pelepasan IUD", "ikon": "🩺",
        "rekomendasi": "Memberikan informasi mengenai IUD serta mengarahkan pemasangan dan pelepasan kepada tenaga kesehatan yang berwenang.",
        "poin": [
            ("IUD/spiral dapat digunakan dalam jangka panjang.", "C1"),
            ("Sebelum pemasangan atau pelepasan, konsultasikan prosedur, manfaat, risiko, dan kemungkinan efek sampingnya.", "C4"),
            ("Pemasangan dan pelepasan harus dilakukan oleh tenaga kesehatan yang berwenang dan terlatih.", "C4"),
        ],
    },
    "P04": {
        "judul": "Pemasangan atau Pelepasan Implan", "ikon": "🩹",
        "rekomendasi": "Memberikan informasi mengenai implan serta mengarahkan pemasangan dan pelepasan kepada tenaga kesehatan yang berwenang.",
        "poin": [
            ("Implan dapat digunakan dalam jangka panjang.", "C1"),
            ("Sebelum pemasangan atau pelepasan, konsultasikan prosedur, manfaat, risiko, dan kemungkinan efek sampingnya.", "C4"),
            ("Pemasangan dan pelepasan harus dilakukan oleh tenaga kesehatan yang berwenang dan terlatih.", "C4"),
        ],
    },
    "P05": {
        "judul": "Keluhan atau Efek Samping KB", "ikon": "🗒️",
        "rekomendasi": "Memberikan informasi awal mengenai keluhan dan mengarahkan pengguna untuk berkonsultasi dengan tenaga kesehatan sesuai kondisi yang dialami.",
        "poin": [
            ("Keluhan seperti perdarahan tidak teratur, menstruasi tidak datang, sakit kepala, atau perubahan berat badan perlu dikonsultasikan kepada tenaga kesehatan.", "C5"),
            ("Edukasi umum membantu memahami efek samping, tetapi penyebab keluhan hanya dapat ditentukan lewat pemeriksaan langsung.", "C5"),
            ("Sistem ini tidak menentukan penyebab keluhan dan tidak memberi diagnosis.", "C6"),
        ],
    },
    "P06": {
        "judul": "Tanda Bahaya dan Penilaian Individual", "ikon": "🚨",
        "rekomendasi": "Mengarahkan pengguna untuk segera memperoleh pemeriksaan medis sesuai tingkat urgensi. Sistem tidak menetapkan diagnosis secara otomatis.",
        "poin": [
            ("Pertolongan segera diperlukan bila terjadi perdarahan sangat banyak, nyeri perut hebat, sesak napas, nyeri dada, atau sakit kepala hebat yang muncul mendadak.", "C5"),
            ("Pemeriksaan langsung diperlukan untuk menentukan penyebab keluhan dan penanganan yang tepat.", "C5"),
        ],
    },
    "P07": {
        "judul": "Pemilihan Metode Kontrasepsi", "ikon": "⚖️",
        "rekomendasi": "Memberikan informasi umum mengenai pilihan metode kontrasepsi dan menyarankan konsultasi dengan tenaga kesehatan sesuai kondisi serta kebutuhan pengguna.",
        "poin": [
            ("Pilihan KB disesuaikan dengan kondisi kesehatan, kebutuhan, dan kenyamanan ibu.", "B2"),
            ("KB suntik dan pil digunakan secara berkala; IUD dan implan dapat digunakan jangka panjang.", "C1"),
            ("Setiap metode memiliki manfaat dan efek samping yang berbeda.", "C1"),
            ("Sistem tidak menentukan metode yang cocok untuk Anda; diskusikan dengan bidan atau tenaga kesehatan.", "C6"),
        ],
    },
}

URGENSI = {
    3: {"label": "Darurat", "kelas": "darurat", "ikon": "🚨",
        "judul": "Segera cari pertolongan medis",
        "teks": "Tanda yang Anda pilih memerlukan pertolongan medis segera. Datangi fasilitas kesehatan atau IGD terdekat, atau hubungi 112. Sistem ini tidak menegakkan diagnosis."},
    2: {"label": "Konsultasi langsung", "kelas": "waspada", "ikon": "🩺",
        "judul": "Disarankan konsultasi langsung dengan bidan atau tenaga kesehatan",
        "teks": "Untuk kondisi seperti ini diperlukan penilaian individual. Sistem tidak memberi kesimpulan otomatis tentang kesesuaian metode KB. Informasi di bawah hanya edukasi umum."},
    1: {"label": "Edukasi umum", "kelas": "aman", "ikon": "📘",
        "judul": "Edukasi umum",
        "teks": "Dari jawaban Anda, tidak ada tanda bahaya atau kondisi yang memicu konsultasi langsung. Informasi di bawah adalah edukasi umum, bukan penilaian individual."},
}

# ---------------------------------------------------------------- Formulir
KEBUTUHAN = [
    ("F01", "📘", "Informasi umum KB", "Gambaran umum metode kontrasepsi"),
    ("F02", "💉", "KB suntik", "Jadwal suntik, penggunaan, atau terlambat suntik"),
    ("F03", "💊", "Pil KB", "Aturan minum atau lupa minum pil"),
    ("F04", "🩺", "IUD / spiral", "Pemasangan atau pelepasan IUD"),
    ("F05", "🩹", "Implan", "Pemasangan atau pelepasan implan"),
    ("F08", "⚖️", "Memilih metode", "Bingung memilih metode yang sesuai"),
]
KELUHAN = [(k, FACTS[k]["teks"]) for k in ("K01", "K02", "K03", "K04", "K05", "K06")]
BAHAYA = [(k, FACTS[k]["teks"]) for k in ("D01", "D02", "D03", "D04", "D05")]
KONDISI = [
    ("G01", "Saya punya riwayat penyakit tertentu"),
    ("G02", "Efek samping yang saya alami berkepanjangan"),
    ("G03", "Saya ragu atau informasi saya belum lengkap, ingin dinilai langsung"),
]
KODE_KEBUTUHAN = [x[0] for x in KEBUTUHAN]
KODE_KELUHAN = [x[0] for x in KELUHAN]
KODE_BAHAYA = [x[0] for x in BAHAYA]
KODE_KONDISI = [x[0] for x in KONDISI]

KB_SAAT_INI = {
    "tidak": "Tidak sedang menggunakan KB",
    "suntik": "KB suntik",
    "pil": "Pil KB",
    "iud": "IUD / spiral",
    "implan": "Implan",
    "lain": "Metode lain",
    "ragu": "Tidak yakin",
}

PRESETS = {
    "suntik": {"judul": "Terlambat suntik", "kebutuhan": ["F02"], "mulai": 1},
    "pil": {"judul": "Lupa minum pil", "kebutuhan": ["F03"], "mulai": 1},
    "pasang": {"judul": "Pasang atau lepas IUD / implan", "kebutuhan": ["F04", "F05"], "mulai": 1},
    "keluhan": {"judul": "Ada keluhan setelah KB", "kebutuhan": [], "mulai": 2},
    "pilih": {"judul": "Bingung memilih KB", "kebutuhan": ["F08"], "mulai": 1},
}

# ---------------------------------------------------------------- Halaman metode
METODE = [
    {"ikon": "💉", "nama": "KB suntik", "pola": "Berkala, mengikuti jadwal kunjungan ulang",
     "perhatian": "Perhatikan jadwal suntik. Jika terlambat, ikuti petunjuk sesuai jenis KB suntik yang digunakan.",
     "konsul": "Perdarahan tidak teratur, menstruasi tidak datang, sakit kepala, perubahan berat badan, atau keluhan lain yang mengganggu."},
    {"ikon": "💊", "nama": "Pil KB", "pola": "Berkala, diminum sesuai petunjuk jenis pil",
     "perhatian": "Jika lupa minum pil, ikuti petunjuk sesuai jenis pil yang digunakan.",
     "konsul": "Lupa minum pil, ragu, atau sudah melewati jadwal; keluhan lain yang mengganggu."},
    {"ikon": "🩺", "nama": "IUD / spiral", "pola": "Jangka panjang",
     "perhatian": "Pemasangan dan pelepasan dilakukan oleh tenaga kesehatan yang berwenang dan terlatih.",
     "konsul": "Sebelum tindakan: prosedur, manfaat, risiko, dan kemungkinan efek samping."},
    {"ikon": "🩹", "nama": "Implan", "pola": "Jangka panjang",
     "perhatian": "Pemasangan dan pelepasan dilakukan oleh tenaga kesehatan yang berwenang dan terlatih.",
     "konsul": "Sebelum tindakan: prosedur, manfaat, risiko, dan kemungkinan efek samping."},
]

PERSIAPAN = [
    "Kebutuhan saya: apa yang ingin saya tanyakan atau capai",
    "Kondisi kesehatan saya, termasuk riwayat penyakit",
    "KB yang sedang saya gunakan",
    "Keluhan atau kekhawatiran saya",
]

TANGGAL_FORMAT_NAMA = {}
