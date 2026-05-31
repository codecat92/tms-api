from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime, date

# ─────────────────
# ENUM
# ─────────────────

class LicenseType(str, Enum):
    A  = "A"
    B1 = "B1"
    B2 = "B2"

class DriverStatus(str, Enum):
    ACTIVE    = "ACTIVE"
    INACTIVE  = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class ShipmentState(str, Enum):
    DRAFT      = "draft"
    CONFIRMED  = "confirmed"
    IN_TRANSIT = "in_transit"
    DELIVERED  = "delivered"
    CANCELLED  = "cancelled"

# ─────────────────
# DRIVER
# ─────────────────

class DriverCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    license_number: str = Field(min_length=5)
    license_type: LicenseType
    license_expiry_date: date
    phone: str = Field(pattern=r'^08[0-9]{8,11}$')
    fatigue_hours: float = Field(ge=0, le=8)

class DriverUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    license_expiry_date: Optional[date] = None
    fatigue_hours: Optional[float] = Field(default=None, ge=0, le=8)
    status: Optional[DriverStatus] = None

class DriverResponse(BaseModel):
    id: int
    name: str
    license_number: str
    license_type: LicenseType
    license_expiry_date: date
    phone:str
    status: DriverStatus
    fatigue_hours:float
    total_trips: int
    model_config = {"from_attributes": True}

# ─────────────────
# ROUTE
# ─────────────────

class Route(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(min_length=3)
    origin: str
    destination: str
    zone: str
    distance_km: float = Field(ge=0)
    estimated_duration_hours: float = Field(gt=0)
    base_cost: float = Field(ge=0)
    created_at: datetime
    model_config = {"from_attributes": True}

class RouteCreate(BaseModel):
    name: str = Field(min_length=3)
    origin: str
    destination: str
    zone: str
    distance_km: float = Field(gt=0)
    estimated_duration_hours: float = Field(gt=0)
    base_cost: float = Field(gt=0)

class RouteUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    origin: Optional[str] = None
    destination: Optional[str] = None
    zone: Optional[str] = None
    distance_km: Optional[float] = Field(default=None, gt=0)
    estimated_duration_hours: Optional[float] = Field(default=None, gt=0)
    base_cost: Optional[float] = Field(default=None, gt=0)

class RouteResponse(BaseModel):
    name: str
    origin: str
    destination: str
    zone: str
    distance_km: float
    estimated_duration_hours: float
    base_cost: Optional[float] = Field(default=None, gt=0)
    model_config = {"from_attributes": True}

# ─────────────────
# SHIPMENT
# ─────────────────

class ShipmentCreate(BaseModel):
    reference: str = Field(min_length=5)
    fleet_id: int
    driver_id: int
    codriver_id: Optional[int] = None
    route_id: int
    scheduled_date: datetime
    total_weight_kg: float = Field(ge=0, le=30000)
    total_volume_m3: float = Field(ge=0)
    vso_rate: float = Field(ge=0, le=100)

class ShipmentUpdate(BaseModel):
    state: Optional[ShipmentState] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    eta: Optional[datetime] = None
    vso_rate: Optional[float] = Field(default=None, ge=0, le=100)


class ShipmentResponse(BaseModel):
    id: int
    reference: str
    driver: DriverResponse          # ← tetap pakai DriverResponse (ada field sensitif)
    codriver: Optional[DriverResponse] = None
    route: Route                    # ← ganti RouteResponse → Route (semua field)
    state: ShipmentState
    scheduled_date: datetime
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    eta: Optional[datetime] = None
    model_config = {"from_attributes": True}


# ─────────────────
# USER
# ─────────────────

class UserCreate(BaseModel):
    email:str
    password:str = Field(min_length = 8, max_length=72)
    full_name:str = Field(min_length = 3)

class UserResponse(BaseModel):
    id:int
    email:str
    full_name:str
    is_active:int
    model_config ={"from_attributes":True}

class LoginRequest(BaseModel):
    email:str
    password:str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ─────────────────
# FLEET
# ─────────────────

class FleetStatus(str, Enum):
    AVAILABLE   = "available"
    IN_USE      = "in_use"
    MAINTENANCE = "maintenance"

class FleetCreate(BaseModel):
    plate_number: str = Field(min_length=3, max_length=20)
    vehicle_type: str = Field(min_length=3)
    capacity_kg: float = Field(gt=0)
    status: FleetStatus = FleetStatus.AVAILABLE

class FleetUpdate(BaseModel):
    vehicle_type: Optional[str] = Field(default=None, min_length=3)
    capacity_kg: Optional[float] = Field(default=None, gt=0)
    status: Optional[FleetStatus] = None

class FleetResponse(BaseModel):
    id: int
    plate_number: str
    vehicle_type: str
    capacity_kg: float
    status: FleetStatus
    created_at: datetime
    model_config = {"from_attributes": True}