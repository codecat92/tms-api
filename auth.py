from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import os
from dotenv import load_dotenv

# ─────────────────────────────
# CONFIG
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Config password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─────────────────────────────
# PASSWORD FUNCTIONS

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verifikasi password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



# ─────────────────────────────
# TOKEN FUNCTIONS

# Buat JWT token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode & validasi token
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ─────────────────────────────
# AUTENTIKASI

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token:str = Depends(oauth2_scheme),
    db:Session = Depends(get_db)
):

    #Decode Token
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code = 401,
            detail = "Token tidak valid atau sudah expired!"
        )

    # Ambil email dari token
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code = 401,
            detail = "Token tidak valid!"
        )

    #Cari user di database
    from models import User as UserModel
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise HTTPException(
            status_code = 401,
            detail = "User tidak ditemukan!"
        )

    return user
