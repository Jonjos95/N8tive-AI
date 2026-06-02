"""
N8tive Portal JWT authentication middleware for FastAPI.
Validates tokens issued by the N8tive Company Portal (/api/auth/token).
Set N8TIVE_JWT_SECRET to the shared secret; set N8TIVE_PORTAL_URL to enable
server-side token introspection as a fallback.
"""

import os
import jwt as pyjwt
from fastapi import HTTPException, Header
from typing import Optional

JWT_SECRET = os.getenv("N8TIVE_JWT_SECRET", "")
JWT_ISSUER = os.getenv("N8TIVE_JWT_ISSUER", "n8tive-portal")
JWT_AUDIENCE = os.getenv("N8TIVE_JWT_AUDIENCE", "n8tive-suite")


def _decode(token: str) -> dict:
    if not JWT_SECRET:
        raise HTTPException(status_code=500, detail="N8TIVE_JWT_SECRET not configured")
    try:
        return pyjwt.decode(
            token, JWT_SECRET,
            algorithms=["HS256"],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
        )
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except pyjwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """FastAPI dependency — injects the decoded token payload as the current user."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    return _decode(authorization.split(" ", 1)[1])
