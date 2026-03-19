import socket
import struct
import os
import platform
import subprocess

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
    
    # 根据操作系统选择 ping 参数
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-W', '1', ip]
    
    # 执行命令并返回状态
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
