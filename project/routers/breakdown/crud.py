from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.lanterns import Lantern
from models.breakdowns import Breakdown


def create_breakdown_db(
    db: Session,
    lantern_id: int,
    date: datetime,
    description: str,
) -> Breakdown:

    lantern = db.query(Lantern).filter(Lantern.id == lantern_id).first()
    if not lantern:
        raise HTTPException(
            status_code=404, detail=f"Lantern with id: {lantern_id} not found"
        )

    new_breakdown = Breakdown(
        lantern_id=lantern_id,
        date=date,
        description=description,
    )
    db.add(new_breakdown)
    db.commit()
    db.refresh(new_breakdown)
    return new_breakdown


def update_breakdown_in_db(
    db: Session,
    breakdown_id: int,
    lantern_id: int,
    date: str,
    time: str,
    date_format: str,
    time_format: str,
    description: str,
) -> Breakdown:

    breakdown = db.query(Breakdown).filter(Breakdown.id == breakdown_id).first()
    if not breakdown:
        raise HTTPException(status_code=404, detail="Breakdown not found")

    if lantern_id:
        lantern = db.query(Lantern).filter(Lantern.id == lantern_id).first()
        if not lantern:
            raise HTTPException(status_code=404, detail="Lantern not found")
        breakdown.lantern_id = lantern_id

    if date:
        try:
            date_obj = datetime.strptime(date, date_format)

            datetime_combined = datetime.combine(date_obj, breakdown.date.time())
            breakdown.date = datetime_combined
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date format. Expected format is {date_format}.",
            )

    if time:
        try:
            time_obj = datetime.strptime(time, time_format)

            datetime_combined = datetime.combine(breakdown.date.date(), time_obj.time())
            breakdown.date = datetime_combined
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid time format. Expected format is {time_format}.",
            )

    if description:
        breakdown.description = description
        if description == "none":
            breakdown.description = None

    db.commit()
    db.refresh(breakdown)
    return breakdown


def get_all_breakdowns_from_db(db: Session) -> List[Breakdown]:
    return db.query(Breakdown).order_by(Breakdown.id).all()


def get_breakdown_from_db(db: Session, breakdown_id: int) -> Breakdown:
    breakdown = db.query(Breakdown).filter(Breakdown.id == breakdown_id).first()
    if not breakdown:
        raise HTTPException(status_code=404, detail="Breakdown not found")

    return breakdown


def delete_breakdown_from_db(db: Session, breakdown_id: int) -> Breakdown:
    breakdown = db.query(Breakdown).filter(Breakdown.id == breakdown_id).first()
    if not breakdown:
        raise HTTPException(status_code=404, detail="Breakdown not found")

    db.delete(breakdown)
    db.commit()
    return breakdown
