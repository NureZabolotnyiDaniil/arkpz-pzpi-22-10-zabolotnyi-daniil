from typing import List
from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from database import get_db
from models.admins import Admin
from routers.admin.dependencies import get_current_admin
from routers.repairman.schemas import RepairmanOut
from routers.repairman.crud import (
    create_repairman_db as create_repairman,
    update_repairman_in_db as update_repairman,
    get_all_repairmans_from_db as get_all_repairmans,
    get_repairman_from_db as get_repairman,
    delete_repairman_from_db,
)

router = APIRouter(prefix="/repairman", tags=["repairman"])


@router.post("/add")
async def create_new_repairman(
    first_name: str = Query(
        None,
        description="First name",
    ),
    surname: str = Query(
        None,
        description="Surname",
    ),
    email: EmailStr = Query(None, description="Repairer email"),
    company_email: EmailStr = Query(
        None, description="Company from which the repairer is from (if existing)"
    ),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    create_repairman(db, first_name, surname, email, company_email)
    return {"message": "Repairman added successfully"}


@router.get("/list", response_model=List[RepairmanOut])
async def get_repairman_list(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    repairmans = get_all_repairmans(db)
    return repairmans


@router.get("/info/{repairman_id}", response_model=RepairmanOut)
def get_single_repairman(
    repairman_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    repairman = get_repairman(db, repairman_id)
    return repairman


@router.put("/update/{repairman_id}", response_model=RepairmanOut)
def update_repairman_details(
    repairman_id: int,
    first_name: str = Query(
        None,
        description="First name. Enter 'none' to reset the value",
    ),
    surname: str = Query(
        None,
        description="Surname. Enter 'none' to reset the value",
    ),
    email: EmailStr = Query(None, description="Repairer email"),
    change_company_email: bool = Query(
        False,
        description="True - if you want to change the company email",
    ),
    company_email: EmailStr = Query(
        None,
        description="Company from which the repairer is from. Leave the field blank to reset the value",
    ),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    repairman = update_repairman(
        db,
        repairman_id,
        first_name,
        surname,
        email,
        change_company_email,
        company_email,
    )
    return repairman


@router.delete("/delete/{repairman_id}", response_model=RepairmanOut)
async def delete_repairman(
    repairman_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    repairman = delete_repairman_from_db(db, repairman_id)
    return repairman
