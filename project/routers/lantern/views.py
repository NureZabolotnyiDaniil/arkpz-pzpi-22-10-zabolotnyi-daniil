from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from routers.admin.dependencies import get_current_admin
from models.admins import Admin
from database import get_db
from routers.lantern.schemas import LanternOut, LanternStatus
from routers.lantern.crud import (
    create_lantern_db as create_lantern,
    get_all_lanterns_from_db as get_all_lanterns,
    update_lantern_in_db as update_lantern,
    get_lantern_from_db as get_lantern,
    delete_lantern_from_db,
)

router = APIRouter(prefix="/lantern", tags=["lantern"])


@router.post("/add")
async def create_new_lantern(
    base_brightness: int = Query(
        0, ge=0, le=100, description="Base brightness (0-100%)"
    ),
    active_brightness: int = Query(
        0, ge=0, le=100, description="Active brightness (0-100%)"
    ),
    active_time: int = Query(5, ge=5, description="Active time in seconds (over 5s)"),
    status: Optional[LanternStatus] = Query("working", description="Lantern status"),
    park_id: Optional[int] = Query(None, description="Park"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    create_lantern(db, base_brightness, active_brightness, active_time, status, park_id)
    return {"message": "Lantern created successfully"}


@router.get("/list", response_model=List[LanternOut])
async def get_lantern_list(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    lanterns = get_all_lanterns(db)
    return lanterns


@router.get("/lantern/{lantern_id}", response_model=LanternOut)
def get_single_lantern(
    lantern_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    lantern = get_lantern(db, lantern_id)
    return lantern


@router.put("/update/{lantern_id}", response_model=LanternOut)
def update_lantern_details(
    lantern_id: int,
    base_brightness: int = Query(
        None, ge=0, le=100, description="Base brightness (0-100%)"
    ),
    active_brightness: int = Query(
        None, ge=0, le=100, description="Active brightness (0-100%)"
    ),
    active_time: int = Query(
        None, ge=5, description="Active time in seconds (over 5s)"
    ),
    status: LanternStatus = Query(None, description="Lantern status"),
    park_id: int = Query(None, description="Park. Enter '0' to reset the value"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    updated_lantern = update_lantern(
        db,
        lantern_id,
        base_brightness,
        active_brightness,
        active_time,
        status,
        park_id,
    )
    return updated_lantern


@router.delete("/delete/{lantern_id}", response_model=LanternOut)
async def delete_lantern(
    lantern_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    lantern = delete_lantern_from_db(db, lantern_id)
    return lantern
