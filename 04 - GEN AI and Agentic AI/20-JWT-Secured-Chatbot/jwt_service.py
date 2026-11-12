"""
jwt_service.py - create and validate JWT tokens.
"""
from datetime import datetime, timedelta, timezone

import jwt
from config import config


def create_token(username):
    """Signed token for this user, valid for JWT_EXPIRE_MINUTES."""
    expiry = datetime.now(timezone.utc) + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expiry}
    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)


def validate_token(token):
    """Returns the username if the token is valid and not expired, else None."""
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY,
                             algorithms=[config.JWT_ALGORITHM],
                             options={"require": ["exp", "sub"]})
        return payload["sub"]
    except jwt.InvalidTokenError:  # expired, tampered, or malformed
        return None