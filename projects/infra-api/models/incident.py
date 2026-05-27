from pydantic import BaseModel

class LogRequest(BaseModel):
    log: str

class IncidentResponse(BaseModel):
    incident_id: str
    timestamp: str
    status: str
    category: str
    summary: str
    issue: str
    severity: str
    recommendation: str