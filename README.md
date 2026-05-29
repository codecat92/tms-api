# 🚛 TMS API — Transportation Management System

Backend API untuk sistem manajemen transportasi, dibangun dengan FastAPI dan PostgreSQL.

## 🛠️ Tech Stack

- **FastAPI** — Modern Python web framework
- **PostgreSQL** — Database
- **SQLAlchemy** — ORM
- **Pydantic** — Data validation
- **JWT** — Authentication

## 📁 Project Structure

```
tms-api/
├── main.py          # Entry point & app setup
├── database.py      # Database connection
├── models.py        # SQLAlchemy models (database tables)
├── schemas.py       # Pydantic models (data validation)
├── auth.py          # JWT authentication helpers
└── routers/
    ├── auth.py      # Register & login endpoints
    ├── driver.py    # Driver CRUD endpoints
    ├── route.py     # Route CRUD endpoints
    └── shipment.py  # Shipment CRUD endpoints
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL

### Installation

1. Clone repository
```bash
git clone https://github.com/codecat92/tms-api.git
cd tms-api
```

2. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-dotenv python-multipart bcrypt==4.0.1
```

3. Setup environment variables
```bash
cp .env.example .env
# Edit .env dengan kredensial PostgreSQL lo
```

4. Run server
```bash
uvicorn main:app --reload
```

5. Buka dokumentasi API
```
http://localhost:8000/docs
```

## 📌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register user baru |
| POST | `/auth/login` | Login & dapat JWT token |

### Driver
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/drivers` | Ambil semua driver |
| GET | `/drivers/{id}` | Ambil satu driver |
| POST | `/drivers` | Tambah driver baru |
| PUT | `/drivers/{id}` | Update driver |
| DELETE | `/drivers/{id}` | Hapus driver |

### Route
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/routes` | Ambil semua route |
| GET | `/routes/{id}` | Ambil satu route |
| POST | `/routes` | Tambah route baru |
| PUT | `/routes/{id}` | Update route |
| DELETE | `/routes/{id}` | Hapus route |

### Shipment
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/shipments` | Ambil semua shipment |
| GET | `/shipments/{id}` | Ambil satu shipment |
| POST | `/shipments` | Buat shipment baru |
| PUT | `/shipments/{id}` | Update shipment |
| DELETE | `/shipments/{id}` | Hapus shipment |

## 🔐 Authentication

Semua endpoint kecuali `/auth/register` dan `/auth/login` membutuhkan JWT token.

1. Register atau login untuk mendapat token
2. Klik tombol **Authorize** di Swagger UI
3. Masukkan username & password
4. Semua request berikutnya otomatis menggunakan token!

## 📝 Environment Variables

```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```