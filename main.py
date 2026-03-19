import subprocess
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./devices.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DeviceDB(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mac = Column(String)
    ip = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# Pydantic models
class DeviceBase(BaseModel):
    name: str
    mac: str
    ip: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# FastAPI app
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.get("/api/devices", response_model=List[Device])
def get_devices(db: Session = Depends(get_db)):
    return db.query(DeviceDB).all()

@app.post("/api/devices", response_model=Device)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    db_device = DeviceDB(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@app.delete("/api/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(DeviceDB).filter(DeviceDB.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"message": "Device deleted"}

@app.post("/api/wake/{device_id}")
def wake_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(DeviceDB).filter(DeviceDB.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Execute the WOL script
    try:
        # Use broadcast 255.255.255.255 by default, or specific IP if provided
        broadcast = "255.255.255.255"
        # If user wants to target specific IP broadcast, they can specify it
        # For now we use global broadcast as in the script's default
        
        result = subprocess.run(
            ["bash", "wol.sh", device.mac, broadcast],
            capture_output=True,
            text=True,
            check=True
        )
        return {"message": f"WOL packet sent to {device.name}", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to send WOL packet: {e.stderr}")

# Serve Frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
