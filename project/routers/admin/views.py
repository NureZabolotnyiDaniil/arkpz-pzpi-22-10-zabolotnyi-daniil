from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.admins import Admin
from routers.admin.dependencies import get_current_admin, get_full_access_admin
from routers.admin.crud import (
    create_admin,
    authenticate_admin,
    create_access_token,
    get_all_admins,
    delete_admin,
    update_admin,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    update_admin_status,
)
from routers.admin.schemas import (
    RegistrationRequest,
    LoginRequest,
    AdminOut,
    AdminUpdate,
    AdminStatusUpdate,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/register")
async def register_admin(user: RegistrationRequest, db: Session = Depends(get_db)):
    create_admin(db, user)
    return {"message": "User registered successfully"}


@router.post("/login")
async def login_admin(user: LoginRequest, db: Session = Depends(get_db)):
    admin = authenticate_admin(db, user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/list", response_model=List[AdminOut])
async def get_admins_list(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    admins = get_all_admins(db)
    return admins


@router.put("/edit", response_model=AdminOut)
async def set_admin(
    admin_data: AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    updated_admin = update_admin(db, current_admin.id, admin_data)
    return updated_admin


@router.put("/update_status/{admin_email}", response_model=AdminOut)
async def set_admin_status(
    admin_email: str,
    status_update: AdminStatusUpdate,
    db: Session = Depends(get_db),
    full_access_admin: Admin = Depends(get_full_access_admin),
):
    updated_admin = update_admin_status(
        db, admin_email, status_update.status, status_update.rights
    )
    return updated_admin


@router.delete("/delete/{admin_id}", response_model=AdminOut)
async def remove_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    full_access_admin: Admin = Depends(get_full_access_admin),
):
    deleted_admin = delete_admin(db, admin_id)
    return deleted_admin
