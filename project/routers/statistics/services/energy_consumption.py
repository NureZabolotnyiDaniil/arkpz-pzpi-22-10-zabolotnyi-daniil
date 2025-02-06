from sqlalchemy import text
from sqlalchemy.orm import Session


def energy_consumption(db: Session, park_filtration: str, park_id: int):
    query = """
    SELECT SUM(s1.energy_expended)
    FROM statistics_hourly s1
    JOIN (
        SELECT park_id, MAX(date) AS max_date
        FROM statistics_hourly
        GROUP BY park_id
    ) s2
    ON s1.park_id = s2.park_id AND s1.date = s2.max_date"""

    energy_expended = db.execute(
        text(f"{query} {park_filtration};"), {"park_id": park_id}
    ).scalar()

    return f"{energy_expended} кВт·год"
