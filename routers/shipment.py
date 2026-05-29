from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Shipment as ShipmentModel, User as UserModel
from schemas import ShipmentCreate, ShipmentUpdate, ShipmentResponse, ShipmentState
from datetime import datetime
from auth import get_current_user
from typing import Optional

router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"]
)

'''
ENDPOINTS
'''

#BACA SEMUA SHIPMENT
@router.get("", response_model= list[ShipmentResponse])
def get_shipment(
    #query parameters (opsional)
    state: Optional[ShipmentState] = None,
    driver_id: Optional[int] = None,
    route_id: Optional[int] = None,



    #dependencies
    db:Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)):


    """
    Ambil semua shipment.
    Bisa difilter by state, driver_id, atau route_id.
    
    Contoh:
    - /shipments?state=in_transit
    - /shipments?driver_id=1
    - /shipments?route_id=2
    """

    query = db.query(ShipmentModel)

    if state is not None:
        query = query.filter(ShipmentModel.state.ilike(f"%{state}$"))
    if driver_id is not None:
        query = query.filter(ShipmentModel.driver_id == driver_id)
    if route_id is not None:
        query = query.filter(ShipmentModel.route_id == route_id)


    return query.all()
    """
    Ambil semua data shipment yang terdaftar di sistem TMS.
    """



#MENAMBAHKAN SHIPMENT
@router.post("", response_model= ShipmentResponse, status_code=201)
def create_shipment(
    data:ShipmentCreate,
    db:Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    new_shipment = ShipmentModel(
        reference = data.reference,
        fleet_id = data.fleet_id,
        driver_id=data.driver_id,       # ← cukup ID, bukan objek!
        codriver_id=data.codriver_id,
        route_id=data.route_id,
        state="draft",                   # ← default draft
        scheduled_date=data.scheduled_date,
        total_weight_kg=data.total_weight_kg,
        total_volume_m3=data.total_volume_m3,
        vso_rate=data.vso_rate,
        created_at=datetime.now()
    )

    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)
    return new_shipment
    """
    Tambahkan driver baru ke sistem TMS.
    """




#EDIT SHIPMENT
@router.put("/{shipment_id}", response_model=ShipmentResponse)
def update_shipment(
    shipment_id:int,
    data:ShipmentUpdate,
    db:Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    
    shipment = db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code = 404,
            detail = f"Shipment dengan id {shipment_id} tidak ditemukan!"
        )
    if data.state is not None:
        shipment.state = data.state
    if data.actual_departure is not None:
        shipment.actual_departure = data.actual_departure
    if data.actual_arrival is not None:
        shipment.actual_arrival = data.actual_arrival
    if data.eta is not None:
        shipment.eta = data.eta
    if data.vso_rate is not None:
        shipment.vso_rate = data.vso_rate

    db.commit()
    db.refresh(shipment)
    return shipment
    """
    Update data shipment berdasarkan ID.
    Hanya field yang dikirim yang akan diupdate.
    """





#DELETE SHIPMENT
@router.delete("/{shipment_id}", status_code=204)
def delete_shipment(
    shipment_id:int,
    db:Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    shipment = db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code = 404,
            detail = f"Shipment dengan ID {shipment_id} tidak ditemukan!"
        )
    db.delete(shipment)
    db.commit()
    return Response(status_code=204)
    """
    Hapus data shipment berdasarkan ID.
    """


# UPDATE STATUS SHIPMENT
@router.patch("/{shipment_id}/status", response_model=ShipmentResponse)
def update_shipment_status(
    shipment_id: int,
    state: ShipmentState,
    db: Session = Depends(get_db),
    _: UserModel = Depends(get_current_user)
):
    """
    Update status shipment berdasarkan ID.
    Status yang tersedia: draft, confirmed, in_transit, delivered, cancelled.
    """
    shipment = db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code=404,
            detail=f"Shipment dengan ID {shipment_id} tidak ditemukan!"
        )
    shipment.state = state
    db.commit()
    db.refresh(shipment)
    return shipment
