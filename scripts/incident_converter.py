import json
import os
import re
from datetime import datetime
import uuid

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "sample_logs.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "reports", "incident_report.json")


# Auto Severity Calculation
def auto_severity(line):
    line = line.lower()
    if "sql injection" in line:
        return "High"
    elif "phishing" in line:
        return "High"
    elif "password spraying" in line:
        return "Medium"
    elif "brute force" in line:
        return "Medium"
    return "Low"


# MITRE ATT&CK Mapping
def mitre_mapping(line):
    line = line.lower()
    if "brute force" in line:
        return "T1110 - Brute Force"
    elif "password spraying" in line:
        return "T1110.003 - Password Spraying"
    elif "sql injection" in line:
        return "T1190 - Exploit Public-Facing Application"
    elif "phishing" in line:
        return "T1566 - Phishing"
    return "Unknown"


incidents = []

# Read log file
with open(LOG_FILE, "r") as file:
    lines = file.readlines()

for line in lines:
    incident = {}

    # Extract IP
    ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)

    # Build Incident Object
    incident["incident_id"] = str(uuid.uuid4())
    incident["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    incident["ip_address"] = ip_match.group() if ip_match else "N/A"
    incident["severity"] = auto_severity(line)
    incident["mitre_attack"] = mitre_mapping(line)
    incident["raw_log"] = line.strip()

    incidents.append(incident)

# Write JSON Output
with open(OUTPUT_FILE, "w") as outfile:
    json.dump(incidents, outfile, indent=4)

print("✅ Advanced Incident report generated successfully!")