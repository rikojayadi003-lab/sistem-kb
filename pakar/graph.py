# -*- coding: utf-8 -*-
"""Membuat diagram jaringan inferensi (fakta -> aturan -> kesimpulan) sebagai SVG."""
import html
from markupsafe import Markup

LEBAR, TINGGI, JARAK_X, JARAK_Y, MARGIN = 190, 46, 64, 14, 12


def _potong(teks, n=27):
    return teks if len(teks) <= n else teks[: n - 1] + "…"


def bangun_svg(hasil, facts, rules):
    rule_by_id = {r["id"]: r for r in rules}
    node = {}   # kode -> dict
    kolom = {}  # kol -> [kode]

    def tambah(kode, kol, kelas, baris1, baris2, judul):
        if kode in node:
            return
        node[kode] = {"kol": kol, "kelas": kelas, "b1": baris1, "b2": baris2, "judul": judul}
        kolom.setdefault(kol, []).append(kode)

    dipakai = set()
    for l in hasil.langkah:
        dipakai.update(l.premis)
    for kode in hasil.awal:
        if kode in dipakai:
            tambah(kode, 0, "n-fakta", kode, _potong(facts[kode]["pendek"]), facts[kode]["teks"])
    for l in hasil.langkah:
        r = rule_by_id[l.aturan]
        kls = "n-aturan" + (" ekstensi" if r["jenis"] == "ekstensi" else "")
        tambah(l.aturan, 2 * l.siklus - 1, kls, l.aturan, "→ " + l.hasil, "Aturan %s" % l.aturan)
        if l.baru:
            f = facts[l.hasil]
            if f["tipe"] == "kesimpulan":
                kls = "n-simpul"
            elif l.hasil == "U3":
                kls = "n-bahaya"
            elif l.hasil == "U2":
                kls = "n-waspada"
            else:
                kls = "n-turunan"
            tambah(l.hasil, 2 * l.siklus, kls, l.hasil, _potong(f["pendek"]), f["teks"])

    if not node:
        return Markup("")

    jml_kol = max(k["kol"] for k in node.values()) + 1
    maks = max(len(v) for v in kolom.values())
    tinggi_total = 2 * MARGIN + maks * TINGGI + (maks - 1) * JARAK_Y
    lebar_total = 2 * MARGIN + jml_kol * LEBAR + (jml_kol - 1) * JARAK_X

    for kol, daftar in kolom.items():
        tinggi_kol = len(daftar) * TINGGI + (len(daftar) - 1) * JARAK_Y
        y0 = (tinggi_total - tinggi_kol) / 2
        for i, kode in enumerate(daftar):
            node[kode]["x"] = MARGIN + kol * (LEBAR + JARAK_X)
            node[kode]["y"] = y0 + i * (TINGGI + JARAK_Y)

    garis = []
    for l in hasil.langkah:
        tujuan = [(p, l.aturan) for p in l.premis if p in node] + [(l.aturan, l.hasil)]
        for a, b in tujuan:
            if a not in node or b not in node:
                continue
            x1 = node[a]["x"] + LEBAR
            y1 = node[a]["y"] + TINGGI / 2
            x2 = node[b]["x"]
            y2 = node[b]["y"] + TINGGI / 2
            dx = (x2 - x1) / 2
            garis.append(
                '<path class="garis" d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" marker-end="url(#panah)"/>'
                % (x1, y1, x1 + dx, y1, x2 - dx, y2, x2, y2)
            )

    kotak = []
    for kode, n in node.items():
        kotak.append(
            '<g class="node %s" transform="translate(%.1f %.1f)"><title>%s</title>'
            '<rect width="%d" height="%d" rx="10"/>'
            '<text x="12" y="19" class="t1">%s</text><text x="12" y="35" class="t2">%s</text></g>'
            % (n["kelas"], n["x"], n["y"], html.escape(n["judul"]), LEBAR, TINGGI,
               html.escape(n["b1"]), html.escape(n["b2"]))
        )

    svg = (
        '<svg class="graf" viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
        'aria-label="Diagram jaringan inferensi forward chaining">'
        '<defs><marker id="panah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ujung"/></marker></defs>%s%s</svg>'
        % (lebar_total, tinggi_total, lebar_total, tinggi_total, "".join(garis), "".join(kotak))
    )
    return Markup(svg)
