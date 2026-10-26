# -*- coding: utf-8 -*-
"""Sahabat KB — Sistem Pakar Informasi & Konseling Kontrasepsi (Forward Chaining, Flask)."""
import os
import re

from flask import (Flask, Response, abort, jsonify, redirect, render_template,
                   request, url_for)

from pakar import db, layanan
from pakar import knowledge as K

NAV = [("index", "Beranda"), ("konsultasi", "Konsultasi"), ("metode", "Metode KB"),
       ("pengingat", "Pengingat"), ("basis", "Basis Pengetahuan"),
       ("statistik", "Statistik"), ("tentang", "Tentang")]


def create_app(db_path=None):
    app = Flask(__name__)
    base = os.path.dirname(os.path.abspath(__file__))
    app.config["DB_PATH"] = db_path or os.path.join(base, "data", "konsultasi.db")
    db.init(app.config["DB_PATH"])

    @app.context_processor
    def konteks():
        return {"APP": K.APP, "NAV": NAV, "K": K}

    @app.after_request
    def header(resp):
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "same-origin"
        return resp

    @app.route("/")
    def index():
        return render_template(
            "index.html", presets=K.PRESETS,
            jml_aturan=len([r for r in K.RULES if r["jenis"] != "ekstensi"]),
            jml_fakta=len([f for f in K.FACTS.values() if f["tipe"] == "masukan"]))

    @app.route("/konsultasi", methods=["GET", "POST"])
    def konsultasi():
        if request.method == "POST":
            awal = layanan.susun_fakta(
                request.form.getlist("kebutuhan"), request.form.getlist("keluhan"),
                request.form.getlist("bahaya"), request.form.getlist("kondisi"))
            kb = request.form.get("kb_saat_ini", "")
            kb = kb if kb in K.KB_SAAT_INI else ""
            v = layanan.proses(awal)
            kode = db.simpan(app.config["DB_PATH"], v["hasil"].awal, kb,
                             v["kode_kesimpulan"], v["urgensi"])
            return redirect(url_for("hasil", kode=kode))
        preset = K.PRESETS.get(request.args.get("preset", ""), {})
        return render_template("konsultasi.html", pre=preset.get("kebutuhan", []),
                               mulai=preset.get("mulai", 1))

    def _muat(kode):
        if not re.fullmatch(r"[A-Za-z0-9_-]{6,16}", kode):
            abort(404)
        rec = db.ambil(app.config["DB_PATH"], kode)
        if not rec:
            abort(404)
        return rec, layanan.proses(rec["fakta"])

    @app.route("/hasil/<kode>")
    def hasil(kode):
        rec, v = _muat(kode)
        return render_template("hasil.html", kode=kode, rec=rec, v=v,
                               kb=K.KB_SAAT_INI.get(rec["kb_saat_ini"], ""))

    @app.route("/hasil/<kode>/unduh.txt")
    def unduh_txt(kode):
        rec, v = _muat(kode)
        teks = layanan.ringkasan_txt(kode, rec["dibuat"], rec["kb_saat_ini"], v)
        return Response(teks, mimetype="text/plain; charset=utf-8",
                        headers={"Content-Disposition": "attachment; filename=konsultasi-%s.txt" % kode})

    @app.route("/metode")
    def metode():
        return render_template("metode.html")

    @app.route("/pengingat")
    def pengingat():
        return render_template("pengingat.html")

    @app.route("/basis-pengetahuan")
    def basis():
        rules = [dict(r, rumus=K.rumus(r)) for r in K.RULES]
        return render_template("basis.html", rules=rules)

    @app.route("/statistik")
    def statistik():
        return render_template("statistik.html", s=db.statistik(app.config["DB_PATH"]))

    @app.route("/tentang")
    def tentang():
        return render_template("tentang.html")

    @app.route("/api/inferensi", methods=["POST"])
    def api_inferensi():
        data = request.get_json(silent=True) or {}
        fakta = data.get("fakta")
        if not isinstance(fakta, list):
            return jsonify(galat="Kirim JSON: {\"fakta\": [\"F01\", \"F02\"]}"), 400
        fakta = [f for f in fakta if isinstance(f, str)]
        return jsonify(layanan.hasil_json(layanan.proses(fakta)))

    @app.errorhandler(404)
    def tidak_ada(_):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    print("\n  %s berjalan di http://127.0.0.1:%d  (Ctrl+C untuk berhenti)\n" % (K.APP["nama"], port))
    app.run(host="127.0.0.1", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
