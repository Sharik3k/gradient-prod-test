from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from service.userService import register_user, login_user
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.post("/register")
def register(user: User):
    try:
        logger.info(f"Registration attempt for email: {user.email}")
        result = register_user(user)
        logger.info(f"Registration successful for email: {user.email}")
        return result
    except HTTPException as e:
        logger.error(f"HTTPException during registration for {user.email}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during registration for {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during registration"
        )


@router.post("/login")
def login(user: User):
    try:
        logger.info(f"Login attempt for email: {user.email}")
        result = login_user(user)
        logger.info(f"Login successful for email: {user.email}")
        return result
    except HTTPException as e:
        logger.error(f"HTTPException during login for {user.email}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login for {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during login"
        )
