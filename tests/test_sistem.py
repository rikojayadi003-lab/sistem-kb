# -*- coding: utf-8 -*-
import os
import re
import tempfile
import unittest

from app import create_app
from pakar import knowledge as K
from pakar import layanan
from pakar.engine import MesinInferensi

M = MesinInferensi(K.RULES, K.FACTS)


def jalan(*fakta):
    return M.jalankan(list(fakta), layanan.KODE_MASUKAN)


class TesEngine(unittest.TestCase):
    def test_aturan_pdf_langsung(self):
        for f, p in [(("F01", "F02"), "P01"), (("F01", "F03"), "P02"), (("F01", "F04"), "P03"),
                     (("F01", "F05"), "P04"), (("F06",), "P05"), (("F07",), "P06"), (("F08",), "P07")]:
            self.assertIn(p, jalan(*f).memori, f)

    def test_premis_tidak_lengkap_tidak_memicu(self):
        self.assertNotIn("P01", jalan("F02").memori[:1])  # F02 saja belum cukup tanpa T01
        self.assertNotIn("P01", jalan("F01").memori)

    def test_turunan_suntik(self):
        h = jalan("F02")
        self.assertIn("F01", h.memori)
        self.assertIn("P01", h.memori)
        self.assertEqual(h.jumlah_siklus, 2)

    def test_iud_bukan_implan(self):
        h = jalan("F04")
        self.assertIn("P03", h.memori)
        self.assertNotIn("P04", h.memori)

    def test_keluhan(self):
        h = jalan("K01")
        self.assertIn("F06", h.memori)
        self.assertIn("P05", h.memori)
        self.assertNotIn("U3", h.memori)

    def test_tanda_bahaya_darurat(self):
        v = layanan.proses(["D04"])
        self.assertEqual(v["urgensi"], 3)
        self.assertIn("P06", v["kode_kesimpulan"])

    def test_riwayat_penyakit_konsultasi(self):
        v = layanan.proses(["F02", "G01"])
        self.assertEqual(v["urgensi"], 2)
        self.assertEqual(v["kode_kesimpulan"][0], "P06")

    def test_kosong_dianggap_info_tidak_lengkap(self):
        awal = layanan.susun_fakta()
        self.assertEqual(awal, ["G03"])
        self.assertEqual(layanan.proses(awal)["urgensi"], 2)

    def test_tanpa_keluhan_urgensi_satu(self):
        self.assertEqual(layanan.proses(["F02"])["urgensi"], 1)

    def test_kesimpulan_tidak_bisa_disuntik(self):
        h = jalan("P06", "U3", "XYZ")
        self.assertEqual(h.awal, [])

    def test_penjelasan(self):
        h = jalan("F02")
        pohon = M.jelaskan("P01", h)
        self.assertEqual(pohon["aturan"], "R01")
        self.assertEqual({a["kode"] for a in pohon["anak"]}, {"F01", "F02"})

    def test_semua_rujukan_aturan_valid(self):
        kode = set(K.FACTS)
        for r in K.RULES:
            self.assertIn(r["then"], kode)
            for p in r["all"] + r["any"]:
                self.assertIn(p, kode, r["id"])


class TesWeb(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.app = create_app(os.path.join(self.tmp.name, "t.db"))
        self.c = self.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_halaman_statis(self):
        for url in ["/", "/konsultasi", "/konsultasi?preset=pil", "/metode", "/pengingat",
                    "/basis-pengetahuan", "/statistik", "/tentang"]:
            r = self.c.get(url)
            self.assertEqual(r.status_code, 200, url)
            self.assertNotIn(b"{{", r.data, url)

    def kirim(self, **data):
        r = self.c.post("/konsultasi", data=data)
        self.assertEqual(r.status_code, 302)
        return r.headers["Location"]

    def test_alur_konsultasi(self):
        lok = self.kirim(kebutuhan=["F02"], kb_saat_ini="suntik")
        r = self.c.get(lok)
        self.assertEqual(r.status_code, 200)
        self.assertIn("Penggunaan KB Suntik".encode(), r.data)
        self.assertIn(b"<svg", r.data)
        t = self.c.get(lok + "/unduh.txt")
        self.assertEqual(t.status_code, 200)
        self.assertIn("KB suntik".encode(), t.data)

    def test_darurat(self):
        lok = self.kirim(bahaya=["D03"], kebutuhan=["F02"])
        r = self.c.get(lok)
        self.assertIn(b"Segera cari pertolongan medis", r.data)
        self.assertIn(b"Informasi umum lainnya", r.data)

    def test_masukan_liar_diabaikan(self):
        lok = self.kirim(kebutuhan=["P06", "U3", "<script>alert(1)</script>"], kb_saat_ini="<x>")
        r = self.c.get(lok)
        self.assertEqual(r.status_code, 200)
        self.assertNotIn(b"alert(1)", r.data)
        self.assertNotIn(b"<x>", r.data)
        # kesimpulan tidak bisa disuntik lewat formulir: hanya G03 (info tidak lengkap) yang aktif
        self.assertIn(b"Info belum lengkap", r.data)
        self.assertNotIn(b"Segera cari pertolongan medis", r.data)

    def test_hasil_tidak_ada(self):
        self.assertEqual(self.c.get("/hasil/abcdefgh").status_code, 404)
        self.assertEqual(self.c.get("/hasil/../etc").status_code, 404)

    def test_statistik_terisi(self):
        self.kirim(kebutuhan=["F03"])
        r = self.c.get("/statistik")
        self.assertIn(b"total konsultasi", r.data)
        self.assertIn(b"Penggunaan Pil KB", r.data)

    def test_api(self):
        r = self.c.post("/api/inferensi", json={"fakta": ["F01", "F02"]})
        self.assertEqual(r.status_code, 200)
        self.assertIn("P01", r.get_json()["kesimpulan"])
        self.assertEqual(self.c.post("/api/inferensi", json={"x": 1}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
