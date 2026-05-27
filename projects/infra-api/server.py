from fastapi import FastAPI
from models.incident import LogRequest, IncidentResponse
from services.analyzer import analyze_infrastructure_log
import requests
import psutil
import platform
app = FastAPI()
incidents=[]

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

@app.post("/analyze", response_model=IncidentResponse)
def analyze_log(request: LogRequest):
    incident = analyze_infrastructure_log(request.log)

    incidents.append(incident)

    return incident

@app.get("/incidents")
def get_incidents():
    return {
        "total_incidents": len(incidents),
        "incidents": incidents
    }
@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str):

    for incident in incidents:

        if incident["incident_id"] == incident_id:
            return incident

    return {
        "message": "Incident not found"
    }
@app.put("/incidents/{incident_id}")
def update_incident_status(incident_id: str):

    for incident in incidents:

        if incident["incident_id"] == incident_id:

            incident["status"] = "resolved"

            return {
                "message": "Incident updated successfully",
                "incident": incident
            }

    return {
        "message": "Incident not found"
    }
@app.delete("/incidents/{incident_id}")
def delete_incident(incident_id: str):

    for incident in incidents:

        if incident["incident_id"] == incident_id:

            incidents.remove(incident)

            return {
                "message": "Incident deleted successfully"
            }

    return {
        "message": "Incident not found"
    }
@app.get("/weather")
def weather():

    url = "https://api.github.com"

    response = requests.get(url)

    return {
        "status_code": response.status_code,
        "response": response.json()
    }