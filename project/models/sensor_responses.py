from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class SensorResponse(Base):
    __tablename__ = "sensor_responses"
    id = Column(Integer, primary_key=True, index=True)

    lantern_id = Column(Integer, ForeignKey("lanterns.id"), nullable=False)
    lantern = relationship("Lantern", back_populates="sensor_responses")

    date = Column(DateTime, nullable=False)
