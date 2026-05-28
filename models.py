from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, DeclarativeBase
from datetime import datetime
from database import Base
import enum

'''
Pembuatan Enum seperti di pydantic, hanya saja ini versi SQLAlchemy
'''

class LicenseTypeEnum (enum.Enum):
    A = "A"
    B1 = "B1"
    B2 = "B2"

class DriverStatusEnum (enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

'''
##### ENUM SELESAI #####
'''


'''
##### TABEL DRIVER ###
'''
class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key= True, index= True)
    name = Column (String(100), nullable = False)
    license_number = Column (String(20), nullable = False)
    license_type = Column (SAEnum(LicenseTypeEnum), nullable = False)
    license_expiry_date = Column (Date, nullable = False)
    phone = Column (String(20), nullable = False)
    status = Column (SAEnum(DriverStatusEnum), nullable = False)
    fatigue_hours = Column (Float, nullable = False)
    total_trips = Column (Integer, nullable = False, default = 0)
    incident_count = Column (Integer, nullable = False, default = 0)
    created_at= Column (DateTime, default = datetime.now)

'''
#### TABEL ROUTE ####
'''

class Route(Base):
    __tablename__= "route"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable = False)
    origin = Column(String(100), nullable = False)
    destination = Column(String(100), nullable = False)
    zone = Column(String(50), nullable = False)
    distance_km = Column (Float, nullable = False)
    estimated_duration_hours = Column (Float, nullable = False)
    base_cost = Column (Float, nullable = False)
    created_at = Column (DateTime, default = datetime.now)


'''
### TABEL SHIPMENT ###
'''

class Shipment(Base):
    __tablename__ = "shipment"

    id                  = Column(Integer, primary_key=True, index=True)
    reference           = Column(String(50), nullable=False, unique=True)
    fleet_id            = Column(Integer, nullable=False)
    driver_id           = Column(Integer, ForeignKey("driver.id"), nullable=False)
    codriver_id         = Column(Integer, ForeignKey("driver.id"), nullable=True)
    route_id            = Column(Integer, ForeignKey("route.id"), nullable=False)
    state               = Column(String(20), nullable=False, default="draft")
    scheduled_date      = Column(DateTime, nullable=False)
    actual_departure    = Column(DateTime, nullable=True)
    actual_arrival      = Column(DateTime, nullable=True)
    total_weight_kg     = Column(Float, nullable=False)
    total_volume_m3     = Column(Float, nullable=False)
    vso_rate            = Column(Float, nullable=False)
    eta                 = Column(DateTime, nullable=True)
    created_at          = Column(DateTime, default=datetime.now)

    #relasi ke driver dan route
    driver = relationship("Driver", foreign_keys=[driver_id])
    codriver = relationship("Driver", foreign_keys=[codriver_id])
    route = relationship("Route")