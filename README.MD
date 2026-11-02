# Python OpenAPI Example

API REST berbasis **FastAPI** dengan database **PostgreSQL**, CRUD user, operasi hitung angka, dan autentikasi JWT.

Dokumentasi interaktif (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Daftar Isi

1. [Prasyarat](#prasyarat)
2. [Struktur Proyek](#struktur-proyek)
3. [Instalasi Lokal](#instalasi-lokal)
4. [Konfigurasi Database PostgreSQL](#konfigurasi-database-postgresql)
5. [Menjalankan Aplikasi](#menjalankan-aplikasi)
6. [Docker](#docker)
7. [Docker Compose](#docker-compose)
8. [API Reference](#api-reference)
9. [Contoh Request (curl)](#contoh-request-curl)
10. [Catatan Keamanan](#catatan-keamanan)

---

## Prasyarat

- Python 3.12+
- PostgreSQL 14+ (lokal atau via Docker)
- (Opsional) Docker & Docker Compose

---

## Struktur Proyek

```
python-openapi/
├── main.py              # Entry point FastAPI, endpoint demo & JWT
├── database.py          # Koneksi PostgreSQL (SQLAlchemy)
├── models.py            # Model tabel users
├── schemas.py           # Validasi request/response (Pydantic)
├── auth_utils.py        # Hash password (bcrypt)
├── routers/
│   └── users.py         # CRUD user
├── requirements.txt     # Dependensi Python
├── Dockerfile           # Image aplikasi
├── docker-compose.yml   # PostgreSQL + API
├── .env.example         # Contoh variabel lingkungan
└── README.MD            # Dokumentasi ini
```

---

## Instalasi Lokal

```bash
cd python-openapi

# Buat & aktifkan virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install dependensi
pip install -r requirements.txt
```

### Dependensi utama

| Paket | Fungsi |
|-------|--------|
| fastapi | Framework API |
| uvicorn | ASGI server |
| sqlalchemy | ORM database |
| psycopg2-binary | Driver PostgreSQL |
| bcrypt | Hash password user |
| python-jose | Token JWT |
| python-multipart | Form login OAuth2 |
| email-validator | Validasi email |

---

## Konfigurasi Database PostgreSQL

Aplikasi membaca connection string dari variabel lingkungan **`DATABASE_URL`**.

Format:

```
postgresql+psycopg2://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>
```

### 1. Buat database di PostgreSQL

```bash
# Masuk ke psql (sesuaikan user Anda)
psql -U postgres

CREATE DATABASE python_openapi;
\q
```

### 2. Set variabel lingkungan

Salin file contoh dan sesuaikan kredensial Anda:

```bash
cp .env.example .env
```

Isi `.env` (contoh — **PostgreSQL di laptop**, port **5432**):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=PASSWORD_ANDA
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=python_openapi
DATABASE_URL=postgresql+psycopg2://postgres:PASSWORD_ANDA@127.0.0.1:5432/python_openapi
```

File `.env` dibaca otomatis saat aplikasi start (`python-dotenv`).

**Default** jika `DATABASE_URL` tidak diset:

```
postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/python_openapi
```

Tabel `users` dibuat otomatis saat aplikasi pertama kali dijalankan (`create_all` pada startup).

### Skema tabel `users`

| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | Integer | Primary key, auto increment |
| nama | String | Nama user |
| email | String | Unik, terindeks |
| password | String | Hash bcrypt (tidak dikembalikan di API) |

---

## Menjalankan Aplikasi

Panduan ini menjalankan API **di laptop** (tanpa Docker), dengan database **PostgreSQL lokal** (pgAdmin / port **5432**).

### Langkah demi langkah (development)

#### Langkah 1 — Masuk ke folder proyek

**Linux / macOS (bash):**

```bash
cd python-openapi
```

**Windows (PowerShell):**

```powershell
cd D:\learning\Learning_Flutter\python_openapi
```

(Sesuaikan path dengan lokasi folder Anda.)

#### Langkah 2 — Buat dan aktifkan virtual environment

**Linux / macOS:**

```bash
python3 -m venv myenv
source myenv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
```

Jika muncul error kebijakan eksekusi di PowerShell, jalankan sekali (sebagai admin jika perlu):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Setelah aktif, prompt biasanya diawali `(myenv)`.

#### Langkah 3 — Install dependensi

```bash
pip install -r requirements.txt
```

Tunggu sampai semua paket ter-install tanpa error.

#### Langkah 4 — Siapkan PostgreSQL

1. Pastikan **PostgreSQL di laptop sudah running** (Services atau pgAdmin bisa connect ke `localhost:5432`).
2. Buat database (jika belum ada), lewat **Query Tool** di pgAdmin atau `psql`:

```sql
CREATE DATABASE python_openapi;
```

#### Langkah 5 — File `.env`

Salin contoh dan edit password sesuai PostgreSQL Anda:

**Linux / macOS:**

```bash
cp .env.example .env
```

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

Contoh isi `.env` (ganti `PASSWORD_ANDA`):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=PASSWORD_ANDA
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=python_openapi
DATABASE_URL=postgresql+psycopg2://postgres:PASSWORD_ANDA@127.0.0.1:5432/python_openapi
```

Aplikasi membaca `.env` otomatis saat start.

#### Langkah 6 — Jalankan server (auto-reload)

Pastikan virtual environment masih aktif `(myenv)`, lalu:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Jika berhasil, terminal menampilkan sekitar:

```text
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

#### Langkah 7 — Buka di browser

| Tujuan | URL |
|--------|-----|
| Swagger UI (coba API) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health / contoh endpoint | http://localhost:8000/hello |

#### Langkah 8 — Uji singkat

1. Di Swagger, buka **GET `/users`** → **Try it out** → **Execute** (awalnya bisa kosong `[]`).
2. **POST `/users`** dengan body JSON (nama, email, password).
3. **GET `/users`** lagi — data harus muncul di response **dan** di pgAdmin (`python_openapi` → Schemas → public → Tables → `users`).

#### Menghentikan server

Di terminal tempat uvicorn jalan: tekan **Ctrl+C**.

---

### Mode production (tanpa reload)

Virtual environment aktif, `.env` sudah benar:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

### Ringkasan perintah (copy-paste)

Setelah langkah 1–5 selesai, setiap kali development cukup:

**Linux / macOS:**

```bash
cd python-openapi
source myenv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Windows (PowerShell):**

```powershell
cd D:\learning\Learning_Flutter\python_openapi
.\myenv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

(`pip install` hanya wajib ulang jika `requirements.txt` berubah.)

---

## Docker

Build image:

```bash
docker build -t python-openapi .
```

Jalankan container (pastikan PostgreSQL dapat dijangkau dari container):

```bash
docker run --rm -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg2://postgres:PASSWORD@HOST:5432/python_openapi \
  python-openapi
```

---

## Docker Compose

Hanya menjalankan **API di container**; database memakai **PostgreSQL di laptop** (`host.docker.internal`).

Pastikan PostgreSQL lokal sudah jalan dan database `python_openapi` ada. Isi `.env` sesuai kredensial pgAdmin Anda.

```bash
docker compose up --build
```

| Service | Port (host) | Keterangan |
|---------|-------------|------------|
| api | 8000 | FastAPI → DB di `127.0.0.1:5432` (via `host.docker.internal` dari container) |

**pgAdmin / DBeaver:** `localhost`, port **5432**, database `python_openapi` — **sama** dengan yang dipakai Swagger/API.

Hentikan:

```bash
docker compose down
```

---

## API Reference

### CRUD User (`/users`)

Password **wajib** saat create, **opsional** saat update. Response **tidak** menyertakan password.

| Method | Endpoint | Deskripsi | Status sukses |
|--------|----------|-----------|---------------|
| POST | `/users` | Buat user baru | 201 |
| GET | `/users` | Daftar semua user | 200 |
| GET | `/users/{id}` | Detail user by ID | 200 |
| PUT | `/users/{id}` | Update user (partial) | 200 |
| DELETE | `/users/{id}` | Hapus user | 204 |

**Body create (`UserCreate`):**

```json
{
  "nama": "Asep",
  "email": "asep@example.com",
  "password": "secret123"
}
```

| Field | Aturan |
|-------|--------|
| nama | Wajib, 1–100 karakter |
| email | Wajib, format email valid, unik |
| password | Wajib, minimal 6 karakter |

**Body update (`UserUpdate`)** — semua field opsional:

```json
{
  "nama": "Asep Baru",
  "email": "asep.baru@example.com",
  "password": "passwordbaru"
}
```

**Response (`UserResponse`):**

```json
{
  "id": 1,
  "nama": "Asep",
  "email": "asep@example.com"
}
```

**Error umum:**

| Status | Pesan | Penyebab |
|--------|-------|----------|
| 400 | Email sudah terdaftar | Email duplikat |
| 404 | User tidak ditemukan | ID tidak ada |
| 422 | Validation Error | Body tidak valid |

---

### Endpoint Demo

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/hello` | Pesan hello |
| GET | `/hello/{name}` | Hello dengan nama |
| GET | `/tambah/{angka1}/{angka2}` | Penjumlahan via path |
| POST | `/tambah` | Penjumlahan via body |
| POST | `/kurang` | Pengurangan |
| POST | `/kali` | Perkalian |
| POST | `/bagi` | Pembagian (error 400 jika angka2 = 0) |

**Body operasi hitung:**

```json
{
  "angka1": 10,
  "angka2": 5
}
```

---

### Autentikasi JWT

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/token` | Login, dapatkan access token |
| GET | `/jwt-secure` | Endpoint terproteksi JWT |

**Login** (`application/x-www-form-urlencoded`):

- `username`: `asep`
- `password`: `password123`

**Response:**

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

**Akses `/jwt-secure`:** kirim header:

```
token: <access_token>
```

---

## Contoh Request (curl)

### User CRUD

```bash
# Create
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"nama":"Asep","email":"asep@example.com","password":"secret123"}'

# List
curl http://localhost:8000/users

# Detail
curl http://localhost:8000/users/1

# Update
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"nama":"Asep Updated"}'

# Delete
curl -X DELETE http://localhost:8000/users/1
```

### Operasi hitung

```bash
curl -X POST http://localhost:8000/tambah \
  -H "Content-Type: application/json" \
  -d '{"angka1":10,"angka2":5}'
```

### JWT

```bash
# Login
curl -X POST http://localhost:8000/token \
  -d "username=asep&password=password123"

# Endpoint secure (ganti TOKEN)
curl http://localhost:8000/jwt-secure \
  -H "token: TOKEN"
```

---

## Catatan Keamanan

- Ganti `SECRET_KEY` di `main.py` untuk production; lebih baik dari variabel lingkungan.
- Jangan commit file `.env` ke repository.
- Password user disimpan sebagai hash bcrypt, tidak pernah dikembalikan di response API.
- CORS saat ini `allow_origins=["*"]` — batasi ke domain spesifik di production.
- Kredensial login JWT demo (`asep` / `password123`) hanya untuk pembelajaran, bukan production.

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `could not connect to server` | Pastikan PostgreSQL berjalan dan `DATABASE_URL` benar |
| `database "python_openapi" does not exist` | Buat database dengan `CREATE DATABASE` |
| `Email sudah terdaftar` | Gunakan email lain atau hapus user lama |
| Port 8000 sudah dipakai | Gunakan port lain: `--port 8001` |
| Error driver PostgreSQL | Install ulang: `pip install psycopg2-binary` |
