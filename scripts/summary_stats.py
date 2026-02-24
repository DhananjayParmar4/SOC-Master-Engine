import json
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "reports", "incident_report.json")

# Load incidents
with open(INPUT_FILE, "r") as f:
    incidents = json.load(f)

# Initialize counters
summary = {
    "High": 0,
    "Medium": 0,
    "Low": 0,
    "Total Incidents": len(incidents)
}

# Count by severity
for incident in incidents:
    sev = incident.get("severity", "Low")
    if sev in summary:
        summary[sev] += 1

# Print summary
print("=== Incident Summary ===")
for key, value in summary.items():
    print(f"{key}: {value}")