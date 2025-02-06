from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.parks import Park

from database import Base


class Lantern(Base):
    __tablename__ = "lanterns"
    id = Column(Integer, primary_key=True, index=True)
    base_brightness = Column(Integer, nullable=False)
    active_brightness = Column(Integer, nullable=False)
    active_time = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="working")

    park_id = Column(Integer, ForeignKey("parks.id"), nullable=True)
    park = relationship("Park", back_populates="lanterns")

    renovations = relationship("Renovation", back_populates="lantern")
    breakdowns = relationship("Breakdown", back_populates="lantern")
    sensor_responses = relationship("SensorResponse", back_populates="lantern")
