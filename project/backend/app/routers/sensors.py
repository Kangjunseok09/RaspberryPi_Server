from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..models import Sensor, SensorLog
from .deps import get_db

router = APIRouter(
    prefix="/api",
    tags=["sensors"],
)

def compute_stage(value: float, threshold: float) -> int:
    if threshold <= 0:
        return 1
    ratio = value / threshold
    if ratio < 0.7:
        return 1
    elif ratio < 1.0:
        return 2
    else:
        return 3

@router.post("/sensor/logs")
def create_sensor_log(payload: dict, db: Session = Depends(get_db)):
    sensor_id = payload["sensor_id"]
    value = payload["value"]

    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if sensor is None:
        return {"error": "sensor not found"}

    log = SensorLog(
        sensor_id=sensor_id,
        value=value,
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    stage = compute_stage(value, sensor.threshold)
    status = {1: "normal", 2: "warning", 3: "danger"}[stage]
    message = {
        1: "주의! 차량 주변 수위가 높습니다.",
        2: "위험! 안전벨트를 풀고 탈출을 준비하십시오.",
        3: "차량 창문이 자동으로 열립니다. 안전하게 탈출하세요."
    }[stage]

    return {
        "log_id": log.id,
        "stage": stage,
        "status": status,
        "message": message,
        "created_at": log.created_at
    }

@router.get("/status/current")
def get_current_status(db: Session = Depends(get_db)):
    log = db.query(SensorLog).order_by(SensorLog.created_at.desc()).first()
    if log is None:
        return {
            "stage": 1,
            "stage_label": "정상",
            "color": "green",
            "current_level": None,
            "level_unit": None,
            "updated_at": None
        }

    sensor = log.sensor
    stage = compute_stage(log.value, sensor.threshold)
    if stage == 1:
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
        "updated_at": log.created_at
    }