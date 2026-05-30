from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Route as RouteModel, User as UserModel
from schemas import Route, RouteResponse, RouteCreate, RouteUpdate
from datetime import datetime
from auth import get_current_user
from typing import Optional

router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)

'''
ENDPOINTS
'''


#ENDPOINT UNTUK BACA SEMUA ROUTE
@router.get("", response_model= list[Route])
def get_routes(

    #query parameters(opsional)
    zone: Optional[str] = None, #filter untuk zone
    origin: Optional[str] = None, #filter untuk origin
    destination: Optional[str] = None, #filter ntuk destination 

    #dependencies
    db:Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):

    """
    Ambil semua route.
    Bisa difilter by zone, origin, atau destination.
    
    Contoh:
    - /routes?zone=Jawa
    - /routes?origin=Jakarta
    - /routes?destination=Surabaya
    """
    query = db.query(RouteModel)

    if zone is not None:
        query = query.filter(RouteModel.zone.ilike(f"%{zone}%"))
    if origin is not None:
        query = query.filter(RouteModel.zone.ilike(f"%{origin}%"))
    if destination is not None:
        query = query.filter(RouteModel.destination.ilike(f"%{destination}%"))
    return query.all()
    """
    Ambil semua data route yang terdaftar di sistem TMS.
    """




#ENDPOINT UNTUK MENAMBAHKAN ROUTE
@router.post("", response_model=RouteResponse, status_code=201)
def create_route(
    data:RouteCreate, db:Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    new_route = RouteModel(
        name = data.name,
        origin = data.origin,
        destination = data.destination,
        zone = data.zone,
        distance_km = data.distance_km,
        estimated_duration_hours = data.estimated_duration_hours,
        base_cost = data.base_cost,
        created_at = datetime.now()
    )

    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route
    """
    Tambahkan route baru ke sistem TMS.
    """





#ENDPOINT UNTUK UPDATE ROUTE
@router.put("/{route_id}", response_model=RouteResponse)
def update_route(
    route_id:int,
    data:RouteUpdate,
    db:Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    route = db.query(RouteModel).filter(RouteModel.id == route_id).first()
    if not route:
        raise HTTPException(
            status_code=404,
            detail=f"Rute dengan ID {route_id} tidak ditemukan!"
        )
    if data.name is not None:
        route.name = data.name
    if data.origin is not None:
        route.origin = data.origin
    if data.destination is not None:
        route.destination = data.destination
    if data.zone is not None:
        route.zone = data.zone
    if data.distance_km is not None:
        route.distance_km = data.distance_km
    if data.estimated_duration_hours is not None:
        route.estimated_duration_hours = data.estimated_duration_hours
    if data.base_cost is not None:
        route.base_cost = data.base_cost
    
    db.commit()
    db.refresh(route)
    return route
    """
    Update data route berdasarkan route id
    hanya ubah data yang di isi oleh user
    
    """




#ENDPOINT UNTUK DELETE ROUTE
@router.delete("/{route_id}", status_code=204)
def delete_route(
    route_id:int,
    db:Session = Depends(get_db),
    current_user:UserModel = Depends(get_current_user)
    ):
    route = db.query(RouteModel).filter(RouteModel.id == route_id).first()
    if not route:
        raise HTTPException(
            status_code =404,
            detail= f"Route dengan ID {route_id} tidak ditemukan!"
        )
    db.delete(route)
    db.commit()
    return None
    """
    Hapus data route berdasarkan ID.
    """