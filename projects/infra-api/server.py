from fastapi import FastAPI
from pydantic import BaseModel
import requests
import psutil
import platform
app = FastAPI()
class LogRequest(BaseModel):
    log: str


@app.get("/")
def home():
    return {"message": "Infra API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/memory")
def memory():
    ram = psutil.virtual_memory()

    return {
        "total_ram_gb": round(ram.total / (1024**3), 2),
        "used_ram_gb": round(ram.used / (1024**3), 2)
    }

@app.get("/system")
def system():
    return {
        "os": platform.system(),
        "processor": platform.processor()
    }
@app.get("/cpu")
def cpu():
    return {
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=1)
    }

@app.post("/analyze")
def analyze_log(request: LogRequest):

    log_text = request.log.lower()

    severity = "low"
    recommendation = "Monitor the system"

    if "disk" in log_text:
        issue = "Disk related issue detected"
        severity = "high"
        recommendation = "Clean disk space or extend storage"

    elif "memory" in log_text:
        issue = "Memory related issue detected"
        severity = "medium"
        recommendation = "Check running processes and memory usage"

    elif "cpu" in log_text:
        issue = "CPU related issue detected"
        severity = "medium"
        recommendation = "Investigate high CPU-consuming services"

    else:
        issue = "Unknown issue"
        recommendation = "Manual investigation required"

    return {
        "received_log": request.log,
        "issue": issue,
        "severity": severity,
        "recommendation": recommendation,
        "message": "Log analyzed successfully"
    }
@app.get("/weather")
def weather():

    url = "https://api.github.com"

    response = requests.get(url)

    return {
        "status_code": response.status_code,
        "response": response.json()
    }