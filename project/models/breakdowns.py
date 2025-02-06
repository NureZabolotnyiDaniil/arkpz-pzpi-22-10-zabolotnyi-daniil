from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Breakdown(Base):
    __tablename__ = "breakdowns"
    id = Column(Integer, primary_key=True, index=True)

    lantern_id = Column(Integer, ForeignKey("lanterns.id"), nullable=False)
    lantern = relationship("Lantern", back_populates="breakdowns")

    date = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)
