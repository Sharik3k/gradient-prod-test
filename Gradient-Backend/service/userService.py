from db import conn
from hashPswd import hash_password, verify_password
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

try:
    ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "2"))
except ValueError:
    ACCESS_TOKEN_EXPIRE_HOURS = 2

def register_user(user):
    try:
        logger.info(f"Starting registration for user: {user.username}, email: {user.email}")
        
        # Check environment variables
        if not SECRET_KEY:
            logger.error("SECRET_KEY environment variable is missing")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error: missing SECRET_KEY"
            )
        
        # Check if user already exists
        logger.info("Checking if user already exists")
        exists = conn.execute(
            "SELECT 1 FROM users WHERE username = ? OR email = ?",
            [user.username, user.email]
        ).fetchone()

        if exists:
            logger.warning(f"User already exists: {user.username}/{user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username or email already exists"
            )

        # Hash password
        logger.info("Hashing password")
        try:
            hashed_pwd = hash_password(user.password)
        except Exception as hash_error:
            logger.error(f"Password hashing failed: {str(hash_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Password processing failed"
            )

        # Get next ID
        logger.info("Getting next user ID")
        try:
            next_id = conn.execute(
                "SELECT COALESCE(MAX(id), 0) + 1 FROM users"
            ).fetchone()[0]
        except Exception as db_error:
            logger.error(f"Database query failed: {str(db_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )

        # Insert user
        logger.info(f"Inserting user with ID: {next_id}")
        try:
            conn.execute(
                "INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)",
                [next_id, user.username, user.email, hashed_pwd]
            )
            conn.commit()
        except Exception as insert_error:
            logger.error(f"User insertion failed: {str(insert_error)}")
            try:
                conn.rollback()
            except Exception as rollback_error:
                logger.warning(f"Rollback failed (no active transaction): {str(rollback_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User creation failed"
            )
        
        logger.info(f"User registered successfully: {user.username}")
        return {"message": "User created successfully"}
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log and handle other exceptions
        logger.error(f"Unexpected registration error: {str(e)}", exc_info=True)
        try:
            conn.rollback()
        except Exception as rollback_error:
            logger.warning(f"Rollback failed (no active transaction): {str(rollback_error)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login_user(user):
    username = user.username or user.email

    row = conn.execute(
        "SELECT username, password FROM users WHERE username = ? OR email = ?",
        [username, user.email or username]
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    stored_username, hashed_password = row

    if not verify_password(user.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token({"sub": stored_username})
    return {"access_token": access_token, "token_type": "bearer"}
