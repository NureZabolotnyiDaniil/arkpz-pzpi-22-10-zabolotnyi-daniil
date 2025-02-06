from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.companies import Company

from database import Base


class Repairman(Base):
    __tablename__ = "repairmans"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    company = relationship("Company", back_populates="repairmans")

    renovations = relationship("Renovation", back_populates="repairman")
