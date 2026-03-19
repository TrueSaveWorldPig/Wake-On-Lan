from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .api.endpoints import router as api_router
from .database import engine, Base, get_db
from . import crud, utils
import os
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager, contextmanager

import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局变量来存储设备状态
device_statuses = {}

# Get base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create database tables
Base.metadata.create_all(bind=engine)

# 后台任务，用于定期检查设备状态
def check_devices_status():
    logger.info("开始检查设备在线状态...")
    with contextmanager(get_db)() as db:
        devices = crud.get_devices(db)
        if not devices:
            logger.info("数据库中没有设备，跳过检查。")
            return
        
        for device in devices:
            status = utils.is_device_online(device.ip)
            device_statuses[device.id] = status
            logger.info(f"设备 {device.name} (ID: {device.id}) 的在线状态: {'在线' if status else '离线'}")
    logger.info("设备在线状态检查完成。")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动后台任务调度器
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_devices_status, 'interval', seconds=30)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)

# Mount static files and templates using absolute paths
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

# Ensure directories exist (for robustness)
os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Include API router
app.include_router(api_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/devices/status")
def get_devices_status():
    return device_statuses
