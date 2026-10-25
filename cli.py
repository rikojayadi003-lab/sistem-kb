# -*- coding: utf-8 -*-
"""Mode terminal: coba mesin forward chaining tanpa web.  Jalankan: python cli.py"""
from pakar import knowledge as K
from pakar import layanan


def tanya(judul, opsi):
    print("\n" + judul)
    dipilih = []
    for kode, teks in opsi:
        if input("  [%s] %s? (y/N) " % (kode, teks)).strip().lower() == "y":
            dipilih.append(kode)
    return dipilih


def main():
    print("== %s (mode terminal) ==" % K.APP["nama"])
    kebutuhan = tanya("Apa yang ingin Anda ketahui?", [(k, n) for k, _, n, _ in K.KEBUTUHAN])
    keluhan = tanya("Keluhan setelah memakai KB?", K.KELUHAN)
    bahaya = tanya("Tanda bahaya sekarang?", K.BAHAYA)
    kondisi = tanya("Kondisi Anda?", K.KONDISI)

    awal = layanan.susun_fakta(kebutuhan, keluhan, bahaya, kondisi)
    v = layanan.proses(awal)

    print("\nMemori kerja awal:", ", ".join(awal))
    print("\n--- Jejak inferensi ---")
    for l in v["langkah"]:
        print("Siklus %d | %s | %s  =>  %s%s" % (
            l["siklus"], l["aturan"], l["rumus"], l["hasil"][0], "" if l["baru"] else " (sudah ada)"))

    print("\n=== %s ===\n%s" % (v["urgensi_info"]["judul"].upper(), v["urgensi_info"]["teks"]))
    for k in v["kartu"]:
        print("\n[%s] %s" % (k["kode"], k["judul"]))
        print("  " + k["rekomendasi"])
        for teks, _ in k["poin"]:
            print("  - " + teks)
    print("\nCatatan: edukasi awal, bukan diagnosis.")


if __name__ == "__main__":
    main()
