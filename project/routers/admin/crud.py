import os
from datetime import datetime, timedelta
from typing import List
import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.admins import Admin
from routers.admin.schemas import RegistrationRequest, LoginRequest, AdminUpdate
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_admin(db: Session, user: RegistrationRequest) -> Admin:
    existing_admin = db.query(Admin).filter(Admin.email == user.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    new_admin = Admin(
        first_name=user.first_name,
        surname=user.surname,
        email=user.email,
        password=hashed_password,
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


def authenticate_admin(db: Session, login_data: LoginRequest) -> Admin:
    admin = db.query(Admin).filter(Admin.email == login_data.email).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email not found",
        )

    if admin.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your account has not been activated. Wait for activation.",
        )

    if not verify_password(login_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    return admin


def get_all_admins(db: Session) -> List[Admin]:
    return db.query(Admin).order_by(Admin.id).all()


def update_admin(db: Session, admin_id: int, admin_data: AdminUpdate) -> Admin:
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if admin_data.first_name is not None:
        admin.first_name = admin_data.first_name

    if admin_data.surname is not None:
        admin.surname = admin_data.surname

    if admin_data.email is not None:
        existing_admin = (
            db.query(Admin)
            .filter(Admin.email == admin_data.email, Admin.id != admin_id)
            .first()
        )
        if existing_admin:
            raise HTTPException(status_code=400, detail="Email already used")
        admin.email = admin_data.email

    if admin_data.password is not None:
        admin.password = pwd_context.hash(admin_data.password)

    db.commit()
    db.refresh(admin)
    return admin


def update_admin_status(
    db: Session, admin_email: str, status: str, rights: str
) -> Admin:
    admin = db.query(Admin).filter(Admin.email == admin_email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    admin.status = status
    admin.rights = rights

    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(db: Session, admin_id: int) -> Admin:
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    db.delete(admin)
    db.commit()
    return admin
