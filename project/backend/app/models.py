from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    gpio_pin = Column(Integer, nullable=False)
    threshold = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

    logs = relationship("SensorLog", back_populates="sensor")

class SensorLog(Base):
    __tablename__ = "sensor_logs"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

    sensor = relationship("Sensor", back_populates="logs")


class LedColor(Base):
    __tablename__ = "led_colors"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(20), unique=True, nullable=False)
    color_hex = Column(String(7), nullable=False, default="#00FF00")
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)
