from fastapi import FastAPI
from models.incident import LogRequest, IncidentResponse
from services.analyzer import analyze_infrastructure_log
from services.database import get_connection
import os
from dotenv import load_dotenv
import requests
import psutil
import platform
app = FastAPI()
incidents=[]
load_dotenv()
APP_NAME = os.getenv("APP_NAME")
APP_ENV = os.getenv("APP_ENV")
APP_PORT = os.getenv("APP_PORT")
@app.get("/config")
def get_config():

    return {
        "app_name": APP_NAME,
        "environment": APP_ENV,
        "port": APP_PORT
    }

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
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO incidents (incident_id, timestamp, status, category, issue, severity, recommendation) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (incident["incident_id"], incident["timestamp"], incident["status"], incident["category"], incident["issue"], incident["severity"], incident["recommendation"])
    )
    conn.commit()
    cursor.close()
    conn.close()

    return incident

@app.get("/incidents")
def get_incidents():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT incident_id, timestamp, status, category, issue, severity, recommendation FROM incidents")
    rows=cursor.fetchall()
    incidents = []
    for row in rows:
        incidents.append({
            "incident_id": row[0],
            "timestamp": row[1],
            "status": row[2],
            "category": row[3],
            "issue": row[4],
            "severity": row[5],
            "recommendation": row[6]
        })
    cursor.close()
    conn.close()
    return {
        "total_incidents": len(incidents),
        "incidents": incidents
    }
@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str):

    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT incident_id, timestamp, status, category, issue, severity, recommendation FROM incidents WHERE incident_id = %s", (incident_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {
            "incident_id": row[0],
            "timestamp": row[1],
            "status": row[2],
            "category": row[3],
            "issue": row[4],
            "severity": row[5],
            "recommendation": row[6]
        }

    if not row:
        return {
            "message": "Incident not found"
        }
@app.put("/incidents/{incident_id}")
def update_incident_status(incident_id: str):
    print("Received:", incident_id)
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("UPDATE incidents SET status = 'resolved' WHERE incident_id = %s", (incident_id,))
    conn.commit()
    print("Rows updated:", cursor.rowcount)
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return {
            "message": "Incident not found"
        }
    cursor.execute("SELECT incident_id, timestamp, status, category, issue, severity, recommendation FROM incidents WHERE incident_id = %s", (incident_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "message": "Incident updated successfully",
        "incident": {
            "incident_id": row[0],
            "timestamp": row[1],
            "status": row[2],
            "category": row[3],
            "issue": row[4],
            "severity": row[5],
            "recommendation": row[6]
        }
    }
@app.delete("/incidents/{incident_id}")
def delete_incident(incident_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM incidents
        WHERE incident_id = %s
        """,
        (incident_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:

        cursor.close()
        conn.close()

        return {
            "message": "Incident not found"
        }

    cursor.close()
    conn.close()

    return {
        "message": "Incident deleted successfully"
    }
@app.get("/weather")
def weather():

    url = "https://api.github.com"

    response = requests.get(url)

    return {
        "status_code": response.status_code,
        "response": response.json()
    }