from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from db import SessionLocal
from models import Forager

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(x_api_key: str = Depends(api_key_header)) -> str:
    db = SessionLocal()
    forager = db.query(Forager).filter_by(api_key=x_api_key).first()
    db.close()
    if forager is None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return forager.username
