from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Route as RouteModel
from schemas import Route, RouteResponse, RouteCreate, RouteUpdate
from datetime import datetime


router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)

'''
ENDPOINTS
'''


#ENDPOINT UNTUK BACA SEMUA ROUTE
@router.get("", response_model= list[Route])
def get_routes(db:Session = Depends(get_db)):
    return db.query(RouteModel).all()



#ENDPOINT UNTUK MENAMBAHKAN ROUTE
@router.post("", response_model=RouteResponse, status_code=201)
def create_route(data:RouteCreate, db:Session = Depends(get_db)):
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



#ENDPOINT UNTUK UPDATE ROUTE
@router.put("/{route_id}", response_model=RouteResponse)
def update_route(route_id:int, data:RouteUpdate, db:Session = Depends(get_db)):
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

#ENDPOINT UNTUK DELETE ROUTE
@router.delete("/{route_id}", status_code=204)
def delete_route(route_id:int, db:Session = Depends(get_db)):
    route = db.query(RouteModel).filter(RouteModel.id == route_id).first()
    if not route:
        raise HTTPException(
            status_code =404,
            detail= f"Route dengan ID {route_id} tidak ditemukan!"
        )
    db.delete(route)
    db.commit()
    return None