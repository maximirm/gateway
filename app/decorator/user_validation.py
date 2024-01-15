from functools import wraps

from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from app.services import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def has_role(allowed_roles: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            token = await oauth2_scheme.__call__(request)
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                )

            user = await user_service.get_user(token)
            if user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden",
                )

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
