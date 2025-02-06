from typing import List
from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from database import get_db
from models.admins import Admin
from routers.admin.dependencies import get_current_admin
from routers.company.schemas import CompanyOut
from routers.company.crud import (
    create_company_db as create_company,
    update_company_in_db as update_company,
    get_all_companies_from_db as get_all_companies,
    get_company_from_db as get_company,
    delete_company_from_db,
)

router = APIRouter(prefix="/company", tags=["company"])


@router.post("/add")
async def create_new_company(
    name: str = Query(
        None,
        description="Company name",
    ),
    email: EmailStr = Query(None, description="Company email address"),
    address: str = Query(
        "вулиця Олександра Зубарєва, 47, Харків, Харківська область, Україна, 61000",
        description="Company address",
    ),
    notes: str = Query(
        None,
        description="Company website, additional contacts or another notes",
    ),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    create_company(db, name, email, address, notes)
    return {"message": "Company added successfully"}


@router.get("/list", response_model=List[CompanyOut])
async def get_company_list(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    companies = get_all_companies(db)
    return companies


@router.get("/info/{company_id}", response_model=CompanyOut)
def get_single_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    company = get_company(db, company_id)
    return company


@router.put("/update/{company_id}", response_model=CompanyOut)
def update_company_details(
    company_id: int,
    name: str = Query(
        None,
        description="Company name. Enter 'none' to reset the value",
    ),
    email: EmailStr = Query(None, description="Company email address"),
    address: str = Query(
        None,
        description="Company address. Enter 'none' to reset the value",
    ),
    notes: str = Query(
        None,
        description="Company website, additional contacts or another notes. Enter 'none' to reset the value",
    ),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    company = update_company(
        db,
        company_id,
        name,
        email,
        address,
        notes,
    )
    return company


@router.delete("/delete/{company_id}", response_model=CompanyOut)
async def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    company = delete_company_from_db(db, company_id)
    return company
