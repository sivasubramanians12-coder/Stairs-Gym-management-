"""
Check patient ID structure and populate if needed
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

print("="*70)
print(" " * 20 + "CHECK PATIENT IDs")
print("="*70)

# Get database structure
print("\n[1/2] Checking PATIENTS database structure...")
db_patients = notion.databases.retrieve(database_id=DB_PATIENTS)
props = db_patients.get('properties', {})

print("\nAvailable properties:")
has_id_field = False
for prop_name, prop_data in props.items():
    prop_type = prop_data.get('type')
    print(f"   - {prop_name}: {prop_type}")
    if prop_name == "Id" or prop_name == "ID" or prop_name == "Patient ID":
        has_id_field = True
        print(f"     ✅ Found ID field!")

if not has_id_field:
    print(f"\n⚠️  No 'Id' or 'Patient ID' field found!")
    print(f"   Recommendation: Add a 'unique_id' or 'number' property called 'Patient ID' in Notion")

# Get all patients
print("\n[2/2] Fetching patient records...")
patients_response = notion.databases.query(
    database_id=DB_PATIENTS,
    filter={"property": "Status", "select": {"equals": "Active"}}
)

print(f"\n{'Name':<20} | {'Status':<10} | {'Page ID (last 6)'}")
print("-" * 60)

for patient in patients_response.get("results", []):
    patient_id = patient["id"]
    props = patient.get("properties", {})

    # Get name
    name_title = props.get("Name", {}).get("title", [])
    name = name_title[0].get("plain_text", "") if name_title else "Unknown"

    # Get status
    status = props.get("Status", {}).get("select", {}).get("name", "N/A")

    # Check for ID field
    patient_numeric_id = None
    for prop_name in ["Id", "ID", "Patient ID", "id"]:
        if prop_name in props:
            id_prop = props[prop_name]
            if id_prop.get("type") == "unique_id":
                patient_numeric_id = id_prop.get("unique_id", {}).get("number")
            elif id_prop.get("type") == "number":
                patient_numeric_id = id_prop.get("number")

    page_id_short = patient_id[-6:]

    if patient_numeric_id:
        print(f"{name:<20} | {status:<10} | {page_id_short} (ID: {patient_numeric_id:03d})")
    else:
        print(f"{name:<20} | {status:<10} | {page_id_short} (No numeric ID)")

print("\n" + "="*70)
print("RECOMMENDATION")
print("="*70)

if not has_id_field:
    print("""
Since your PATIENTS database doesn't have a numeric ID field,
the system is using page IDs (hexadecimal) for workout log naming.

OPTIONS:

1. Keep current naming (using hex page IDs):
   - Pros: Unique, works immediately
   - Cons: Not as clean (WO-a29-T002-20251025-001)

2. Add a Patient ID field in Notion:
   - Go to PATIENTS database
   - Add property: "Patient ID" (type: Number or Unique ID)
   - Manually assign IDs: 1, 2, 3, 4...
   - Re-run: python fix_workout_log_names.py
   - Pros: Clean names (WO-001-T002-20251025-001)
   - Cons: Requires manual setup

3. Use patient name abbreviations:
   - Example: WO-ROBE-T002-20251025-001
   - Pros: Human-readable
   - Cons: Not standardized
""")
else:
    print("\n✅ Patient ID field exists!")
    print("   Verify that all patients have numeric IDs assigned.")

print("\n" + "="*70)
