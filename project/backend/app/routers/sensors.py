from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional

from ..models import Sensor, SensorLog
from .deps import get_db
from .. import schemas   

router = APIRouter(
    prefix="/api",
    tags=["sensors"],
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_utc(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def compute_stage(value: float | None, threshold: float | None) -> int:
    if value is None:
        return 0

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return 0

    if numeric_value.is_integer() and 0 <= int(numeric_value) <= 3:
        return int(numeric_value)

    if numeric_value <= 0:
        return 0

    if threshold is None or threshold <= 0:
        return 1

    ratio = numeric_value / threshold
    if ratio < 0.7:
        return 1
    elif ratio < 1.0:
        return 2
    else:
        return 3

@router.post("/sensor/logs")
def create_sensor_log(payload: dict, db: Session = Depends(get_db)):
    sensor_id = payload.get("sensor_id")
    value = payload.get("value")
    stage_override = payload.get("stage")

    if sensor_id is None:
        raise HTTPException(status_code=400, detail="sensor_id is required")

    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if sensor is None:
        raise HTTPException(status_code=404, detail="sensor not found")

    if value is None and stage_override is None:
        raise HTTPException(status_code=400, detail="value or stage must be provided")

    if value is None:
        value = float(stage_override)

    log = SensorLog(
        sensor_id=sensor_id,
        value=value,
        created_at=utc_now()
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    if stage_override is not None:
        stage = int(stage_override)
    else:
        stage = compute_stage(value, sensor.threshold)

    status_map = {0: "clear", 1: "normal", 2: "warning", 3: "danger"}
    status = status_map.get(stage, "normal")
    message_map = {
        0: "정상 상태입니다.",
        1: "주의! 차량 주변 수위가 높습니다.",
        2: "위험! 안전벨트를 풀고 탈출을 준비하십시오.",
        3: "차량 창문이 자동으로 열립니다. 안전하게 탈출하세요."
    }
    message = message_map.get(stage, "수위 정보를 확인할 수 없습니다.")

    return {
        "log_id": log.id,
        "stage": stage,
        "status": status,
        "message": message,
        "created_at": ensure_utc(log.created_at)
    }

@router.get("/status/current")
def get_current_status(db: Session = Depends(get_db)):
    log = db.query(SensorLog).order_by(SensorLog.created_at.desc()).first()
    if log is None:
        return {
            "stage": 0,
            "stage_label": "정상",
            "color": "green",
            "current_level": None,
            "level_unit": None,
            "updated_at": None
        }

    sensor = log.sensor
    stage = compute_stage(log.value, sensor.threshold)
    if stage <= 0:
        label, color = "정상", "green"
    elif stage == 1:
        label, color = "주의", "green"
    elif stage == 2:
        label, color = "사전 대비 경고", "yellow"
    else:
        label, color = "위험", "red"

    return {
        "stage": stage,
        "stage_label": label,
        "color": color,
        "current_level": log.value,
        "level_unit": "cm",
        "updated_at": ensure_utc(log.created_at)
    }

@router.get("/sensors", response_model=list[schemas.SensorOut])
def list_sensors(db: Session = Depends(get_db)):

    sensors = db.query(Sensor).order_by(Sensor.id).all()
    return sensors

@router.get("/notifications")
def get_notifications(db: Session = Depends(get_db)):
    """모든 센서 로그를 알림 형태로 반환"""
    logs = db.query(SensorLog).order_by(SensorLog.created_at.desc()).limit(50).all()

    notifications = []
    for log in logs:
        sensor = log.sensor
        stage = compute_stage(log.value, sensor.threshold)
        status = {0: "clear", 1: "normal", 2: "warning", 3: "danger"}.get(stage, "normal")

        notifications.append({
            "log_id": log.id,
            "stage": stage,
            "status": status,
            "created_at": ensure_utc(log.created_at).isoformat()
        })

    return notifications
