from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from database import get_db
from models import Fleet as FleetModel, User as UserModel
from schemas import FleetCreate, FleetUpdate, FleetResponse, FleetStatus
from datetime import datetime
from auth import get_current_user

router = APIRouter(
    prefix="/fleet",
    tags=["Fleet"]
)

# GET SEMUA FLEET
@router.get("", response_model=list[FleetResponse])
def get_fleets(
    db: Session = Depends(get_db),
    _: UserModel = Depends(get_current_user)
):
    """Ambil semua data armada kendaraan yang terdaftar."""
    return db.query(FleetModel).all()


# GET SATU FLEET
@router.get("/{fleet_id}", response_model=FleetResponse)
def get_fleet(
    fleet_id: int,
    db: Session = Depends(get_db),
    _: UserModel = Depends(get_current_user)
):
    """Ambil detail satu kendaraan berdasarkan ID."""
    fleet = db.query(FleetModel).filter(FleetModel.id == fleet_id).first()
    if not fleet:
        raise HTTPException(
            status_code=404,
            detail=f"Kendaraan dengan ID {fleet_id} tidak ditemukan!"
        )
    return fleet


# POST FLEET BARU
@router.post("", response_model=FleetResponse, status_code=201)
def create_fleet(
    data: FleetCreate,
    db: Session = Depends(get_db),
    _: UserModel = Depends(get_current_user)
):
    """Tambahkan kendaraan baru ke sistem TMS."""
    # Cek plate number sudah ada belum
    existing = db.query(FleetModel).filter(FleetModel.plate_number == data.plate_number).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Plat nomor {data.plate_number} sudah terdaftar!"
        )
    new_fleet = FleetModel(
        plate_number=data.plate_number,
        vehicle_type=data.vehicle_type,
        capacity_kg=data.capacity_kg,
        status=data.status,
        created_at=datetime.now()
    )
    db.add(new_fleet)
    db.commit()
    db.refresh(new_fleet)
    return new_fleet


# UPDATE FLEET
@router.put("/{fleet_id}", response_model=FleetResponse)
def update_fleet(
    fleet_id: int,
    data: FleetUpdate,
    db: Session = Depends(get_db),
    _: UserModel = Depends(get_current_user)
):
    """Update data kendaraan berdasarkan ID."""
    fleet = db.query(FleetModel).filter(FleetModel.id == fleet_id).first()
    if not fleet:
        raise HTTPException(
            status_code=404,
            detail=f"Kendaraan dengan ID {fleet_id} tidak ditemukan!"
        )
    if data.vehicle_type is not None:
        fleet.vehicle_type = data.vehicle_type
    if data.capacity_kg is not None:
        fleet.capacity_kg = data.capacity_kg
    if data.status is not None:
        fleet.status = data.status

    db.commit()
    db.refresh(fleet)
    return fleet


# DELETE FLEET
@router.delete("/{fleet_id}", status_code=204)
def delete_fleet(
    fleet_id: int,
    db: Session = Depends(get_db),
    _: UserModel = Depends(get_current_user)
):
    """Hapus data kendaraan berdasarkan ID."""
    fleet = db.query(FleetModel).filter(FleetModel.id == fleet_id).first()
    if not fleet:
        raise HTTPException(
            status_code=404,
            detail=f"Kendaraan dengan ID {fleet_id} tidak ditemukan!"
        )
    db.delete(fleet)
    db.commit()
    return Response(status_code=204)