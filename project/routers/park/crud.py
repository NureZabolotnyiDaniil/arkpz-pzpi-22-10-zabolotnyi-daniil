from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.admins import Admin
from models.parks import Park


def create_park_db(
    db: Session,
    name: str,
    address: str,
    admin_id: int,
) -> Park:
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    new_park = Park(
        name=name,
        address=address,
        admin_id=admin_id,
    )
    db.add(new_park)
    db.commit()
    db.refresh(new_park)
    return new_park


def update_park_in_db(
    db: Session,
    park_id: int,
    name: str,
    address: str,
    admin_id: int,
) -> Park:

    park = db.query(Park).filter(Park.id == park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    if name:
        park.name = name
    if address:
        park.address = address
    if admin_id:
        park.admin_id = admin_id

    db.commit()
    db.refresh(park)
    return park


def get_all_parks_from_db(db: Session) -> List[Park]:
    return db.query(Park).order_by(Park.id).all()


def get_park_from_db(db: Session, park_id: int) -> Park:
    park = db.query(Park).filter(Park.id == park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")

    return park


def delete_park_from_db(db: Session, park_id: int) -> Park:
    park = db.query(Park).filter(Park.id == park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")

    db.delete(park)
    db.commit()
    return park
