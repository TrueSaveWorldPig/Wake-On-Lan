from sqlalchemy import Column, Integer, String
from .database import Base

class DeviceDB(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mac = Column(String)
    ip = Column(String, nullable=False)
