from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from routers.admin.dependencies import get_current_admin
from models.admins import Admin
from database import get_db

from datetime import datetime
from routers.renovation.schemas import RenovationStatus, RenovationOut
from routers.renovation.crud import (
    create_renovation_db as create_renovation,
    get_all_renovations_from_db as get_all_renovations,
    update_renovation_in_db as update_renovation,
    get_renovation_from_db as get_renovation,
    delete_renovation_from_db,
)

router = APIRouter(prefix="/renovation", tags=["renovation"])

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


@router.post("/add")
async def create_new_renovation(
    lantern_id: int = Query(None, description="Foreign key of the table 'lanterns'"),
    date: str = Query(
        datetime.now().strftime(DATE_FORMAT),
        description=f"Date in format {DATE_FORMAT}",
    ),
    time: str = Query(
        datetime.now().strftime(TIME_FORMAT),
        description=f"Time in format {TIME_FORMAT}",
    ),
    status: RenovationStatus = Query("planned", description="Renovation status"),
    cost: int = Query(0, description="Cost of the renovation (only integers)"),
    repairman_email: EmailStr = Query(
        None, description="Repairer responsible for the renovation"
    ),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    try:
        date_obj = datetime.strptime(date, DATE_FORMAT)
        time_obj = datetime.strptime(time, TIME_FORMAT)

        datetime_combined = datetime.combine(date_obj, time_obj.time())

        create_renovation(
            db, lantern_id, datetime_combined, status, cost, repairman_email
        )
        return {"message": "Renovation added successfully"}
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date or time format. Expected formats are {DATE_FORMAT} and {TIME_FORMAT} respectively.",
        )


@router.get("/list", response_model=List[RenovationOut])
async def get_renovation_list(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    renovations = get_all_renovations(db)

    formatted_renovations = []
    for renovation in renovations:
        renovation_out = RenovationOut(**vars(renovation))
        renovation_out.date = renovation.date.strftime(DATETIME_FORMAT)
        formatted_renovations.append(renovation_out)

    return formatted_renovations


@router.get("/info/{renovation_id}", response_model=RenovationOut)
def get_single_renovation(
    renovation_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    renovation = get_renovation(db, renovation_id)

    formatted_renovation = RenovationOut(**vars(renovation))
    formatted_renovation.date = renovation.date.strftime(DATETIME_FORMAT)
    return formatted_renovation


@router.put("/update/{renovation_id}", response_model=RenovationOut)
def update_renovation_details(
    renovation_id: int,
    lantern_id: Optional[int] = Query(
        None, description="Foreign key of the table 'lanterns'"
    ),
    date: str = Query(
        None,
        description=f"Date in format {DATE_FORMAT}",
    ),
    time: str = Query(
        None,
        description=f"Time in format {TIME_FORMAT}",
    ),
    status: Optional[RenovationStatus] = Query(None, description="Renovation status"),
    cost: int = Query(None, description="Cost of the renovation (only integers)"),
    change_repairman_email: bool = Query(
        False,
        description="True - if you want to change the repairman email",
    ),
    repairman_email: EmailStr = Query(
        None,
        description="Repairer responsible for the renovation. Leave the field blank to reset the value",
    ),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    renovation = update_renovation(
        db,
        renovation_id,
        lantern_id,
        date,
        time,
        DATE_FORMAT,
        TIME_FORMAT,
        status,
        cost,
        change_repairman_email,
        repairman_email,
    )

    formatted_renovation = RenovationOut(**vars(renovation))
    formatted_renovation.date = renovation.date.strftime(DATETIME_FORMAT)
    return formatted_renovation


@router.delete("/delete/{renovation_id}", response_model=RenovationOut)
async def delete_renovation(
    renovation_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    renovation = delete_renovation_from_db(db, renovation_id)

    formatted_renovation = RenovationOut(**vars(renovation))
    formatted_renovation.date = renovation.date.strftime(DATETIME_FORMAT)
    return formatted_renovation
