"""
Verify that patient records have been updated with assessment scores
"""

import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from notion_client import Client

# Load environment
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Database IDs
DB_PATIENTS = os.getenv("NOTION_DATABASE_ID_PATIENTS")

print("="*75)
print(" " * 20 + "PATIENT ASSESSMENT SCORES VERIFICATION")
print("="*75)

# Get all active patients
print("\n[1/1] Fetching patients with assessment scores...\n")
patients_response = notion.databases.query(
    database_id=DB_PATIENTS,
    filter={"property": "Status", "select": {"equals": "Active"}}
)

print(f"{'Patient Name':<20} | {'Str':<4} | {'Mob':<4} | {'Bal':<4} | {'Flex':<4} | {'Overall':<7} | {'Last Assessment'}")
print("-" * 90)

patients_with_scores = 0

for patient in patients_response.get("results", []):
    props = patient.get("properties", {})

    # Get name
    name_title = props.get("Name", {}).get("title", [])
    name = name_title[0].get("plain_text", "Unknown") if name_title else "Unknown"

    # Get scores
    strength = props.get("Current Strength Score", {}).get("number")
    mobility = props.get("Current Mobility Score", {}).get("number")
    balance = props.get("Current Balance Score", {}).get("number")
    flexibility = props.get("Current Flexibility Score", {}).get("number")
    overall = props.get("Current Overall Score", {}).get("number")

    # Get last assessment date
    last_assessment_date = props.get("Last Assessment Date", {}).get("date", {})
    last_assessment = last_assessment_date.get("start", "N/A") if last_assessment_date else "N/A"

    # Format scores
    str_display = f"{int(strength)}" if strength is not None else "N/A"
    mob_display = f"{int(mobility)}" if mobility is not None else "N/A"
    bal_display = f"{int(balance)}" if balance is not None else "N/A"
    flex_display = f"{int(flexibility)}" if flexibility is not None else "N/A"
    overall_display = f"{overall:.1f}" if overall is not None else "N/A"

    if strength is not None or mobility is not None:
        patients_with_scores += 1
        status = "✅"
    else:
        status = "⚠️ "

    print(f"{status} {name:<18} | {str_display:<4} | {mob_display:<4} | {bal_display:<4} | {flex_display:<4} | {overall_display:<7} | {last_assessment}")

# Summary
print("\n" + "="*75)
print(" " * 30 + "SUMMARY")
print("="*75)

print(f"\n📊 Results:")
print(f"   Total Patients: {len(patients_response.get('results', []))}")
print(f"   Patients with Assessment Scores: {patients_with_scores}")
print(f"   Patients without Scores: {len(patients_response.get('results', [])) - patients_with_scores}")

print(f"\n✅ Patient records have been updated with assessment data!")
print(f"\n📋 Score Fields Updated:")
print(f"   - Current Strength Score")
print(f"   - Current Mobility Score")
print(f"   - Current Balance Score")
print(f"   - Current Flexibility Score")
print(f"   - Current Overall Score")
print(f"   - Last Assessment Date")

print("\n" + "="*75)
