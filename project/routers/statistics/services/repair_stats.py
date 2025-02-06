from sqlalchemy import text
from sqlalchemy.orm import Session


def get_avg_repair_time(db: Session, park_id: int) -> float:
    query = text(
        """
        WITH ranked_renovations AS (
            SELECT 
                b.id AS breakdown_id,
                b.date AS breakdown_date,
                r.date AS renovation_date,
                ROW_NUMBER() OVER (
                    PARTITION BY b.id 
                    ORDER BY r.date - b.date ASC
                ) AS rn
            FROM breakdowns b
            LEFT JOIN renovations r 
                ON b.lantern_id = r.lantern_id 
                AND r.status = 'completed'
                AND r.date >= b.date
            JOIN lanterns l ON b.lantern_id = l.id
    		WHERE l.park_id = :park_id
        )
        SELECT 
            AVG(EXTRACT(EPOCH FROM (renovation_date - breakdown_date))) 
        FROM ranked_renovations
        WHERE rn = 1;
    """
    )
    result = db.execute(query, {"park_id": park_id})
    avg_seconds = result.scalar()
    return avg_seconds if avg_seconds else 0.0
