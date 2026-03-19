from typing import Optional
from pydantic import BaseModel, ConfigDict

class DeviceBase(BaseModel):
    name: str
    mac: str
    ip: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
