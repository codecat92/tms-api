from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum as SAEnum
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
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

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
    fatigue_hours = Column (Float, nullable = False),
    total_trips = Column (Integer, nullable = False, Default = 0),
    incident_count = Column (Integer, nullable = False, Default = 0),
    created_at= Column (DateTime, default = datetime.now)