from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Park(Base):
    __tablename__ = "parks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=True)
    admin = relationship("Admin", back_populates="parks")

    lanterns = relationship("Lantern", back_populates="park")
