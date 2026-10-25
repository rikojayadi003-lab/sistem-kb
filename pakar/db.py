# -*- coding: utf-8 -*-
"""Penyimpanan konsultasi anonim (tanpa nama, tanpa IP, tanpa teks bebas)."""
import json
import os
import secrets
import sqlite3
from contextlib import closing
from datetime import datetime

SKEMA = """CREATE TABLE IF NOT EXISTS konsultasi (
    id TEXT PRIMARY KEY,
    dibuat TEXT NOT NULL,
    fakta TEXT NOT NULL,
    kb_saat_ini TEXT,
    kesimpulan TEXT NOT NULL,
    urgensi INTEGER NOT NULL
)"""


def _koneksi(path):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


def init(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with closing(_koneksi(path)) as con:
        con.execute(SKEMA)
        con.commit()


def simpan(path, fakta, kb_saat_ini, kesimpulan, urgensi):
    kode = secrets.token_urlsafe(6)
    with closing(_koneksi(path)) as con:
        con.execute(
            "INSERT INTO konsultasi VALUES (?,?,?,?,?,?)",
            (kode, datetime.now().isoformat(timespec="seconds"), json.dumps(fakta),
             kb_saat_ini, json.dumps(kesimpulan), urgensi),
        )
        con.commit()
    return kode


def ambil(path, kode):
    with closing(_koneksi(path)) as con:
        row = con.execute("SELECT * FROM konsultasi WHERE id=?", (kode,)).fetchone()
    if not row:
        return None
    return {"id": row["id"], "dibuat": row["dibuat"], "fakta": json.loads(row["fakta"]),
            "kb_saat_ini": row["kb_saat_ini"], "kesimpulan": json.loads(row["kesimpulan"]),
            "urgensi": row["urgensi"]}


def statistik(path):
    with closing(_koneksi(path)) as con:
        rows = con.execute("SELECT dibuat, fakta, kesimpulan, urgensi FROM konsultasi").fetchall()
    hari_ini = datetime.now().date().isoformat()
    total = len(rows)
    urg = {1: 0, 2: 0, 3: 0}
    simpulan, masukan = {}, {}
    hari = 0
    for r in rows:
        urg[r["urgensi"]] = urg.get(r["urgensi"], 0) + 1
        if r["dibuat"].startswith(hari_ini):
            hari += 1
        for k in json.loads(r["kesimpulan"]):
            simpulan[k] = simpulan.get(k, 0) + 1
        for k in json.loads(r["fakta"]):
            masukan[k] = masukan.get(k, 0) + 1
    return {
        "total": total, "hari_ini": hari, "urgensi": urg,
        "kesimpulan": sorted(simpulan.items(), key=lambda x: -x[1]),
        "masukan": sorted(masukan.items(), key=lambda x: -x[1])[:8],
    }
