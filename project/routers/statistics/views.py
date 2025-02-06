from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from routers.admin.dependencies import get_current_admin
from models.admins import Admin
from database import get_db

from models.parks import Park
from sqlalchemy import text

from routers.statistics.services.energy_consumption import energy_consumption
from routers.statistics.services.energy_savings import energy_savings
from routers.statistics.services.repair_stats import get_avg_repair_time
from routers.statistics.utils.time_formatters import seconds_to_days_hours

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.post("/park_statistics")
async def get_park_statistics(
    park_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    park = db.query(Park).filter(Park.id == park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")

    # Fetch activated lanterns
    activated_lanterns = db.execute(
        text("SELECT * FROM get_top_activated_lanterns(:park_id)"), {"park_id": park_id}
    )
    columns = ["id", "activation_count"]
    formatted_activated_lanterns = [
        dict(zip(columns, row)) for row in activated_lanterns.fetchall()
    ]

    # Fetch lanterns needing renovation
    needing_renovation = db.execute(
        text("SELECT * FROM get_lanterns_needing_renovation(:park_id)"),
        {"park_id": park_id},
    )
    columns = ["id", "last_renovation_date"]
    formatted_needing_renovation = [
        dict(zip(columns, row)) for row in needing_renovation.fetchall()
    ]

    # Fetch planned renovations
    planned_renovations = db.execute(
        text("SELECT * FROM get_planned_renovations(:park_id)"),
        {"park_id": park_id},
    )
    columns = ["id", "lantern_id", "date"]
    formatted_planned_renovations = [
        dict(zip(columns, row)) for row in planned_renovations.fetchall()
    ]

    avg_seconds = get_avg_repair_time(db, park_id)
    formatted_time = seconds_to_days_hours(avg_seconds)

    return {
        "Top activated lanterns": formatted_activated_lanterns,
        "Lanterns needing renovation": formatted_needing_renovation,
        "Planned renovations": formatted_planned_renovations,
        "Average repair time": formatted_time,
    }


@router.post("/efficiency_statistics")
async def get_efficiency_statistics(
    park_id: int = Query(
        None,
        description="If the park is not entered, the statistics will be generalized",
    ),
    energy_cost: float = Query(
        4.32,
        description="Enter the actual energy cost in the грн/кВт∙год",
    ),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    park_filtration = ""

    if park_id:
        park = db.query(Park).filter(Park.id == park_id).first()
        if not park:
            raise HTTPException(status_code=404, detail="Park not found")
        park_filtration = "WHERE s1.park_id = :park_id"

    total_energy_consumption = energy_consumption(db, park_filtration, park_id)
    avg_savings_percent, avg_savings = energy_savings(db, park_filtration, park_id)
    savings_in_money = f"{round(avg_savings * energy_cost, 4)} грн/кВт∙год"

    return {
        "Total energy consumption": total_energy_consumption,
        "Average energy savings": avg_savings_percent,
        "Energy savings in monetary terms": savings_in_money,
    }
