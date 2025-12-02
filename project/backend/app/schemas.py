from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# /api/sensor/logs POST
class SensorLogCreate(BaseModel):
    sensor_id: int
    value: float

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

# /api/windows GET
class WindowOut(BaseModel):
    id: int
    name: str
    position: int
    last_updated: datetime

    class Config:
        from_attributes = True

# /api/windows/open POST
class WindowOpenRequest(BaseModel):
    window_ids: list[int]
    position: int = 100
    reason: str | None = None

class WindowOpenResponse(BaseModel):
    success: bool
    updated_windows: list[WindowOut]