from sqlalchemy import text
from sqlalchemy.orm import Session


def energy_savings(db: Session, park_filtration: str, park_id: int):
    expended = retrieve_value_from_db("energy_expended", db, park_filtration, park_id)
    max_expenditure = retrieve_value_from_db(
        "max_energy_expenditure", db, park_filtration, park_id
    )

    avg_savings = max_expenditure - expended
    avg_savings_percent = int((1 - expended / max_expenditure) * 100)

    return f"{avg_savings_percent}%", avg_savings


def retrieve_value_from_db(
    db_variable: str, db: Session, park_filtration: str, park_id: int
):
    query = f"""
    SELECT SUM(s1.{db_variable})
    FROM statistics_hourly s1
    JOIN (
        SELECT park_id, MAX(date) AS max_date
        FROM statistics_hourly
        GROUP BY park_id
    ) s2
    ON s1.park_id = s2.park_id AND s1.date = s2.max_date"""

    execute_query = db.execute(
        text(f"{query} {park_filtration};"), {"park_id": park_id}
    ).scalar()

    return execute_query
