from datetime import datetime
import uuid

from datetime import datetime
import uuid

def analyze_infrastructure_log(log_text: str):

    log_text = log_text.lower()

    severity = "low"
    recommendation = "Monitor the system"
    issue = "Unknown issue"
    category = "general"

    if "disk" in log_text:
        issue = "Disk related issue detected"
        severity = "high"
        category = "storage"
        recommendation = "Clean disk space or extend storage"

    elif "memory" in log_text:
        issue = "Memory related issue detected"
        severity = "medium"
        category = "memory"
        recommendation = "Check running processes and memory usage"

    elif "cpu" in log_text:
        issue = "CPU related issue detected"
        severity = "medium"
        category = "compute"
        recommendation = "Investigate high CPU-consuming services"

    incident_id = f"INC-{uuid.uuid4().hex[:8]}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary = f"""
    Infrastructure Incident Summary

    Incident ID: {incident_id}
    Issue: {issue}
    Severity: {severity}
    Category: {category}

    Recommendation:
    {recommendation}
    """

    incident = {
        "incident_id": incident_id,
        "timestamp": timestamp,
        "status": "open",
        "category": category,
        "summary": summary,
        "issue": issue,
        "severity": severity,
        "recommendation": recommendation
    }

    return incident