from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User as UserModel
from schemas import UserCreate, UserResponse, TokenResponse
from auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


#REGISTRASI USER BARU
@router.post("/register", response_model = UserResponse, status_code=201)
def register(data:UserCreate, db:Session = Depends(get_db)):
    #cek apakah email sudah ada
    existing_user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail = "Email sudah terdaftar!"
        )
    #hash password sebelum disimpan
    new_user = UserModel(
        email = data.email,
        password = hash_password(data.password),
        full_name = data.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#LOGIN
@router.post("/login", response_model=TokenResponse)
def login(
    data:OAuth2PasswordRequestForm = Depends()
, db:Session = Depends(get_db)
):
    #cari user berdasarkan email
    user = db.query(UserModel).filter(UserModel.email == data.username).first()
    if not user:
        raise HTTPException(
            status_code = 401,
            detail= "Email atau password salah!"
        )

    #verifikasi password
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code = 401,
            detail = "Email atau password salah!"
        )

    #buat token
    token = create_access_token(data={"sub": user.email})
    return {"access_token" : token, "token_type" : "bearer"}