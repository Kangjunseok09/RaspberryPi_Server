from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .deps import get_db
from .. import models, schemas

router = APIRouter(prefix="/api", tags=["sounds"])


@router.get("/sounds", response_model=list[schemas.SoundProfileOut])
def list_sounds(db: Session = Depends(get_db)):
    """사운드 프로필 리스트 조회"""
    sounds = db.query(models.SoundProfile).order_by(models.SoundProfile.id).all()
    return sounds


@router.post("/sounds/play", response_model=schemas.SoundPlayResponse)
def play_sound(req: schemas.SoundPlayRequest, db: Session = Depends(get_db)):

    sound = db.query(models.SoundProfile).filter(models.SoundProfile.id == req.sound_id).first()
    if not sound:
        raise HTTPException(status_code=404, detail="Sound profile not found")

    # 액션 로그 기록 (선택)
    action = models.ActionLog(
        window_id=None,
        sound_id=sound.id,
        sensor_log_id=None,
        action_type="SOUND_PLAY",
        reason=req.reason or "MANUAL_REQUEST",
    )
    db.add(action)
    db.commit()

    return schemas.SoundPlayResponse(
        success=True,
        sound=sound,
        message="사운드 재생 명령이 기록되었습니다.",
    )