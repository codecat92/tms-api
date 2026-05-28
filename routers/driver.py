from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Driver as DriverModel
from schemas import DriverCreate, DriverResponse, DriverStatus, DriverUpdate
from datetime import datetime


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)

# GET SEMUA DRIVER
@router.get("", response_model=list[DriverResponse])
def get_drivers(db: Session = Depends(get_db)):
    return db.query(DriverModel).all()

# GET SATU DRIVER
@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(DriverModel).filter(DriverModel.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=404,
            detail=f"Driver dengan ID {driver_id} tidak ditemukan!"
        )
    return driver

# POST DRIVER BARU
@router.post("", response_model=DriverResponse, status_code=201)
def create_driver(data: DriverCreate, db: Session = Depends(get_db)):
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

# UPDATE DRIVER
@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: int, data: DriverUpdate, db: Session = Depends(get_db)):
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

# DELETE DRIVER
@router.delete("/{driver_id}", status_code=204)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(DriverModel).filter(DriverModel.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=404,
            detail=f"Driver dengan ID {driver_id} tidak ditemukan!"
        )
    db.delete(driver)
    db.commit()
    return None