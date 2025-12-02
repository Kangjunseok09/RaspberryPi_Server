from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Window(Base):
    __tablename__ = "windows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    position = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow)

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    gpio_pin = Column(Integer, nullable=False)
    threshold = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    logs = relationship("SensorLog", back_populates="sensor")

class SensorLog(Base):
    __tablename__ = "sensor_logs"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    sensor = relationship("Sensor", back_populates="logs")

class SoundProfile(Base):
    __tablename__ = "sound_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    file_path = Column(String(255), nullable=False)
    volume = Column(Integer, nullable=False, default=80)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)
    window_id = Column(Integer, ForeignKey("windows.id"), nullable=True)
    sound_id = Column(Integer, ForeignKey("sound_profiles.id"), nullable=True)
    sensor_log_id = Column(Integer, ForeignKey("sensor_logs.id"), nullable=True)
    action_type = Column(String(50), nullable=False)
    reason = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)