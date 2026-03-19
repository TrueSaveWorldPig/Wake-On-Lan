from pydantic import BaseModel, ConfigDict

class DeviceBase(BaseModel):
    name: str
    mac: str
    ip: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
