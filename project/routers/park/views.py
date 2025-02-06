from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from routers.admin.dependencies import get_current_admin
from models.admins import Admin
from database import get_db

from routers.park.schemas import ParkOut
from routers.park.crud import (
    create_park_db as create_park,
    get_all_parks_from_db as get_all_parks,
    update_park_in_db as update_park,
    get_park_from_db as get_park,
    delete_park_from_db,
)

router = APIRouter(prefix="/park", tags=["park"])


@router.post("/add")
async def create_new_park(
    name: str = Query(
        "Центральний парк культури та відпочинку",
        description="Name of the park",
    ),
    address: str = Query(
        "вулиця Сумська, 81, Харків, Харківська область, Україна, 61000",
        description="Address, city, state of the park",
    ),
    admin_id: int = Query(None, description="Administrator responsible for the park"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    create_park(db, name, address, admin_id)
    return {"message": "Park added successfully"}


@router.get("/list", response_model=List[ParkOut])
async def get_park_list(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    parks = get_all_parks(db)
    return parks


@router.get("/info/{park_id}", response_model=ParkOut)
def get_single_park(
    park_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    park = get_park(db, park_id)
    return park


@router.put("/update/{park_id}", response_model=ParkOut)
def update_park_details(
    park_id: int,
    name: str = Query(
        None,
        description="Name of the park",
    ),
    address: str = Query(
        None,
        description="Address, city, state of the park",
    ),
    admin_id: int = Query(None, description="Administrator responsible for the park"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    park = update_park(db, park_id, name, address, admin_id)
    return park


@router.delete("/delete/{park_id}", response_model=ParkOut)
async def delete_park(
    park_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    park = delete_park_from_db(db, park_id)
    return park
