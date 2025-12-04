from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .deps import get_db
from .. import models, schemas

router = APIRouter(prefix="/api", tags=["device"])


def _evaluate_stage(value: float, threshold: float) -> tuple[int, str, str]:

    if threshold <= 0:
        return 1, "safe", "정상 수위입니다."

    ratio = value / threshold

    if ratio < 0.5:
        return 1, "safe", "현재 수위는 안전한 수준입니다."
    elif ratio < 0.8:
        return 2, "warning", "수위가 높아지고 있습니다. 대비를 준비하십시오."
    else:
        return 3, "danger", "위험! 즉시 창문을 열고 탈출을 준비하십시오."


@router.get("/device/control/current", response_model=schemas.DeviceControlState)
def get_device_control_state(db: Session = Depends(get_db)):

    latest_log = (
        db.query(models.SensorLog)
        .order_by(models.SensorLog.created_at.desc())
        .first()
    )

    if not latest_log: 
        return schemas.DeviceControlState(
            stage=1,
            status="safe",
            should_open=False,
            target_position=0,
            play_sound_id=None,
            message="센서 데이터가 없습니다. 기본적으로 창문을 닫아 둡니다.",
            checked_at=datetime.utcnow(),
        )

    sensor = db.query(models.Sensor).filter(models.Sensor.id == latest_log.sensor_id).first()
    threshold = sensor.threshold if sensor else 1.0

    stage, status, msg = _evaluate_stage(latest_log.value, threshold)

    if stage == 1:
        should_open = False
        target_position = 0
        sound_id = None
    elif stage == 2:
        should_open = True
        target_position = 50
        sound_id = None
    else: 
        should_open = True
        target_position = 100
        sound_id = 1

    return schemas.DeviceControlState(
        stage=stage,
        status=status,
        should_open=should_open,
        target_position=target_position,
        play_sound_id=sound_id,
        message=msg,
        checked_at=datetime.utcnow(),
    )