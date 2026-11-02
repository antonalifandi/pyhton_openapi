# Panduan Singkat — Praktikum Python OpenAPI (FastAPI + PostgreSQL)

**Repo:** https://github.com/antonalifandi/pyhton_openapi.git  
**Tujuan:** Clone → setup DB → jalankan API → uji lewat Swagger & DBeaver.

---

## A. Unduh dulu (jika belum punya)

| Software | Fungsi | Link unduh |
|----------|--------|------------|
| **Python 3.12+** | Menjalankan API | https://www.python.org/downloads/ — centang **Add Python to PATH** saat install |
| **PostgreSQL 14+** | Database | https://www.postgresql.org/download/windows/ — catat **password user `postgres`** saat install |
| **DBeaver Community** | Lihat & query database (gratis) | https://dbeaver.io/download/ |
| **Git** (opsional) | Clone repo | https://git-scm.com/download/win |

Setelah PostgreSQL ter-install, pastikan service **PostgreSQL** **Running** (Windows: *Services* → *postgresql*).

---

## B. Clone proyek

**PowerShell:**

```powershell
cd D:\learning
git clone https://github.com/antonalifandi/pyhton_openapi.git
cd pyhton_openapi
```

(Tanpa Git: download ZIP dari GitHub → extract → buka folder di terminal.)

---

## C. Virtual environment & dependensi Python

```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
```

Jika error kebijakan PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Lalu:

```powershell
pip install -r requirements.txt
```

Prompt harus diawali `(myenv)`.

---

## D. Buat database `python_openapi`

### Opsi 1 — DBeaver (disarankan untuk pemula)

1. Buka **DBeaver** → **New Database Connection** → pilih **PostgreSQL**.
2. Host: `localhost`, Port: `5432`, Database: `postgres`, User: `postgres`, Password: (saat install PostgreSQL).
3. **Test Connection** → **Finish**.
4. Klik kanan koneksi → **SQL Editor** → **New SQL Script**, jalankan:

```sql
CREATE DATABASE python_openapi;
```

5. Refresh → buka database **`python_openapi`**.

### Opsi 2 — psql

```powershell
psql -U postgres -c "CREATE DATABASE python_openapi;"
```

---

## E. File `.env`

```powershell
Copy-Item .env.example .env
```

Edit `.env` — ganti `PASSWORD_ANDA` dengan password PostgreSQL Anda:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=PASSWORD_ANDA
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=python_openapi
DATABASE_URL=postgresql+psycopg2://postgres:PASSWORD_ANDA@127.0.0.1:5432/python_openapi
```

---

## F. Jalankan API

Virtual environment aktif `(myenv)`:

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Berhasil jika muncul: `Application startup complete.`  
Buka browser: **http://localhost:8000/docs**

Stop server: **Ctrl+C** di terminal.

---

## G. Uji singkat (Swagger)

1. **GET `/users`** → Try it out → Execute → awalnya `[]`.
2. **POST `/users`** → body contoh:

```json
{
  "nama": "Asep",
  "email": "asep@example.com",
  "password": "secret123"
}
```

3. **GET `/users`** lagi → data muncul di response.
4. Di **DBeaver**: database `python_openapi` → **Schemas** → **public** → **Tables** → **`users`** → lihat baris data.

---

## H. Kesalahan umum

| Gejala | Perbaikan |
|--------|-----------|
| `could not connect to server` | PostgreSQL belum jalan / password `.env` salah |
| `database "python_openapi" does not exist` | Jalankan `CREATE DATABASE python_openapi;` |
| Port 8000 dipakai | `uvicorn main:app --port 8001 --reload` |
| `Activate.ps1` ditolak | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |

---

## I. Setiap kali praktik (ringkas)

```powershell
cd D:\learning\pyhton_openapi
.\myenv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

(`pip install -r requirements.txt` hanya jika `requirements.txt` berubah.)

---

**Dokumentasi lengkap:** lihat `README.MD` di repo yang sama.
