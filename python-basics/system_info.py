import platform
import socket
import psutil

print("===== SYSTEM INFORMATION =====")

print(f"Hostname: {socket.gethostname()}")
print(f"Operating System: {platform.system()}")
print(f"OS Version: {platform.version()}")
print(f"Processor: {platform.processor()}")

print("\n===== MEMORY =====")
memory = psutil.virtual_memory()
print(f"Total RAM: {round(memory.total / (1024**3), 2)} GB")
print(f"Used RAM: {round(memory.used / (1024**3), 2)} GB")

print("\n===== DISK =====")
disk = psutil.disk_usage('/')
print(f"Total Disk: {round(disk.total / (1024**3), 2)} GB")
print(f"Used Disk: {round(disk.used / (1024**3), 2)} GB")