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


class WindowOut(BaseModel):
    id: int
    name: str
    position: int
    last_updated: datetime

    class Config:
        from_attributes = True

class WindowOpenRequest(BaseModel):
    window_ids: list[int]
    position: int = 100
    reason: str | None = None

class WindowOpenResponse(BaseModel):
    success: bool
    updated_windows: list[WindowOut]

class SensorOut(BaseModel):
    id: int
    type: str
    name: str
    gpio_pin: int
    threshold: float
    created_at: datetime

    class Config:
        from_attributes = True


class SoundProfileOut(BaseModel):
    id: int
    name: str
    file_path: str
    volume: int
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class SoundPlayRequest(BaseModel):
    sound_id: int
    reason: str | None = None


class SoundPlayResponse(BaseModel):
    success: bool
    sound: SoundProfileOut | None = None
    message: str

class ActionLogOut(BaseModel):
    id: int
    window_id: int | None = None
    sound_id: int | None = None
    sensor_log_id: int | None = None
    action_type: str
    reason: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class DeviceControlState(BaseModel):
    stage: int
    status: str          
    should_open: bool    
    target_position: int 
    play_sound_id: int | None = None
    message: str
    checked_at: datetime