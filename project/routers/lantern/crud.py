from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.lanterns import Lantern
from models.parks import Park


def create_lantern_db(
    db: Session,
    base_brightness: int,
    active_brightness: int,
    active_time: int,
    status: str,
    park_id: int,
) -> Lantern:
    park = db.query(Park).filter(Park.id == park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")
    new_lantern = Lantern(
        base_brightness=base_brightness,
        active_brightness=active_brightness,
        active_time=active_time,
        status=status,
        park_id=park_id,
    )
    db.add(new_lantern)
    db.commit()
    db.refresh(new_lantern)
    return new_lantern


def update_lantern_in_db(
    db: Session,
    lantern_id: int,
    base_brightness: int,
    active_brightness: int,
    active_time: int,
    status: str,
    park_id: int,
) -> Lantern:
    lantern = db.query(Lantern).filter(Lantern.id == lantern_id).first()
    if not lantern:
        raise HTTPException(status_code=404, detail="Lantern not found")

    if base_brightness:
        lantern.base_brightness = base_brightness

    if active_brightness:
        lantern.active_brightness = active_brightness

    if active_time:
        lantern.active_time = active_time

    if status:
        lantern.status = status

    if park_id is not None:
        if park_id == 0:
            lantern.park_id = None
        else:
            park = db.query(Park).filter(Park.id == park_id).first()
            if not park:
                raise HTTPException(status_code=404, detail="Park not found")
            lantern.park_id = park_id

    db.commit()
    db.refresh(lantern)
    return lantern


def get_all_lanterns_from_db(db: Session) -> List[Lantern]:
    return db.query(Lantern).order_by(Lantern.id).all()


def get_lantern_from_db(db: Session, lantern_id: int) -> Lantern:
    lantern = db.query(Lantern).filter(Lantern.id == lantern_id).first()
    if not lantern:
        raise HTTPException(status_code=404, detail="Lantern not found")

    return lantern


def delete_lantern_from_db(db: Session, lantern_id: int) -> Lantern:
    lantern = db.query(Lantern).filter(Lantern.id == lantern_id).first()
    if not lantern:
        raise HTTPException(status_code=404, detail="Lantern not found")
    db.delete(lantern)
    db.commit()
    return lantern
