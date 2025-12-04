from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .deps import get_db
from .. import models, schemas

router = APIRouter(prefix="/api", tags=["actions"])


@router.get("/actions/logs", response_model=list[schemas.ActionLogOut])
def list_action_logs(limit: int = 50, db: Session = Depends(get_db)):

    logs = (
        db.query(models.ActionLog)
        .order_by(models.ActionLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return logs