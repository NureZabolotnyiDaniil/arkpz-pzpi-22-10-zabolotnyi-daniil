import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from routers.admin.crud import SECRET_KEY, ALGORITHM
from models.admins import Admin
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")


def get_current_admin(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Admin:
    print("Получен токен:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload декодирован:", payload)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: subject not provided",
            )
    except jwt.PyJWTError as e:
        print("Ошибка при декодировании токена:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    admin = db.query(Admin).filter(Admin.email == email).first()
    if admin is None:
        print("Администратор не найден для email:", email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found"
        )
    return admin


def get_full_access_admin(
    current_admin: Admin = Depends(get_current_admin),
) -> Admin:
    """
    Проверка доступа: только администратор с активным статусом и полными правами имеет доступ.
    """
    if current_admin.status != "active" or current_admin.rights != "full_access":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have sufficient privileges to modify admin status.",
        )
    return current_admin
