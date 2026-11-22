from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.roles import UserRole, ROLE_PERMISSIONS
from app.models.user import User
from app.services.auth_service import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None or not user.is_active:
        raise credentials_exception

    return user


def require_permission(permission: str):
    def permission_checker(
        current_user: User = Depends(get_current_user)
    ):
        try:
            user_role = UserRole(current_user.role)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid user role"
            )

        allowed_permissions = ROLE_PERMISSIONS.get(user_role, [])

        if permission not in allowed_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )

        return current_user

    return permission_checker
