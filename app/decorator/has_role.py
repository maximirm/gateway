from functools import wraps

from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer

from app.clients import user_service_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def has_role(allowed_roles: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            token = await oauth2_scheme.__call__(request)
            if not token:
                raise HTTPException(
                    status_code=401,
                    detail="Unauthorized",
                )
            user = await user_service_client.fetch_user_by_token(token)
            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"User with token {token} not found"
                )
            if user.role not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail="Forbidden",
                )
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    user = await user_service_client.fetch_user_by_token(token)
    return user.id if user else None
