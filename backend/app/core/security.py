# app/core/security.py
from pwdlib import PasswordHash
from fastapi import HTTPException,status
from jose import jwt,JWTError
from datetime import datetime, timedelta,timezone
import os
from dotenv import load_dotenv

load_dotenv()

password_hash = PasswordHash.recommended()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(form_password: str, hashed_password: str) -> bool:
    return password_hash.verify(form_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token,os.getenv("SECRET_KEY"),algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Token invalido o expirado")