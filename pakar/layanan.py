# -*- coding: utf-8 -*-
"""Lapisan layanan: menyusun fakta dari formulir, menjalankan mesin, menyiapkan tampilan."""
from . import knowledge as K
from .engine import MesinInferensi
from .graph import bangun_svg

MESIN = MesinInferensi(K.RULES, K.FACTS)
KODE_MASUKAN = {k for k, v in K.FACTS.items() if v["tipe"] == "masukan"} | set(K.KODE_KELUHAN) | set(K.KODE_BAHAYA) | set(K.KODE_KONDISI)


def _saring(daftar, diizinkan):
    return [k for k in dict.fromkeys(daftar or []) if k in diizinkan]


def susun_fakta(kebutuhan=(), keluhan=(), bahaya=(), kondisi=()):
    awal = (_saring(kebutuhan, K.KODE_KEBUTUHAN) + _saring(keluhan, K.KODE_KELUHAN)
            + _saring(bahaya, K.KODE_BAHAYA) + _saring(kondisi, K.KODE_KONDISI))
    if not awal:  # informasi tidak lengkap -> sarankan konsultasi (wawancara C6)
        awal = ["G03"]
    return awal


def _urgensi(hasil):
    return 3 if "U3" in hasil.memori else 2 if "U2" in hasil.memori else 1


def _poin_p06(awal):
    poin = []
    bahaya = [K.FACTS[k]["teks"].lower() for k in awal if k.startswith("D")]
    if bahaya:
        poin.append(("Tanda bahaya yang Anda pilih: %s." % ", ".join(bahaya), "Masukan Anda"))
    alasan = [K.FACTS[k]["teks"].lower() for k in awal if k[0] in "GK" and k in ("G01", "G02", "G03", "K06")]
    if alasan:
        poin.append(("Perlu penilaian individual karena: %s." % ", ".join(alasan), "C6"))
    return poin


def proses(awal):
    hasil = MESIN.jalankan(awal, KODE_MASUKAN)
    urg = _urgensi(hasil)
    kode_p = sorted(k for k in hasil.memori if k in K.KESIMPULAN)
    if urg >= 2 and "P06" in kode_p:
        kode_p.remove("P06")
        kode_p.insert(0, "P06")
    kartu = []
    for kode in kode_p:
        info = K.KESIMPULAN[kode]
        poin = list(info["poin"])
        if kode == "P06":
            poin = _poin_p06(hasil.awal) + poin
        rid = hasil.turunan[kode][0]
        rule = next(r for r in K.RULES if r["id"] == rid)
        kartu.append({"kode": kode, "judul": info["judul"], "ikon": info["ikon"],
                      "rekomendasi": info["rekomendasi"], "poin": poin,
                      "aturan": rid, "jenis": rule["jenis"],
                      "pohon": MESIN.jelaskan(kode, hasil)})
    if urg == 3:
        utama = [k for k in kartu if k["kode"] == "P06"]
        lain = [k for k in kartu if k["kode"] != "P06"]
    else:
        utama, lain = kartu, []
    rules = {r["id"]: r for r in K.RULES}
    langkah = [{
        "siklus": l.siklus, "aturan": l.aturan, "rumus": K.rumus(rules[l.aturan]),
        "jenis": rules[l.aturan]["jenis"],
        "premis": [(p, K.FACTS[p]["pendek"]) for p in l.premis],
        "hasil": (l.hasil, K.FACTS[l.hasil]["pendek"]), "baru": l.baru,
    } for l in hasil.langkah]
    ringkasan = {
        "kebutuhan": [(k, K.FACTS[k]["pendek"]) for k in hasil.awal if k.startswith("F")],
        "keluhan": [(k, K.FACTS[k]["pendek"]) for k in hasil.awal if k.startswith("K")],
        "bahaya": [(k, K.FACTS[k]["pendek"]) for k in hasil.awal if k.startswith("D")],
        "kondisi": [(k, K.FACTS[k]["pendek"]) for k in hasil.awal if k.startswith("G")],
    }
    return {
        "hasil": hasil, "urgensi": urg, "urgensi_info": K.URGENSI[urg],
        "kartu_utama": utama, "kartu_lain": lain, "kartu": kartu,
        "langkah": langkah, "ringkasan": ringkasan,
        "memori_awal": [(k, K.FACTS[k]["teks"]) for k in hasil.awal],
        "graf": bangun_svg(hasil, K.FACTS, K.RULES),
        "kode_kesimpulan": [k["kode"] for k in kartu],
    }


def ringkasan_txt(kode, dibuat, kb_saat_ini, v):
    baris = ["%s — Ringkasan Konsultasi" % K.APP["nama"], "=" * 50,
             "Kode: %s" % kode, "Waktu: %s" % dibuat.replace("T", " "),
             "KB saat ini: %s" % K.KB_SAAT_INI.get(kb_saat_ini, "-"), "",
             "STATUS: %s" % v["urgensi_info"]["judul"], v["urgensi_info"]["teks"], ""]
    for k in v["kartu"]:
        baris.append("[%s] %s (aturan %s)" % (k["kode"], k["judul"], k["aturan"]))
        baris.append("  Rekomendasi: " + k["rekomendasi"])
        for teks, sumber in k["poin"]:
            baris.append("  - " + teks)
        baris.append("")
    baris += ["Catatan: informasi ini edukasi awal, bukan diagnosis dan tidak menggantikan",
              "pemeriksaan oleh bidan atau tenaga kesehatan."]
    return "\n".join(baris)


def hasil_json(v):
    h = v["hasil"]
    return {"fakta_awal": h.awal, "memori_kerja": h.memori, "urgensi": v["urgensi"],
            "kesimpulan": v["kode_kesimpulan"], "siklus": h.jumlah_siklus,
            "langkah": [{"siklus": l.siklus, "aturan": l.aturan, "premis": l.premis,
                         "hasil": l.hasil, "baru": l.baru} for l in h.langkah]}
