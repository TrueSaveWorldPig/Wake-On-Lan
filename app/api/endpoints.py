from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, utils
from ..database import get_db
import subprocess

router = APIRouter()

@router.get("/devices", response_model=List[schemas.Device])
def get_devices(db: Session = Depends(get_db)):
    return crud.get_devices(db)

@router.post("/devices", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    return crud.create_device(db, device)

@router.delete("/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = crud.delete_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted"}

@router.post("/wake/{device_id}")
def wake_device(device_id: int, db: Session = Depends(get_db)):
    device = crud.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Execute the WOL script
    try:
        output = utils.send_wol_packet(device.mac, device.ip)
        return {"message": f"WOL packet sent to {device.name}", "output": output}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to send WOL packet: {e.stderr}")
