from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..models import Window, ActionLog
from .deps import get_db

router = APIRouter(
    prefix="/api",
    tags=["windows"],
)

@router.get("/windows")
def list_windows(db: Session = Depends(get_db)):
    windows = db.query(Window).all()
    return [
        {
            "id": w.id,
            "name": w.name,
            "position": w.position,
            "last_updated": w.last_updated
        }
        for w in windows
    ]

@router.post("/windows/open")
def open_windows(payload: dict, db: Session = Depends(get_db)):
    window_ids = payload["window_ids"]
    position = payload.get("position", 100)
    reason = payload.get("reason", "manual")

    updated = []

    for wid in window_ids:
        w = db.query(Window).filter(Window.id == wid).first()
        if not w:
            continue
        w.position = position
        w.last_updated = datetime.utcnow()
        updated.append(w)

        log = ActionLog(
            window_id=w.id,
            action_type="window_open",
            reason=reason,
            created_at=datetime.utcnow(),
        )
        db.add(log)

    db.commit()

    return {
        "success": True,
        "updated_windows": [
            {"id": w.id, "position": w.position} for w in updated
        ]
    }