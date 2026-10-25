# -*- coding: utf-8 -*-
"""Mesin inferensi Forward Chaining (data-driven) dengan fasilitas penjelasan."""
from dataclasses import dataclass


@dataclass
class Langkah:
    siklus: int
    aturan: str
    premis: list
    hasil: str
    baru: bool


@dataclass
class Hasil:
    awal: list
    memori: list
    langkah: list
    turunan: dict      # kode -> (id_aturan, premis_terpakai, siklus)
    jumlah_siklus: int


class MesinInferensi:
    def __init__(self, rules, facts):
        self.rules = rules
        self.facts = facts

    @staticmethod
    def _cocok(rule, memori):
        """Kembalikan daftar premis terpakai bila aturan terpenuhi, selain itu None."""
        semua = rule.get("all", [])
        salah = rule.get("any", [])
        if semua and not all(f in memori for f in semua):
            return None
        ada = [f for f in salah if f in memori]
        if salah and not ada:
            return None
        return list(semua) + ada

    def jalankan(self, fakta_awal, diizinkan=None):
        awal = []
        for k in fakta_awal:
            if k in self.facts and k not in awal and (diizinkan is None or k in diizinkan):
                awal.append(k)
        memori = list(awal)
        tahu = set(awal)
        terpicu = set()
        langkah, turunan = [], {}
        siklus = 0
        while True:
            siklus += 1
            snapshot = set(tahu)
            ada_api = False
            for r in self.rules:
                if r["id"] in terpicu or r["then"] in snapshot:
                    continue
                dipakai = self._cocok(r, snapshot)
                if dipakai is None:
                    continue
                terpicu.add(r["id"])
                ada_api = True
                baru = r["then"] not in tahu
                langkah.append(Langkah(siklus, r["id"], dipakai, r["then"], baru))
                if baru:
                    tahu.add(r["then"])
                    memori.append(r["then"])
                    turunan[r["then"]] = (r["id"], dipakai, siklus)
            if not ada_api:
                siklus -= 1
                break
        return Hasil(awal, memori, langkah, turunan, siklus)

    def jelaskan(self, kode, hasil):
        """Pohon pembuktian: dari kesimpulan turun ke fakta masukan."""
        node = {"kode": kode, "teks": self.facts[kode]["teks"], "aturan": None, "anak": []}
        if kode in hasil.turunan:
            rid, dipakai, _ = hasil.turunan[kode]
            node["aturan"] = rid
            node["anak"] = [self.jelaskan(p, hasil) for p in dipakai]
        return node
