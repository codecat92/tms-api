from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Driver as DriverModel, User as UserModel
from schemas import DriverCreate, DriverResponse, DriverStatus, DriverUpdate
from datetime import datetime
from auth import get_current_user



router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)

# GET SEMUA DRIVER
@router.get("", response_model=list[DriverResponse])
def get_drivers(
    db: Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)):  
    return db.query(DriverModel).all()
    """
    Ambil semua data driver yang terdaftar di sistem TMS.
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