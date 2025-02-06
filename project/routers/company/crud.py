from typing import List
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from models.companies import Company


def create_company_db(
    db: Session,
    name: str,
    email: EmailStr,
    address: str,
    notes: str,
) -> Company:
    existing_email = db.query(Company).filter(Company.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_company = Company(
        name=name,
        email=email,
        address=address,
        notes=notes,
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def update_company_in_db(
    db: Session,
    company_id: int,
    name: str,
    email: EmailStr,
    address: str,
    notes: str,
) -> Company:

    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    existing_email = db.query(Company).filter(Company.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    if name:
        company.name = name
        if name == "none":
            company.name = None

    if email:
        company.email = email

    if address:
        company.address = address
        if address == "none":
            company.address = None

    if notes:
        company.notes = notes
        if notes == "none":
            company.notes = None

    db.commit()
    db.refresh(company)
    return company


def get_all_companies_from_db(db: Session) -> List[Company]:
    return db.query(Company).order_by(Company.id).all()


def get_company_from_db(db: Session, company_id: int) -> Company:
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


def delete_company_from_db(db: Session, company_id: int) -> Company:
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(company)
    db.commit()
    return company
