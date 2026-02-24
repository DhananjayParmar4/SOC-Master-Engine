import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "reports", "incident_report.json")
OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "reports",
    f"incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
)

# Load JSON
with open(INPUT_FILE, "r") as f:
    incidents = json.load(f)

# Count severity
summary = {"High": 0, "Medium": 0, "Low": 0}
for inc in incidents:
    sev = inc.get("severity", "Low")
    if sev in summary:
        summary[sev] += 1

# Create PDF
c = canvas.Canvas(OUTPUT_FILE, pagesize=A4)
width, height = A4

# Header
c.setFont("Helvetica-Bold", 18)
c.drawString(50, height - 50, "SOC Incident Report")

c.setFont("Helvetica", 11)
c.drawString(50, height - 70, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
c.drawString(50, height - 85, "Analyst: SOC Automation Engine")

# Summary Section
c.setFont("Helvetica-Bold", 14)
c.drawString(50, height - 120, "Incident Summary")

c.setFont("Helvetica", 12)
y = height - 145

for key, val in summary.items():
    if key == "High":
        c.setFillColor(colors.red)
    elif key == "Medium":
        c.setFillColor(colors.orange)
    else:
        c.setFillColor(colors.green)

    c.drawString(60, y, f"{key}: {val}")
    y -= 20

c.setFillColor(colors.black)
c.drawString(60, y, f"Total Incidents: {len(incidents)}")
y -= 40

# Table Header
c.setFont("Helvetica-Bold", 12)
c.drawString(50, y, "IP Address")
c.drawString(180, y, "MITRE Technique")
c.drawString(350, y, "Severity")
c.drawString(430, y, "Timestamp")
y -= 20

c.setFont("Helvetica", 10)

# Table Rows
for inc in incidents:
    if y < 60:
        c.showPage()
        y = height - 60

    c.drawString(50, y, inc["ip_address"])
    c.drawString(180, y, inc["mitre_attack"])

    # Color severity
    if inc["severity"] == "High":
        c.setFillColor(colors.red)
    elif inc["severity"] == "Medium":
        c.setFillColor(colors.orange)
    else:
        c.setFillColor(colors.green)

    c.drawString(350, y, inc["severity"])
    c.setFillColor(colors.black)

    c.drawString(430, y, inc["timestamp"])
    y -= 20

# Footer
c.setFont("Helvetica-Oblique", 9)
c.drawString(50, 30, "Confidential - Internal SOC Use Only")

c.save()

print(f"✅ Professional PDF Report generated at: {OUTPUT_FILE}")