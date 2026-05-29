from fastapi import FastAPI
from database import engine, Base
from routers import driver, route, shipment,auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TMS API",
    description="""
    ## Transportation Management System API

Backend API untuk mengelola operasional transportasi logistik.

### Features
- 🚗 **Driver** — Manajemen data pengemudi
- 🗺️ **Route** — Manajemen rute pengiriman
- 📦 **Shipment** — Manajemen pengiriman barang
- 🔐 **Authentication** — JWT based authentication

### How to Use
1. **Register** — Buat akun baru di `/auth/register`
2. **Login** — Login di `/auth/login` untuk dapat token
3. **Authorize** — Klik tombol **Authorize** di atas, masukkan username & password
4. **Explore** — Semua endpoint siap digunakan!

### Tech Stack
- **FastAPI** — Modern Python web framework
- **PostgreSQL** — Database
- **SQLAlchemy** — ORM
- **JWT** — Authentication
    """,
    version="1.0.0",
    contact={
        "name": "TMS API Support",
        "email": "hello@tms.com"
    }
)
    


@app.get("/")
def root():
    return {"message": "TMS API is running!"}

# Daftarkan semua router
app.include_router(driver.router)
app.include_router(route.router)
app.include_router(shipment.router)
app.include_router(auth.router)