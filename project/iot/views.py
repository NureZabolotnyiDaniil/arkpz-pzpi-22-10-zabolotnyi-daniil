from datetime import datetime

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.breakdowns import Breakdown
from models.lanterns import Lantern
from models.sensor_responses import SensorResponse

router = APIRouter(prefix="/iot", tags=["iot"])


@router.get("/{lantern_id}/settings")
async def get_settings(lantern_id: int, db: Session = Depends(get_db)):
    settings = db.query(Lantern).filter_by(id=lantern_id).first()
    if not settings:
        raise HTTPException(status_code=404)
    return {
        "base_brightness": settings.base_brightness,
        "active_brightness": settings.active_brightness,
        "active_time": settings.active_time,
    }


@router.post("/{lantern_id}/motion")
async def log_motion(lantern_id: int, db: Session = Depends(get_db)):
    db.add(SensorResponse(lantern_id=lantern_id, date=datetime.now()))
    db.commit()
    return {"status": "logged"}


@router.post("/{lantern_id}/fault")
async def log_fault(
    lantern_id: int, error_type: str, value: float, db: Session = Depends(get_db)
):
    db.add(
        Breakdown(
            lantern_id=lantern_id,
            date=datetime.now(),
            description=error_type + f"; {value}",
        )
    )
    db.commit()
    return {"status": "error_logged"}


@router.post("/{lantern_id}/reboot")
async def reboot(lantern_id: int):
    return {"status": "reboot_command_received"}


@router.get("/{lantern_id}/status")
async def get_status(lantern_id: int):
    return {"status": "online", "voltage": 3.3}
