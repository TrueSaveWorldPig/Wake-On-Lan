import socket
import struct
import os
import platform
import subprocess
import logging

# 配置日志
logger = logging.getLogger(__name__)

def send_wol_packet(mac: str, ip: str = None):
    """
    使用原生 Python Socket 发送 WOL 魔法包。
    """
    # 格式化 MAC 地址 (去掉 : 或 -)
    mac_clean = mac.replace(':', '').replace('-', '')
    if len(mac_clean) != 12:
        raise ValueError("无效的 MAC 地址")

    # 构造魔法包 (6个 FF + 16次 MAC 地址)
    data = bytes.fromhex('FFFFFF' * 6 + mac_clean * 16)
    
    # 确定广播地址
    broadcast_ip = ip if ip else '255.255.255.255'
    
    # 发送 UDP 包
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data, (broadcast_ip, 9))
    
    return f"Sent WOL magic packet to {mac} via {broadcast_ip}:9"

def is_device_online(ip: str) -> bool:
    """
    使用 ping 命令检查设备是否在线。
    """
    if not ip:
        return False
    
    system_type = platform.system().lower()
    
    # 默认超时设置
    timeout_val = "1"
    
    if system_type == 'windows':
        # Windows: -n 1, -w 1000 (ms)
        command = ['ping', '-n', '1', '-w', '1000', ip]
    elif system_type == 'darwin':
        # macOS: -c 1, -W 1000 (ms) 或 -t 1 (s)
        # 这里使用 -W 1000 表示等待 1000 毫秒
        command = ['ping', '-c', '1', '-W', '1000', ip]
    else:
        # Linux 和其他: -c 1, -W 1 (s)
        command = ['ping', '-c', '1', '-W', '1', ip]
    
    # 执行命令并返回状态
    try:
        # logger.debug(f"Executing ping command: {' '.join(command)}")
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        return True
    except subprocess.TimeoutExpired:
        logger.warning(f"Ping command timed out for IP: {ip}")
        return False
    except subprocess.CalledProcessError:
        # ping 失败通常意味着设备不在线
        return False
    except Exception as e:
        logger.error(f"Error while pinging {ip}: {str(e)}")
        return False
