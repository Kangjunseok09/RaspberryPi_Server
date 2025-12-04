from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import sensors, windows, sounds, actions, device

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(sensors.router)
app.include_router(windows.router)
app.include_router(sounds.router)
app.include_router(actions.router)
app.include_router(device.router)

@app.get("/")
def read_root():
    return {"message": "홍수디딤이 API"}