from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Driver as DriverModel, User as UserModel
from schemas import DriverCreate, DriverResponse, DriverStatus, DriverUpdate, LicenseType
from datetime import datetime
from auth import get_current_user
from typing import Optional



router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)

# GET SEMUA DRIVER
@router.get("", response_model=list[DriverResponse])
def get_drivers(
    #query parameters, semuanya opsional
    status:Optional[DriverStatus] = None, #filter untuk status driver
    license_type:Optional[LicenseType] = None, #filter untuk jenis SIM
    name:Optional[str] = None, #search by name

    # Pagination parameters
    page: int = 1,        # halaman berapa? default halaman 1
    limit: int = 10,      # berapa data per halaman? default 10

    #dependencies
    db: Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)):  

    query = db.query(DriverModel)
    #Apply filter kalau ada
    if status is not None:
        query = query.filter(DriverModel.status == status)
    
    if license_type is not None:
        query = query.filter(DriverModel.license_type == license_type)
    
    if name is not None:
        # ilike = case insensitive search
        # %name% = contains, bukan exact match
        query = query.filter(DriverModel.name.ilike(f"%{name}%"))

    # Apply pagination
    offset = (page - 1) * limit   # hitung skip berapa data
    return query.all()
    """
    Ambil semua data driver yang terdaftar di sistem TMS.
    dengan fitur filter yang opsional
    """



# GET SATU DRIVER
@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(
    driver_id: int, db: Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    driver = db.query(DriverModel).filter(DriverModel.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=404,
            detail=f"Driver dengan ID {driver_id} tidak ditemukan!"
        )
    return driver
    """
    Ambil detail satu driver berdasarkan ID.
    """





# POST DRIVER BARU
@router.post("", response_model=DriverResponse, status_code=201)
def create_driver(
    data: DriverCreate, db: Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    new_driver = DriverModel(
        name=data.name,
        license_number=data.license_number,
        license_type=data.license_type,
        license_expiry_date=data.license_expiry_date,
        phone=data.phone,
        status=DriverStatus.ACTIVE,
        fatigue_hours=data.fatigue_hours,
        total_trips=0,
        incident_count=0,
        created_at=datetime.now()
    )
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver
    """
    Tambahkan driver baru ke sistem TMS.
    """




# UPDATE DRIVER
@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: int, data: DriverUpdate, db: Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    driver = db.query(DriverModel).filter(DriverModel.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=404,
            detail=f"Driver dengan ID {driver_id} tidak ditemukan!"
        )
    if data.name is not None:
        driver.name = data.name
    if data.phone is not None:
        driver.phone = data.phone
    if data.license_expiry_date is not None:
        driver.license_expiry_date = data.license_expiry_date
    if data.fatigue_hours is not None:
        driver.fatigue_hours = data.fatigue_hours
    if data.status is not None:
        driver.status = data.status

    db.commit()
    db.refresh(driver)
    return driver
    """
    Update data driver berdasarkan ID.
    Hanya field yang dikirim yang akan diupdate.
    """


# DELETE DRIVER
@router.delete("/{driver_id}", status_code=204)
def delete_driver(
    driver_id: int, db: Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    driver = db.query(DriverModel).filter(DriverModel.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=404,
            detail=f"Driver dengan ID {driver_id} tidak ditemukan!"
        )
    db.delete(driver)
    db.commit()
    return None
    """
    Hapus data driver berdasarkan ID.
    """




# FATIGUE ALERT
@router.get("/alerts/fatigue", response_model=list[DriverResponse])
def get_fatigue_alerts(
    db: Session = Depends(get_db),
    _: UserModel = Depends(get_current_user)
):
    """
    Ambil daftar driver yang fatigue hours nya melebihi 6 jam.
    Digunakan untuk monitoring keselamatan pengemudi.
    """
    return db.query(DriverModel).filter(DriverModel.fatigue_hours > 6).all()