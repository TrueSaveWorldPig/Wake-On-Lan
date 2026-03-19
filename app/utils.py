import subprocess
import os

def send_wol_packet(mac: str, ip: str = None):
    # Construct the command
    # Assuming scripts/wol.sh is relative to project root
    script_path = os.path.join(os.getcwd(), "scripts", "wol.sh")
    cmd = ["bash", script_path, mac]
    if ip:
        cmd.append(ip)
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout
