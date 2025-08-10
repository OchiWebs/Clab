# Project Adamantine Strain

<p align="center">
  <img src="https://raw.githubusercontent.com/gist/gemini-ai-assistant/a2e04fbe58a0d4814e565982855f4648/raw/a0833a69a915998b5327289f1f0a2d219273f5ac/labvault_logo.svg" alt="Project Logo" width="150"/>
</p>

<p align="center">
  <i>"A seemingly unbreakable system, with a fatal strain hidden within."</i>
  <br><br>
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-2.3-green?style=for-the-badge&logo=flask" alt="Flask Version">
  <img src="https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker" alt="Docker Ready">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" alt="License">
</p>

---

## ## Tentang Proyek Ini

**Project Adamantine Strain** adalah sebuah laboratorium keamanan siber dalam bentuk aplikasi web yang sengaja dibuat rentan (*deliberately vulnerable*). Aplikasi ini dirancang untuk mensimulasikan lingkungan korporat modern yang terlihat aman di permukaan, lengkap dengan mekanisme pertahanan seperti **CSRF Token** dan **API Rate Limiting**.

Tujuan utamanya adalah untuk melatih para praktisi keamanan dalam menemukan dan mengeksploitasi celah keamanan tingkat lanjut yang bersifat multi-langkah dan tersembunyi di dalam logika bisnis atau arsitektur aplikasi.

### ### Dibangun Dengan

* [Flask](https://flask.palletsprojects.com/) - Micro-framework web untuk Python.
* [Flask-WTF](https://flask-wtf.readthedocs.io/) - Untuk integrasi form dan proteksi CSRF.
* [Jinja2](https://jinja.palletsprojects.com/) - Template engine.
* [Bootstrap 5](https://getbootstrap.com/) - Framework CSS untuk tampilan profesional.
* [Docker](https://www.docker.com/) - Untuk deployment yang mudah dan konsisten.

---

## ## Memulai

Untuk menjalankan lab ini di mesin lokal Anda, ikuti langkah-langkah di bawah ini.

### ### Prasyarat

Pastikan perangkat lunak berikut sudah terpasang di sistem Anda:
* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/) & [Docker Compose](https://docs.docker.com/compose/install/) (Untuk metode instalasi yang direkomendasikan)
* [Python 3.9+](https://www.python.org/downloads/) (Untuk metode instalasi manual)

### ### Instalasi

Ada dua cara untuk menjalankan proyek ini:

**A. Menggunakan Docker (Direkomendasikan)**

Ini adalah cara termudah dan paling andal untuk menjalankan aplikasi tanpa mengkhawatirkan dependensi.

1.  **Clone repositori ini:**
    ```sh
    git clone https://github.com/OchiWebs/FacadeLab.git
    cd NAMA_REPO_ANDA
    ```

2.  **Jalankan dengan Docker Compose:**
    Perintah ini akan membangun *image* dan menjalankan *container* secara otomatis.
    ```sh
    docker-compose up --build
    ```

3.  Aplikasi sekarang berjalan di `http://localhost:5001`

**B. Instalasi Manual (Lokal)**

Gunakan cara ini jika Anda tidak ingin menggunakan Docker.

1.  **Clone repositori:**
    ```sh
    git clone https://github.com/OchiWebs/FacadeLab.git
    cd NAMA_REPO_ANDA
    ```

2.  **Buat dan aktifkan Virtual Environment:**
    * Di Windows:
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * Di macOS/Linux:
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install semua dependensi:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi Flask:**
    ```sh
    flask run
    ```

5.  Aplikasi sekarang berjalan di `http://localhost:5000`

---

## ## Penggunaan

Setelah aplikasi berjalan, buka browser Anda dan akses alamat yang sesuai.

### ### Kredensial Login

Anda dapat menggunakan salah satu dari tiga akun pengguna yang telah disiapkan:

| Peran         | Username | Password    |
| :------------ | :------- | :---------- |
| Administrator | `admin`  | `password123` |
| Manajer       | `manager`| `password123` |
| Karyawan      | `employee`| `password123` |

---

## ## 🎯 Tantangan Keamanan (Spoiler!)

<details>
  <summary><strong>Klik di sini untuk melihat petunjuk mengenai celah keamanan yang ada.</strong></summary>
  
  ### ### 1. Server-Side Template Injection (SSTI) -> Remote Code Execution (RCE)
  * **Lokasi:** Fitur "Generate Report" pada halaman detail proyek.
  * **Petunjuk:** Aplikasi ini tampaknya merender judul laporan yang Anda masukkan. Apa yang terjadi jika Anda memasukkan ekspresi template seperti `{{ 7*7 }}`? Bisakah Anda meningkatkannya untuk berinteraksi dengan sistem operasi (`os`) server?

  ### ### 2. CSRF pada API -> Pengambilalihan Proyek
  * **Lokasi:** Endpoint API `POST /api/proyek/<uuid>/ganti_pemilik`.
  * **Petunjuk:** Meskipun form HTML dilindungi oleh CSRF token, apakah perlindungan yang sama berlaku untuk semua endpoint API? Seorang `manager` bisa membuat halaman web berbahaya yang, jika dikunjungi oleh `admin`, akan mengirim request untuk mengubah kepemilikan proyek rahasia. Serangan ini memerlukan *social engineering*.

  ### ### 3. Information Disclosure & IDOR
  * **Lokasi:** Respons dari API `GET /api/proyek/<uuid>/tasks`.
  * **Petunjuk:** Periksa respons JSON dari API ini menggunakan Developer Tools. Apakah ada informasi sensitif (seperti UUID pengguna lain) yang bocor? Bisakah informasi tersebut digunakan untuk mengakses halaman profil pengguna lain secara tidak sah?

  ### ### 4. Melewati Rate Limiting
  * **Lokasi:** Semua endpoint API.
  * **Petunjuk:** API ini akan memblokir Anda jika Anda mengirim terlalu banyak request dalam waktu singkat. Mekanisme ini berbasis alamat IP. Bagaimana cara seorang penyerang bisa melewati pertahanan seperti ini di dunia nyata?

</details>

---

## ## Lisensi

Didistribusikan di bawah Lisensi MIT. Lihat `LICENSE` untuk informasi lebih lanjut.

## ## Kontak

[Nama Anda] - [email@anda.com]

Link Proyek: [https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA](https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA)

