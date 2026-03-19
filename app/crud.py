from sqlalchemy.orm import Session
from . import models, schemas

def get_devices(db: Session):
    return db.query(models.DeviceDB).all()

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.DeviceDB(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: int):
    device = db.query(models.DeviceDB).filter(models.DeviceDB.id == device_id).first()
    if device:
        db.delete(device)
        db.commit()
    return device

def get_device(db: Session, device_id: int):
    return db.query(models.DeviceDB).filter(models.DeviceDB.id == device_id).first()
