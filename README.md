# Wake On LAN 管理工具

这是一个轻量级的 Wake On LAN (WOL) 远程唤醒管理工具，支持通过 Web 页面管理设备并发送唤醒指令。支持 Docker 部署，适合在家庭服务器或局域网中使用。

## 🌟 主要功能

- **设备管理**: 支持添加、查看和删除局域网内的设备（名称、MAC 地址、IP 地址）。
- **一键唤醒**: 在 Web 界面一键向指定设备发送 WOL 魔法包。
- **持久化存储**: 使用 SQLite 数据库保存设备信息，重启不丢失。
- **Docker 支持**: 提供 Dockerfile 和 docker-compose 配置文件，一键部署。
- **现代化 UI**: 基于 Tailwind CSS 构建的简洁、响应式前端界面。

## 🚀 快速开始

### 方式一：使用 Docker (推荐)

这是最简单且推荐的部署方式，确保你的 Docker 环境支持 `host` 网络模式（通常在 Linux 上表现最佳）。

1. 克隆或下载本项目到本地。
2. 在项目根目录下执行：
   ```bash
   docker-compose up -d
   ```
3. 访问浏览器：`http://localhost:8000`

### 方式二：本地运行

1. **环境准备**:
   - Python 3.10+
   - 安装系统依赖 (仅 Linux/macOS): `nc` (netcat) 和 `xxd` (用于执行 WOL 脚本)。

2. **安装 Python 依赖**:
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务**:
   ```bash
   python3 main.py
   ```
4. 访问浏览器：`http://localhost:8000`

## 📂 项目结构

```text
.
├── main.py              # FastAPI 后端程序，提供 API 接口
├── wol.sh               # WOL 核心脚本，负责构造和发送魔法包
├── templates/
│   └── index.html       # 前端 Web 页面
├── static/              # 静态资源目录
├── Dockerfile           # Docker 构建文件
├── docker-compose.yml   # Docker Compose 配置文件
└── requirements.txt     # Python 依赖列表
```

## ⚠️ 注意事项

- **网络权限**: Wake On LAN 依赖于在局域网内发送 UDP 广播包。在 Docker 中部署时，必须使用 `network_mode: host`，否则广播包可能无法到达目标网段。
- **BIOS 设置**: 确保目标设备在 BIOS/UEFI 中已开启 "Wake On LAN" 或类似的电源管理选项。
- **操作系统设置**: 确保目标设备的网卡驱动设置中已允许 "魔术封包唤醒"。

## 🛠️ 技术栈

- **后端**: FastAPI, SQLAlchemy (SQLite), Pydantic
- **前端**: Tailwind CSS, JavaScript (Fetch API)
- **容器化**: Docker, Docker Compose
