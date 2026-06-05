from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel

from database import Base, engine
from routers import users as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only; production isi origin spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router.router)

# Konfigurasi JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
# Model untuk operasi hitung angka
class HitungAngka(BaseModel):
    angka1: int
    angka2: int

# 1. Endpoint dasar
@app.get("/hello")
def read_hello():
    return {"message": "Hello, Open API!"}
# 2. Endpoint dinamis
@app.get("/hello/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}
    
#endpoint untuk penjumlahan angka dengan parameter path (angka1 dan angka2)
@app.get("/tambah/{angka1}/{angka2}")
def tambah(angka1: int, angka2: int):
    return {"hasil": angka1 + angka2}
#endpoint untuk penjumlahan angka dengan parameter body (angka1 dan angka2)
@app.post("/tambah")
def tambah(data: HitungAngka):
    hasil = data.angka1 + data.angka2
    return {"hasil": hasil}
#endpoint untuk pengurangan angka dengan parameter body (angka1 dan angka2)
@app.post("/kurang")
def kurang(data: HitungAngka):
    hasil = data.angka1 - data.angka2
    return {"hasil": hasil}
#endpoint untuk perkalian angka dengan parameter body (angka1 dan angka2)
@app.post("/kali")
def kali(data: HitungAngka):
    hasil = data.angka1 * data.angka2
    return {"hasil": hasil}
#endpoint untuk pembagian angka dengan parameter body (angka1 dan angka2)
@app.post("/bagi")
def bagi(data: HitungAngka):
    if data.angka2 == 0:
        raise HTTPException(status_code=400, detail="angka2 cannot be zero")
    hasil = data.angka1 /  data.angka2
    return {"hasil": hasil}

# # 3. Autentikasi dengan API Key
# @app.get("/secure-data")
# def secure_data(x_api_key: str = Header(...)):
#     if x_api_key != "mysecretkey":
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     return {"data": "This is protected data"}

# 4. Endpoint login JWT
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "asep" or form_data.password != "password123":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": form_data.username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# 5. Endpoint dengan proteksi JWT
@app.get("/jwt-secure")
def jwt_secure(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"data": f"Secure data for {payload['sub']}"}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

