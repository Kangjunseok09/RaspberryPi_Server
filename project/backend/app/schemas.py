from pydantic import BaseModel
from datetime import datetime

# /api/sensor/logs POST
class SensorLogCreate(BaseModel):
    sensor_id: int
    value: float | None = None
    stage: int | None = None

class SensorLogResponse(BaseModel):
    log_id: int
    stage: int
    status: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True  

# /api/status/current GET
class StatusResponse(BaseModel):
    stage: int
    stage_label: str
    color: str
    current_level: float | None = None
    level_unit: str | None = None
    updated_at: datetime | None = None


class SensorOut(BaseModel):
    id: int
    type: str
    name: str
    gpio_pin: int
    threshold: float
    created_at: datetime

    class Config:
        from_attributes = True


class LedColorOut(BaseModel):
    state: str
    color_hex: str
    updated_at: datetime

    class Config:
        from_attributes = True


class LedColorUpdate(BaseModel):
    color_hex: str
