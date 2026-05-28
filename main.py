from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Driver as DriverModel
from schemas import DriverCreate, DriverResponse, DriverStatus, DriverUpdate
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

@app.get("/drivers", response_model=list[DriverResponse]) #Endpoint ini akan return BANYAK driver, dan setiap driver harus sesuai template DriverResponse
def get_drivers(db:Session = Depends(get_db)): # means => sebelum fungsi get_drivers di jalankan, minta izin koneksi ke database (Depends(get_db)), lalu kita simpan ke variable 'db' 
    return db.query(DriverModel).all() #means => 'db' yang sudah punya akses ke database, melakukan request/query untuk semua data (.all)
    # baris kode yang di atas ini ORM yang jika di terjemahkan ke SQL akan menjadi SELECT * FROM driver;

'''
##### GET SATU DRIVER #####
'''
@app.get("/drivers/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id:int, db:Session = Depends (get_db)):
    driver = db.query(DriverModel).filter(DriverModel.id ==driver_id).first() # ini ORM, .filter(DriverModel.id == driver_id) artinya WHERE id = driver_id di SQL , .first() artinya LIMIT di sql
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

'''
#### UPDATE DRIVER ####
'''
@app.put("/drivers/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id:int, data:DriverUpdate, db:Session = Depends(get_db)):
    #cari driver dulu
    driver = db.query(DriverModel).filter(DriverModel.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code = 404,
            detail = f"Driver dengan ID {driver_id} tidak ditemukan!"
            )
    #hanya update field yang dikirim user
    if data.name is not None:
        driver.name = data.name                          # ← driver dapat dari data
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


'''
### DELETE DRIVER ###
'''

@app.delete("/drivers/{driver_id}", status_code = 204)
def delete_driver(driver_id:int, db:Session = Depends(get_db)):
    #cari driver
    driver = db.query(DriverModel).filter(DriverModel.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code =404,
            detail=f"Driver dengan ID {driver_id} tidak ditemukan!"
        )

    #hapus driver dari database
    db.delete(driver)
    db.commit()
    return None 