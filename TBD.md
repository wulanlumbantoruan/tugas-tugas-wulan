# Ringkasan Materi: Database Transactions

## 1. Definisi Dasar Transaksi
* **Pengertian:** Transaksi adalah serangkaian operasi (proses) pada basis data yang dijalankan sebagai satu kesatuan logis.
* **Prinsip Utama:** Semua operasi harus berhasil dijalankan, atau tidak dijalankan sama sekali (*All or Nothing*).
* **Tujuan:** Mencegah masalah integritas data dan mencerminkan kejadian nyata (seperti transfer bank atau pembelian e-commerce).
* **Komponen SQL:** Transaksi bisa terdiri dari kombinasi perintah `SELECT`, `UPDATE`, dan `INSERT`.

## 2. Prinsip Utama: ACID (Sangat Penting untuk Ujian)
Ini adalah konsep paling krusial dalam materi transaksi. Hafalkan kepanjangan dan maknanya:

* **A - Atomicity (Keutuhan):**
    Semua operasi SQL dalam transaksi harus selesai sepenuhnya. Jika satu gagal, seluruh transaksi dibatalkan.
    *Contoh:* Transfer uang (Debet Akun A & Kredit Akun B). Jika Kredit gagal, Debet harus dibatalkan.
* **C - Consistency (Ketepatan):**
    Eksekusi transaksi harus membawa database dari satu keadaan valid (konsisten) ke keadaan valid lainnya sesuai aturan integritas.
* **I - Isolation (Pemisahan):**
    Jika ada banyak transaksi berjalan bersamaan (*multi-user*), mereka tidak boleh saling mengganggu. Data yang sedang diproses Transaksi A tidak boleh diakses Transaksi B sampai A selesai.
* **D - Durability (Daya Tahan):**
    Setelah transaksi dinyatakan berhasil (*commit*), perubahannya bersifat permanen dan tidak akan hilang meskipun sistem mati atau *crash*.

## 3. Daur Hidup (State) Transaksi
Sebuah transaksi akan melewati status-status berikut:
1.  **Active (Aktif):** Status awal saat transaksi sedang dieksekusi.
2.  **Partially Committed (Berhasil Sebagian):** Operasi terakhir selesai, tapi belum disimpan permanen.
3.  **Committed (Berhasil Sempurna):** Transaksi sukses total dan data tersimpan permanen.
4.  **Failed (Gagal):** Transaksi terhenti sebelum tuntas (bisa karena error sistem atau logic).
5.  **Aborted (Batal):** Transaksi dianggap tidak pernah terjadi setelah dilakukan *rollback* (mengembalikan data ke nilai semula).

## 4. Skema & Manajemen Transaksi
Dalam sistem database, terdapat komponen yang mengatur jalannya transaksi:
* **Transaction Manager:** Mengelola transaksi awal.
* **Scheduler:** Menentukan urutan eksekusi transaksi.
* **Recovery Manager:** Bertanggung jawab melakukan *commit* atau *rollback* jika ada kegagalan.
* **Cache Manager:** Mengelola penyimpanan sementara (memori *volatile*).

## 5. Implementasi Teknis di MySQL
* **Syarat Engine:** Wajib menggunakan **InnoDB** (mendukung ACID). Engine MyISAM tidak mendukung transaksi.
* **Perintah Penting:**
    * `START TRANSACTION` atau `BEGIN`: Memulai transaksi.
    * `COMMIT`: Menyimpan perubahan secara permanen.
    * `ROLLBACK`: Membatalkan perubahan dan kembali ke kondisi awal.
    * `SAVEPOINT`: Membuat titik aman tertentu dalam transaksi, sehingga jika error, kita bisa *rollback* ke titik ini saja (tidak perlu membatalkan seluruh transaksi).
* **Auto-Commit:** Secara default MySQL menggunakan mode *auto-commit* (langsung simpan). Untuk transaksi manual, ini sering dimatikan dengan `SET @@autocommit = 0`.

### ⚠️ Prediksi Soal Ujian (Wajib Diingat)
Berdasarkan isi modul, berikut adalah materi yang sangat potensial keluar dalam ujian (baik teori maupun praktik):

1.  **Studi Kasus ACID:**
    * *Soal:* "Jelaskan apa yang terjadi jika lampu mati saat proses transfer bank sedang berlangsung?"
    * *Jawab:* Fokus pada prinsip Atomicity dan Durability. Sistem akan melakukan Rollback saat restart karena transaksi belum Commit sempurna.
2.  **Perbedaan Engine MySQL:**
    * *Soal:* "Mengapa transaksi saya tidak bisa di-rollback padahal sintaksnya benar?"
    * *Jawab:* Cek Storage Engine tabelnya. Kemungkinan tabel masih menggunakan MyISAM, harus diubah ke InnoDB dengan perintah `ALTER TABLE`.
3.  **Perintah yang Tidak Bisa di-Rollback (Jebakan):**
    * Hati-hati! Tidak semua perintah bisa dibatalkan. Perintah DDL (*Data Definition Language*) melakukan commit implisit (otomatis).
    * *Daftar perintah yang tidak bisa di-rollback:* `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, `TRUNCATE TABLE`, `CREATE INDEX`.
    * *Tips:* Jika di ujian ada soal transaksi yang menyelipkan perintah `ALTER TABLE` di tengah-tengahnya, maka transaksi sebelum baris itu otomatis tersimpan dan tidak bisa di-*rollback*.
4.  **Fungsi Savepoint:**
    * *Soal:* Bagaimana cara membatalkan sebagian transaksi saja tanpa menghapus semuanya?
    * *Jawab:* Gunakan `SAVEPOINT nama_point;` lalu `ROLLBACK TO SAVEPOINT nama_point;`.

---

# Ringkasan Materi: Concurrency Control

## 1. Definisi & Tujuan
* **Apa itu?** Kontrol konkurensi adalah koordinasi pelaksanaan transaksi yang terjadi secara simultan (bersamaan) dalam sistem database multiuser.
* **Tujuan Utama:** Menjamin **Serializability**. Artinya, hasil eksekusi transaksi yang berjalan bersamaan (paralel) harus sama persis dengan jika transaksi tersebut dijalankan satu per satu (serial).

## 2. Masalah Jika Tanpa Kontrol (Wajib Hafal)
Jika transaksi berjalan bersamaan tanpa aturan, 3 masalah fatal ini bisa terjadi:

**A. Lost Update (Pembaruan yang Hilang)**
* **Konsep:** Dua transaksi memperbarui data yang sama, dan pembaruan terakhir menimpa pembaruan pertama sehingga data pertama "hilang".
* **📝 Contoh:**
    * Stok awal: 35.
    * T1 membaca stok 35, lalu menambah 100 (menjadi 135).
    * T2 membaca stok 35 (sebelum T1 selesai), lalu mengurangi 30 (menjadi 5).
    * T1 simpan 135. T2 simpan 5.
    * *Hasil:* Stok jadi 5. Padahal seharusnya $35 + 100 - 30 = 105$. Penambahan 100 oleh T1 hilang.

**B. Uncommitted Data (Data Belum dikomit)**
* **Konsep:** T2 membaca data yang diubah oleh T1, padahal T1 belum melakukan *commit* (dan akhirnya T1 gagal/rollback).
* **📝 Contoh:**
    * T1 ubah saldo dari 100 jadi 200 (belum commit).
    * T2 baca saldo 200 untuk cetak resi.
    * T1 tiba-tiba error dan Rollback (saldo balik ke 100).
    * *Hasil:* T2 memegang data "hantu" (200) yang tidak valid.

**C. Inconsistent Retrievals (Pengambilan Tidak Konsisten)**
* **Konsep:** T1 membaca sebagian data sebelum diubah T2, dan sebagian lagi setelah diubah T2, menghasilkan data agregat (total) yang kacau.
* **📝 Contoh:** T1 sedang menghitung total aset bank. T2 melakukan transfer antar cabang saat T1 sedang menghitung. Akibatnya, uang yang ditransfer mungkin terhitung dua kali atau tidak terhitung sama sekali.

## 3. Mekanisme & Protokol Penguncian (Locking)
Ini adalah cara sistem mencegah masalah di atas.

**Jenis Kunci (Lock Modes):**
* **Exclusive (X):** Data bisa dibaca (Read) DAN diubah (Write). Transaksi lain tidak boleh akses sama sekali.
* **Shared (S):** Data hanya boleh dibaca (Read). Transaksi lain boleh ikut baca (Share), tapi tidak boleh ubah.

**2-Phase Locking Protocol (2PL)**
Protokol ini menjamin serializability. Transaksi dibagi menjadi dua fase:
1.  **Growing Phase (Fase Bertumbuh):** Transaksi boleh mengambil kunci (Lock), tapi tidak boleh melepas kunci satupun.
2.  **Shrinking Phase (Fase Pelepasan):** Transaksi boleh melepas kunci (Unlock), tapi tidak boleh mengambil kunci baru lagi.

*📝 Contoh:* Bayangkan belanja di kasir.
* *Growing:* Kamu ambil barang A, B, C masuk keranjang.
* *Lockpoint:* Kamu selesai ambil barang, siap bayar.
* *Shrinking:* Kamu bayar dan barang dikeluarkan dari keranjang. Kamu tidak boleh lari balik ke rak ambil barang D saat sedang proses bayar.

## 4. Timestamp-Based Protocols
Sistem memberi "stempel waktu" pada setiap transaksi.
* **Aturan Dasar:** Transaksi yang lebih tua (Timestamp kecil) diprioritaskan.
* **Aturan Konflik:** Jika Transaksi A (baru) sudah membaca data, lalu Transaksi B (lama) mau mengubah data tersebut, Transaksi B akan ditolak (Rollback) karena dianggap terlambat (kadaluwarsa).

## 5. Deadlock (Sering Keluar di Ujian)
* **Definisi:** Kondisi saling tunggu. T1 mengunci A dan minta B. T2 mengunci B dan minta A. Keduanya macet selamanya.
* **Pencegahan (Prevention):**
    * **Wait-Die:** Jika T_tua minta data T_muda, T_tua menunggu. Jika T_muda minta data T_tua, T_muda mati (rollback). (Yang tua mengalah menunggu).
    * **Wound-Wait:** Jika T_tua minta data T_muda, T_muda "dilukai" (rollback) agar T_tua bisa masuk. Jika T_muda minta data T_tua, T_muda menunggu. (Yang tua prioritas, yang muda disingkirkan).
* **Deteksi:** Menggunakan **Wait-for Graph**. Jika ada siklus (lingkaran panah) dalam grafik, berarti terjadi deadlock.

### ⚠️ Prediksi Soal Ujian (Sangat Potensial)
1.  **Identifikasi Masalah Konkurensi:**
    * *Soal:* Diberikan tabel urutan waktu (seperti halaman 7 modul). Kamu diminta menentukan masalah apa yang terjadi.
    * *Jawaban:* Perhatikan kapan WRITE terjadi. Jika T1 Write lalu ditimpa T2 Write tanpa T2 membaca update T1 dulu, itu *Lost Update*.
2.  **Perbedaan Fase 2PL:**
    * *Soal:* Jelaskan perbedaan Growing Phase dan Shrinking Phase!
    * *Kunci:* Fokus pada kata "Akuisisi" (Growing) dan "Pelepasan" (Shrinking). Ingat aturannya: di fase shrinking dilarang ambil kunci baru.
3.  **Deadlock Prevention (Logika Wait-Die vs Wound-Wait):**
    * *Soal:* T1 (Timestamp 5) minta data yang dipegang T2 (Timestamp 10). Apa yang terjadi pada metode Wait-Die?
    * *Analisis:* T1 lebih kecil (lebih tua/senior), T2 lebih besar (lebih muda/junior).
    * *Jawab:* Di Wait-Die (Non-preemptive), Senior menunggu Junior. Jadi T1 menunggu T2.
    * *Tips:* Ingat "Wait-Die" = Senior Wait (Tua Nunggu). "Wound-Wait" = Senior Wound (Tua Melukai/Mengusir).
4.  **Wait-For Graph:**
    * *Soal:* Diberikan gambar node lingkaran. Manakah yang Deadlock?
    * *Jawab:* Cari gambar yang panahnya muter membentuk lingkaran tertutup (Cycle).

---

# Ringkasan Materi: Recovery System

## 1. Konsep Dasar Kegagalan & Masalah
Kegagalan sistem (seperti listrik mati tiba-tiba) menyebabkan dua masalah utama pada transaksi:
1.  **Hilangnya Durability (Daya Tahan):** Transaksi yang sudah sukses (commit) tapi datanya belum sempat tersimpan permanen di harddisk karena masih di RAM.
2.  **Hilangnya Atomicity (Keutuhan):** Transaksi baru berjalan setengah (belum tuntas), tapi sistem mati. Data menjadi tidak konsisten (uang terpotong di A tapi belum masuk ke B).

## 2. Solusi Utama: LOG (Catatan Transaksi)
* **Definisi:** Log adalah catatan detail yang merekam setiap operasi transaksi. Disimpan di penyimpanan permanen (*nonvolatile*).
* **Isi Record Log:** Nama transaksi, data yang diubah, Nilai Lama (*Old Value*), dan Nilai Baru (*New Value*).
* **Hierarki Penyimpanan Log:**
    * Log ditulis dulu ke Log Buffer (di RAM/Memori) agar cepat.
    * Log Writer bertugas memindahkan data dari Buffer ke Log File (di Harddisk/Disk).
* **Aturan Penting:** Log harus ditulis ke disk sebelum data aktual database ditulis (*Write-Ahead Logging*).

## 3. Mekanisme Pemulihan (Recovery Operations)
Saat sistem hidup kembali setelah mati (restart), Recovery Manager akan melakukan dua hal berdasarkan Log:

**A. REDO (Forward Recovery / Maju)**
* **Tujuan:** Menangani masalah Durability. Mengulang kembali transaksi yang sudah Commit tapi datanya hilang di RAM.
* **Syarat:** Di log ditemukan record `<Ti, begin>` DAN `<Ti, commit>`.
* **Cara:** Mengubah nilai data menjadi *New Value* sesuai urutan log.

**B. UNDO (Backward Recovery / Mundur)**
* **Tujuan:** Menangani masalah Atomicity. Membatalkan transaksi yang belum selesai (gagal di tengah jalan).
* **Syarat:** Di log ditemukan `<Ti, begin>` TETAPI tidak ada commit atau rollback.
* **Cara:** Mengembalikan nilai data menjadi *Old Value* (mundur dari kejadian terakhir ke awal).

## 4. Checkpoint
* **Masalah:** Menelusuri log dari awal sekali sangat lambat.
* **Solusi:** Checkpoint adalah titik penanda di mana semua data di buffer (RAM) dipaksa tulis (*force-writing*) ke harddisk secara permanen.
* **Manfaat:** Saat recovery, sistem cukup memproses log mulai dari checkpoint terakhir, tidak perlu dari awal zaman.

## 5. Strategi Log & Update (Sering Keluar Ujian)
Ada dua pendekatan utama mencatat perubahan:
1.  **Deferred Update (Penundaan Modifikasi):**
    * Perubahan dicatat di log dulu, tapi penulisan ke database asli ditunda sampai transaksi Commit.
    * *Ciri:* Tidak memerlukan "Nilai Lama" di log.
2.  **Immediate Update (Pengubahan Langsung):**
    * Perubahan langsung ditulis ke database meskipun transaksi masih berjalan (belum commit).
    * *Syarat Mutlak:* Record Log harus ditulis ke disk sebelum data database diubah.

## 6. Shadow Paging (Alternatif Tanpa Log)
* **Konsep:** Menggunakan dua tabel halaman: *Current Page* (Halaman Aktif) dan *Shadow Page* (Halaman Bayangan/Cadangan).
* **Cara Kerja:** Selama transaksi, perubahan dilakukan pada halaman salinan (copy). Halaman asli tidak disentuh.
* **Kelebihan:** Recovery sangat cepat (tidak butuh Undo/Redo).
* **Kekurangan:** Terjadi fragmentasi data (data terpecah-pecah) dan proses commit lebih lambat.

## 7. Jenis Backup
* **Statis (Offline):** Database dimatikan dulu. Hasil backup konsisten tapi sistem harus mati (*downtime*).
* **Dinamis (Online):** Backup dilakukan saat database aktif/hidup. Hati-hati karena bisa mengganggu performa.
* **Remote Backup:** Data dikirim ke situs cadangan (lokasi lain) secara real-time lewat jaringan untuk bencana besar.

### 📝 Contoh Studi Kasus & Prediksi Soal Ujian
Berikut adalah contoh penerapan yang sangat mungkin keluar di ujian (Essay atau Pilihan Ganda):

**Skenario:**
Terjadi mati listrik pada pukul 10:00. Berikut isi Log terakhir yang ditemukan teknisi:

| Record Log | Isi |
| :--- | :--- |
| `<T1, begin>` | Transaksi 1 Mulai |
| `<T1, A, 100, 200>` | T1 ubah A: 100 jadi 200 |
| `<T2, begin>` | Transaksi 2 Mulai |
| `<T1, commit>` | Transaksi 1 Selesai |
| `<T2, B, 500, 400>` | T2 ubah B: 500 jadi 400 |
| *(Listrik Mati Disini)* | |

**Analisis Soal Ujian:**
* **Tanya:** Apa yang dilakukan sistem recovery terhadap T1?
    * **Jawab:** Sistem melakukan **REDO** pada T1.
    * **Alasan:** T1 memiliki `<begin>` dan `<commit>` lengkap di log. Meskipun listrik mati, perubahan T1 (A jadi 200) harus dipastikan tersimpan.
* **Tanya:** Apa yang dilakukan sistem recovery terhadap T2?
    * **Jawab:** Sistem melakukan **UNDO** pada T2.
    * **Alasan:** T2 memiliki `<begin>` tapi tidak ada `<commit>` saat listrik mati. Transaksi dianggap gagal, nilai B harus dikembalikan ke 500 (Nilai Lama).
* **Tanya:** Sebutkan kelemahan Shadow Paging dibanding Log-based!
    * **Jawab:** Menyebabkan fragmentasi data ("data sampah") dan proses commit yang lebih berat karena menyalin blok data.

---

# Ringkasan Materi: Spatial Database

## 1. Konsep Dasar Data Spasial
Basis data spasial tidak hanya menyimpan apa (atribut), tetapi juga di mana (lokasi) suatu objek berada. Ada dua model utama untuk merepresentasikan data ini:

**A. Raster Model (Grid):**
* Area dibagi menjadi sel/grid (biasanya persegi) dengan ukuran sama.
* Setiap sel memiliki nilai tunggal.
* *Contoh:* Citra satelit, foto udara (Digital Orthophoto), ketinggian tanah (DEM).
* *Ciri:* Data bersifat continuous (berlanjut).

**B. Vector Model (Objek Diskrit):**
* Merepresentasikan fitur geografis sebagai bentuk geometri.
* **Tipe Geometri Utama:**
    * **Point (Titik):** Pohon, tiang listrik, lokasi kejadian.
    * **Line/Arc (Garis):** Jalan raya, sungai, jalur kereta api.
    * **Polygon (Area):** Batas kota, danau, persil tanah, jenis tanah.
* *Ciri:* Data bersifat discrete (terpisah).

## 2. Properti Data Spasial (Hafalkan Definisi ini)
Setiap data geografis memiliki 4 properti utama:
1.  **Projection (Proyeksi):** Metode mengubah permukaan bumi yang melengkung (3D) menjadi peta datar (2D). Distorsi pasti terjadi.
2.  **Scale (Skala):** Rasio jarak di peta berbanding jarak sebenarnya di lapangan.
3.  **Accuracy (Akurasi):** Seberapa dekat data di database dengan kenyataan di dunia nyata (posisi, konsistensi, kelengkapan).
4.  **Resolution (Resolusi):** Ukuran fitur terkecil yang bisa dikenali. Pada raster, ini adalah ukuran pixel.

## 3. Hubungan Spasial (Spatial Relationships)
Sistem perlu memahami hubungan antar objek, bukan hanya koordinatnya. Hubungan ini dibagi menjadi:
* **Topologi (Connectivity & Contiguity):**
    * *Contoh:* Apakah jalan A terhubung dengan jalan B? Apakah wilayah A bersebelahan dengan wilayah B?
* **Operasi Koordinat (X,Y):**
    * **Disjoint:** A dan B terpisah (tidak bersentuhan sama sekali).
    * **Touches:** A dan B bersentuhan di batas (boundary), tapi tidak tumpang tindih.
    * **Overlaps:** A dan B tumpang tindih sebagian.
    * **Contains / Within:** A berada sepenuhnya di dalam B (atau sebaliknya).

## 4. Desain Basis Data Spasial (Expanded E-R Model)
Dalam perancangan database, kita memperluas diagram E-R biasa untuk menangani objek spasial. Setiap entitas reguler diberi "pasangan" entitas spasialnya.
* **📝 Contoh Desain:**
    * Entitas City (Kota) $\rightarrow$ Tipe Spasial: POLYGON.
    * Entitas River (Sungai) $\rightarrow$ Tipe Spasial: LINE.
    * Entitas Hospital (RS) $\rightarrow$ Tipe Spasial: POINT.
    * Relasi: City *Contains* Hospital.

## 5. Spatial Query (SQL dengan Fungsi Spasial)
Ini adalah bagian paling teknis dan sering keluar di ujian praktik atau isian. PostGIS menggunakan fungsi khusus yang diawali dengan `ST_`. Berikut adalah fungsi-fungsi kuncinya:

**A. ST_Within (Di dalam)**
* **Fungsi:** Mengembalikan TRUE jika Geometri A berada sepenuhnya di dalam Geometri B.
* **📝 Contoh Kasus:** Mencari bandara (airports) yang letaknya di dalam area hutan (trees) tertentu.
* **Query:**
    ```sql
    SELECT a.name, t.vegdesc
    FROM airports a, trees t
    WHERE ST_Within(a.geom, t.geom);
    ```

**B. ST_Intersects (Berpotongan/Bersinggungan)**
* **Fungsi:** Mengembalikan TRUE jika A dan B berbagi ruang (bersentuhan, tumpang tindih, atau di dalam). Kebalikan dari Disjoint.
* **📝 Contoh Kasus:** Mencari jalur kereta api (railroads) yang membelah atau melewati hutan (trees).
* **Query:**
    ```sql
    SELECT r.gid, t.vegdesc
    FROM railroads r, trees t
    WHERE ST_Intersects(r.geom, t.geom);
    ```

**C. ST_Distance (Jarak Eksak)**
* **Fungsi:** Menghitung jarak minimum Cartesian (garis lurus) antara dua geometri.
* **📝 Contoh Kasus:** Menghitung jarak antara bandara dengan rel kereta, lalu pilih yang jaraknya kurang dari 50km (50.000 meter).
* **Query:**
    ```sql
    SELECT a.name, ST_Distance(a.geom, r.geom)
    FROM airports a, railroads r
    WHERE ST_Distance(a.geom, r.geom) <= 50000;
    ```

**D. ST_DWithin (Distance Within / Dalam Radius)**
* **Fungsi:** Mengembalikan TRUE jika dua objek berada dalam jarak radius tertentu. Ini lebih efisien daripada menggunakan `ST_Distance` di dalam klausa WHERE.
* **📝 Contoh Kasus:** Apakah bandara A berada dalam radius 50km dari rel kereta?
* **Query:**
    ```sql
    SELECT a.name
    FROM airports a, railroads r
    WHERE ST_DWithin(a.geom, r.geom, 50000);
    ```

### ⚠️ Prediksi Soal Ujian (Wajib Diingat)
Berdasarkan struktur modul, berikut adalah materi yang sangat potensial keluar:

1.  **Raster vs Vector:**
    * *Soal:* "Jelaskan perbedaan model data Raster dan Vektor, serta berikan contoh penggunaan masing-masing!"
    * *Jawab:* Fokus pada Grid/Pixel vs Geometri (Titik/Garis/Polygon). Raster untuk data kontinu (suhu, elevasi), Vektor untuk data diskrit (batas tanah, lokasi gedung).
2.  **Analisis SQL Spas
