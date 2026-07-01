from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db


def get_current_user(db: Session = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")


def require_admin():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin access required")


def require_student():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Student access required")
