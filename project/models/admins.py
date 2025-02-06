from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    status = Column(String, nullable=False, default="inactive")
    rights = Column(String, nullable=False, default="restricted_access")

    parks = relationship("Park", back_populates="admin")
