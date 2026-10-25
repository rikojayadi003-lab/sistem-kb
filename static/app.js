(function () {
  'use strict';
  document.documentElement.classList.add('js');

  /* ---- tema & menu ---- */
  var tema = document.getElementById('tema-tombol');
  if (tema) tema.addEventListener('click', function () {
    var t = document.documentElement.dataset.tema === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.tema = t;
    try { localStorage.setItem('tema', t); } catch (e) {}
  });
  var mt = document.getElementById('menu-tombol'), menu = document.getElementById('menu');
  if (mt && menu) mt.addEventListener('click', function () {
    var buka = menu.classList.toggle('buka');
    mt.setAttribute('aria-expanded', buka ? 'true' : 'false');
  });

  document.querySelectorAll('[data-cetak]').forEach(function (b) {
    b.addEventListener('click', function () { window.print(); });
  });

  /* ---- wizard konsultasi ---- */
  var form = document.getElementById('form-konsul');
  if (form) {
    var langkah = Array.prototype.slice.call(form.querySelectorAll('.langkah'));
    var progres = Array.prototype.slice.call(form.querySelectorAll('.progres li'));
    var kini = Math.max(1, Math.min(langkah.length, parseInt(form.dataset.mulai, 10) || 1));
    var tampil = function (n) {
      kini = n;
      langkah.forEach(function (el, i) { el.classList.toggle('aktif', i === n - 1); });
      progres.forEach(function (el, i) {
        el.classList.toggle('aktif', i === n - 1);
        el.classList.toggle('selesai', i < n - 1);
      });
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };
    form.addEventListener('click', function (e) {
      var a = e.target.closest('[data-aksi]');
      if (!a) return;
      tampil(kini + (a.dataset.aksi === 'maju' ? 1 : -1));
    });
    // "Tidak ada ..." saling meniadakan dengan pilihan lain dalam grup
    form.querySelectorAll('[data-grup]').forEach(function (g) {
      g.addEventListener('change', function (e) {
        var none = g.querySelector('[data-none]');
        if (!none) return;
        if (e.target === none && none.checked) {
          g.querySelectorAll('input:not([data-none])').forEach(function (c) { c.checked = false; });
        } else if (e.target !== none && e.target.checked) {
          none.checked = false;
        }
      });
    });
    tampil(kini);
  }

  /* ---- filter tabel basis pengetahuan ---- */
  var cari = document.getElementById('cari');
  if (cari) cari.addEventListener('input', function () {
    var q = cari.value.toLowerCase();
    document.querySelectorAll('table[data-filter] tbody tr').forEach(function (tr) {
      tr.hidden = q && tr.textContent.toLowerCase().indexOf(q) === -1;
    });
  });

  /* ---- pengingat kunjungan (localStorage, tanpa server) ---- */
  var fi = document.getElementById('form-ingat');
  if (fi) {
    var KEY = 'pengingat_kb_v1';
    var daftar = document.getElementById('daftar-ingat');
    var kosong = document.getElementById('kosong-ingat');
    var muat = function () { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } };
    var simpan = function (a) { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} };
    var selisih = function (iso) {
      var t = new Date(); t.setHours(0, 0, 0, 0);
      return Math.round((new Date(iso + 'T00:00:00') - t) / 86400000);
    };
    var tglIndo = function (iso) {
      return new Date(iso + 'T00:00:00').toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
    };
    var el = function (tag, cls, teks) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (teks !== undefined) n.textContent = teks;
      return n;
    };
    var unduhIcs = function (it) {
      var d = it.tanggal.replace(/-/g, '');
      var akhir = new Date(it.tanggal + 'T00:00:00'); akhir.setDate(akhir.getDate() + 1);
      var e = akhir.getFullYear() + ('0' + (akhir.getMonth() + 1)).slice(-2) + ('0' + akhir.getDate()).slice(-2);
      var stamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
      var isi = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Sahabat KB//ID', 'BEGIN:VEVENT',
        'UID:' + it.id + '@sahabat-kb', 'DTSTAMP:' + stamp, 'DTSTART;VALUE=DATE:' + d, 'DTEND;VALUE=DATE:' + e,
        'SUMMARY:Kunjungan ulang KB (' + it.metode + ')',
        'DESCRIPTION:Ikuti petunjuk bidan. Jika ragu atau jadwal terlewat\\, segera konsultasi dengan tenaga kesehatan.',
        'BEGIN:VALARM', 'TRIGGER:-P1D', 'ACTION:DISPLAY', 'DESCRIPTION:Besok kunjungan ulang KB', 'END:VALARM',
        'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
      var url = URL.createObjectURL(new Blob([isi], { type: 'text/calendar' }));
      var a = el('a'); a.href = url; a.download = 'kunjungan-kb.ics';
      document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    };
    var render = function () {
      var data = muat().sort(function (a, b) { return a.tanggal < b.tanggal ? -1 : 1; });
      daftar.textContent = '';
      kosong.hidden = data.length > 0;
      data.forEach(function (it) {
        var s = selisih(it.tanggal);
        var kartu = el('article', 'kartu ingat' + (s < 0 ? ' lewat' : s === 0 ? ' hariini' : ''));
        kartu.appendChild(el('span', 'lencana', it.metode));
        kartu.appendChild(el('div', 'hari', s > 0 ? s + ' hari lagi' : s === 0 ? 'Hari ini' : 'Terlewat ' + (-s) + ' hari'));
        kartu.appendChild(el('div', '', tglIndo(it.tanggal)));
        if (it.catatan) kartu.appendChild(el('div', 'bantu', it.catatan));
        if (s < 0) kartu.appendChild(el('p', 'bantu', 'Ikuti petunjuk sesuai jenis KB Anda dan segera konsultasi dengan bidan atau tenaga kesehatan agar mendapat arahan yang tepat.'));
        var t = el('div', 'tindak');
        var b1 = el('button', 'tombol', 'Simpan ke kalender'); b1.type = 'button';
        b1.addEventListener('click', function () { unduhIcs(it); });
        var b2 = el('button', 'tombol', 'Hapus'); b2.type = 'button';
        b2.addEventListener('click', function () { simpan(muat().filter(function (x) { return x.id !== it.id; })); render(); });
        t.appendChild(b1); t.appendChild(b2); kartu.appendChild(t);
        daftar.appendChild(kartu);
      });
    };
    fi.addEventListener('submit', function (e) {
      e.preventDefault();
      var a = muat();
      a.push({
        id: String(Date.now()) + Math.floor(Math.random() * 1000),
        metode: document.getElementById('i-metode').value,
        tanggal: document.getElementById('i-tanggal').value,
        catatan: document.getElementById('i-catatan').value.trim()
      });
      simpan(a); fi.reset(); render();
    });
    render();
  }
})();
