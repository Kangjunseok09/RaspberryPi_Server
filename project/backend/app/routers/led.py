from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import LedColor
from .. import schemas
from .deps import get_db

router = APIRouter(
    prefix="/api/led",
    tags=["led"],
)

DEFAULT_COLORS = {
    "normal": "#00FF00",
    "warning": "#FFA500",
    "danger": "#FF0000",
}


def ensure_defaults(db: Session):
    """Create default records if missing."""
    existing = {color.state for color in db.query(LedColor).all()}
    created = False
    for state, color in DEFAULT_COLORS.items():
        if state not in existing:
            db.add(LedColor(state=state, color_hex=color))
            created = True
    if created:
        db.commit()


@router.get("/colors", response_model=list[schemas.LedColorOut])
def list_led_colors(db: Session = Depends(get_db)):
    ensure_defaults(db)
    return db.query(LedColor).order_by(LedColor.id).all()


@router.put("/colors/{state}", response_model=schemas.LedColorOut)
def update_led_color(state: str, payload: schemas.LedColorUpdate, db: Session = Depends(get_db)):
    ensure_defaults(db)
    color = db.query(LedColor).filter(LedColor.state == state).first()
    if color is None:
        raise HTTPException(status_code=404, detail="state not found")
    color.color_hex = payload.color_hex
    db.commit()
    db.refresh(color)
    return color
