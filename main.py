from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime, date


app = FastAPI(
    title = "TMS API",
    description = "Transportation Management System",
    version = "1.0.0"
)

@app.get("/")
def root():
    return {"message" : "TMS API is running!"}



'''
TIPE ENUM MULAI
'''

class LicenseType(str, Enum):
    A = "A" # sim untuk kendaraaan ringan
    B1 = "B1" # sim untuk  kendaraan berat non - trailer
    B2 = "B2" # sim untuk kendaraan berat dengan trailer

#class enum untuk driver_status
class DriverStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


#class enum untuk shipment
class ShipmentState(str, Enum):
    DRAFT ="draft"
    CONFIRMED= "confirmed"
    IN_TRANSIT ="in_transit"
    DELIVERED= "delivered"
    CANCELLED= "cancelled"

'''
TIPE ENUM SELESAI
'''


'''
ENTITIES CLASS MULAI
'''

'''
    ######
    DRIVER
    ######
'''
# Model untuk CREATE — data yang user kirim


class DriverCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    license_number: str = Field(min_length=5)
    license_type: LicenseType
    license_expiry_date: date
    phone: str = Field(pattern=r'^08[0-9]{8,11}$')
    fatigue_hours: float = Field(ge=0, le=8)

# Model untuk RESPONSE — data yang kita kirim balik ke user
class DriverResponse(BaseModel):
    id: int
    name: str
    license_type: LicenseType
    license_expiry_date: date
    status: DriverStatus
    total_trips: int
    model_config = {"from_attributes": True}

# Model lengkap Driver — internal
class Driver(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=100)
    license_number: str        # ← tidak ada di DriverResponse!
    license_type: LicenseType
    license_expiry_date: date
    phone: str                 # ← tidak ada di DriverResponse!
    status: DriverStatus
    fatigue_hours: float
    total_trips: int
    incident_count: int        # ← tidak ada di DriverResponse!
    created_at: datetime


'''
    ######
    ROUTE
    ######
'''

#Model Lengkap Route
class Route(BaseModel):
    id: int = Field (ge =0)
    name: str = Field (min_length = 3)
    origin:str
    destination:str
    zone:str
    distance_km:float = Field (ge = 0)
    estimated_duration_hours:float = Field(gt=0)
    base_cost:float = Field(ge=0)
    created_at: datetime

#Response Model Route
class RouteResponse(BaseModel):
    id: int = Field (ge =0)
    name: str = Field (min_length = 3)
    origin:str
    destination:str
    zone:str
    distance_km:float = Field (ge = 0)
    estimated_duration_hours:float = Field(gt=0)
    model_config = {"from_attributes": True}



'''
    ######
    SHIPMENT
    ######
'''

#Model Lengkap Shipment

class Shipment(BaseModel):
    id: int
    reference: str = Field(min_length=5)
    fleet_id: int
    driver: Driver
    codriver: Optional[Driver] = None
    route: Route
    state: ShipmentState
    scheduled_date: datetime
    actual_departure: Optional [datetime] = None
    actual_arrival: Optional [datetime] = None
    total_weight_kg: float = Field (ge=0, le=30000, description= "Tidak boleh negatif, harus setara atau kurang dari 30000")
    total_volume_m3: float = Field (ge=0, description ="Tidak boleh negatif")
    vso_rate: float = Field (ge=0, le=100, description="Nilai hanya boleh antara 0 -100")
    eta: Optional [datetime] = None
    created_at: datetime

#Response Model Shipment
class ShipmentResponse(BaseModel):
    id: int
    reference: str = Field(min_length=5)
    driver: DriverResponse
    codriver: Optional[DriverResponse] = None
    route: RouteResponse
    state: ShipmentState
    scheduled_date: datetime
    eta: Optional [datetime] = None
    model_config = {"from_attributes": True}

    
'''
ENTITIES CLASS SELESAI
'''


drivers_db = [
    Driver(
        id=1,
        name="Budi Santoso",
        license_number="SIM-B2-123456",
        license_type=LicenseType.B2,
        license_expiry_date="2027-12-31",
        phone="081234567890",
        status=DriverStatus.ACTIVE,
        fatigue_hours=4.5,
        total_trips=120,
        incident_count=0,
        created_at="2024-01-15 08:00:00"
    ),
    Driver(
        id=2,
        name="Fajar Anugrah",
        license_number="SIM-B2-66666",
        license_type=LicenseType.B2,
        license_expiry_date="2026-11-30",
        phone="081878456790",
        status=DriverStatus.ACTIVE,
        fatigue_hours=3.0,
        total_trips=85,
        incident_count=1,
        created_at="2024-02-01 08:00:00"
    )
]


#--Endpoint GET semua driver ---
'''
AMBIL SEMUA DATA DRIVER
'''
@app.get("/drivers", response_model=list[DriverResponse])
def get_drivers():
    return drivers_db

'''
AMBIL SALAH SATU DATA DRIVER
'''
@app.get("/drivers/{driver_id}", response_model = DriverResponse)
def get_drivers(driver_id: int):
    for driver in drivers_db:
        if driver.id == driver_id:
            return driver


    raise HTTPException(
        status_code=404,
        detail=f"Driver dengan ID {driver_id} tidak ditemukan"
    )



'''
TRYING POST METHOD
'''

@app.post("/drivers", response_model=DriverResponse, status_code=201)
def create_driver(data:DriverCreate):
    #kita buat objek baru untuk driver baru!
    new_driver = Driver(
        id = len(drivers_db) + 1, #untuk autoincrement id 
        name = data.name,
        license_number=data.license_number,
        license_type=data.license_type,
        license_expiry_date=data.license_expiry_date,
        phone=data.phone,
        status=DriverStatus.ACTIVE,   # default active
        fatigue_hours=data.fatigue_hours,
        total_trips=0,                # mulai dari 0
        incident_count=0,             # mulai dari 0
        created_at=datetime.now()     # otomatis sekarang 
    )

    drivers_db.append(new_driver) # simpan/tambahkan ke array database dummy
    return new_driver