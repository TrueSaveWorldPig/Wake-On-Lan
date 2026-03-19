#!/bin/bash 
 
 MAC="$1" 
 BROADCAST="${2:-255.255.255.255}" 
 PORT="${3:-9}" 
 
 if [ -z "$MAC" ]; then 
   echo "Usage: $0 <MAC> [BROADCAST_IP] [PORT]" 
   exit 1 
 fi 
 
 # 去掉分隔符 
 MAC_CLEAN=$(echo "$MAC" | tr -d ':-') 
 
 # 校验 MAC 长度 
 if [ ${#MAC_CLEAN} -ne 12 ]; then 
   echo "Invalid MAC address" 
   exit 1 
 fi 
 
 # 构造 magic packet 
 PACKET="FFFFFFFFFFFF" 
 for i in {1..16}; do 
   PACKET="${PACKET}${MAC_CLEAN}" 
 done 
 
 # 发送 
 echo "$PACKET" | xxd -r -p | nc -u -w1 "$BROADCAST" "$PORT" 
 
 echo "Sent WOL packet to $MAC via $BROADCAST:$PORT"
