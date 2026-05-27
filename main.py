from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Driver as DriverModel
from schemas import DriverCreate, DriverResponse, DriverStatus
from datetime import datetime

'''
#### CREATE TABLE OTOMATIS SAAT SERVER JALAN #####
'''
Base.metadata.create_all(bind=engine)

app= FastAPI(
    title="TMS API",
    description = "Transportation Management System",
    version="1.0.0"
)

@app.get("/")
def root():
    return{"message":"TMS API is running!"}

'''
##### GET SEMUA DRIVER
'''

@app.get("/drivers", response_model=DriverResponse)
def get_drivers(db:Session = Depends(get_db)):
    return db.query(DriverModel).all()


'''
##### GET SATU DRIVER #####
'''
@app.get("/drivers/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id:int, db:Session = Depends (get_db)):
    driver = db.query(DriverModel).filter(DriverModel.id ==driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=404,
            detail= f"Driver dengan ID {driver_id} tidak ditemukan!"
        )
    return driver



'''
##### POST DRIVER BARU #####
'''

@app.post("/drivers", response_model = DriverResponse, status_code= 201)
def create_driver (data:DriverCreate, db: Session = Depends(get_db)):
    new_driver = DriverModel(
        name = data.name,
        license_number = data.license_number,
        license_type = data.license_type,
        license_expiry_date = data.license_expiry_date,
        phone = data.phone,
        status = DriverStatus.ACTIVE,
        fatigue_hours = data.fatigue_hours,
        total_trips = 0,
        incident_count = 0,
        created_at = datetime.now()
    )
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver