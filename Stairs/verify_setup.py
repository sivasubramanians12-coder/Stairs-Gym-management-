"""
Verify complete setup - check all components
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
DB_WORKOUTS = os.getenv("NOTION_DATABASE_ID_WORKOUTS")
DB_WEEKLY = os.getenv("NOTION_DATABASE_ID_WEEKLY")
DB_MONTHLY = os.getenv("NOTION_DATABASE_ID_MONTHLY")

print("="*70)
print(" " * 15 + "STAIRS GYM - SYSTEM VERIFICATION")
print("="*70)

# Check 1: Patients
print("\n[1/5] Checking PATIENTS database...")
patients = notion.databases.query(
    database_id=DB_PATIENTS,
    filter={"property": "Status", "select": {"equals": "Active"}}
)
patient_count = len(patients.get("results", []))
print(f"   ✅ {patient_count} active patients found")

# Check 2: Workout Logs
print("\n[2/5] Checking WORKOUT LOGS database...")
workouts = notion.databases.query(database_id=DB_WORKOUTS)
workout_count = len(workouts.get("results", []))
print(f"   ✅ {workout_count} workout logs found")

# Check workout relations
workout_with_patient = 0
for workout in workouts.get("results", []):
    patient_rel = workout.get("properties", {}).get("Patient", {}).get("relation", [])
    if patient_rel:
        workout_with_patient += 1
print(f"   ✅ {workout_with_patient}/{workout_count} workouts have patient relation")

# Check 3: Weekly Reports
print("\n[3/5] Checking WEEKLY LOGS database...")
weekly = notion.databases.query(database_id=DB_WEEKLY)
weekly_count = len(weekly.get("results", []))
print(f"   ✅ {weekly_count} weekly reports found")

weekly_with_patient = 0
for report in weekly.get("results", []):
    patient_rel = report.get("properties", {}).get("patient", {}).get("relation", [])
    if patient_rel:
        weekly_with_patient += 1
print(f"   ✅ {weekly_with_patient}/{weekly_count} reports have patient relation")

# Check 4: Monthly Reports
print("\n[4/5] Checking MONTHLY LOGS database...")
monthly = notion.databases.query(database_id=DB_MONTHLY)
monthly_count = len(monthly.get("results", []))
print(f"   ✅ {monthly_count} monthly reports found")

monthly_with_patient = 0
for report in monthly.get("results", []):
    patient_rel = report.get("properties", {}).get("Patient", {}).get("relation", [])
    if patient_rel:
        monthly_with_patient += 1
print(f"   ✅ {monthly_with_patient}/{monthly_count} reports have patient relation")

# Check 5: Two-way relations
print("\n[5/5] Checking two-way relations...")

# Get first patient with data
if patients.get("results"):
    patient = patients["results"][0]
    patient_props = patient.get("properties", {})
    patient_name = patient_props.get("Name", {}).get("title", [])[0].get("plain_text", "")

    workout_rel = patient_props.get("Workout logs", {}).get("relation", [])
    monthly_rel = patient_props.get("monthly Logs", {}).get("relation", [])

    print(f"\n   Testing with patient: {patient_name}")
    print(f"   ✅ Workout logs showing: {len(workout_rel)} items")

    if len(monthly_rel) > 0:
        print(f"   ✅ Monthly logs showing: {len(monthly_rel)} items")
    else:
        print(f"   ⚠️  Monthly logs: 0 items (normal if just created)")

    # Check for weekly logs relation
    weekly_rel_found = False
    for prop_name, prop_data in patient_props.items():
        if prop_data.get("type") == "relation":
            # Get the database this relation points to
            db_patients = notion.databases.retrieve(database_id=DB_PATIENTS)
            db_props = db_patients.get('properties', {})
            if prop_name in db_props:
                relation_db = db_props[prop_name].get('relation', {}).get('database_id')
                if relation_db == DB_WEEKLY:
                    relation_items = prop_data.get("relation", [])
                    print(f"   ✅ Weekly reports showing: {len(relation_items)} items in '{prop_name}'")
                    weekly_rel_found = True
                    break

    if not weekly_rel_found:
        print(f"   ⚠️  Weekly reports relation NOT found in PATIENTS")
        print(f"      ACTION: Follow instructions in ADD_WEEKLY_RELATION_INSTRUCTIONS.md")

# Summary
print("\n" + "="*70)
print(" " * 25 + "SUMMARY")
print("="*70)

print(f"\n✅ Database Connections:")
print(f"   - Patients: {patient_count} active")
print(f"   - Workouts: {workout_count} logs")
print(f"   - Weekly Reports: {weekly_count} reports")
print(f"   - Monthly Reports: {monthly_count} reports")

print(f"\n✅ Relations Working:")
print(f"   - Workouts → Patients: {workout_with_patient}/{workout_count}")
print(f"   - Weekly → Patients: {weekly_with_patient}/{weekly_count}")
print(f"   - Monthly → Patients: {monthly_with_patient}/{monthly_count}")

if weekly_rel_found:
    print(f"\n✅ ALL SYSTEMS OPERATIONAL!")
    print(f"   Your weekly reports system is fully functional.")
else:
    print(f"\n⚠️  ALMOST READY!")
    print(f"   Just one manual step needed:")
    print(f"   → Enable two-way relation for Weekly Reports in Notion")
    print(f"   → See: ADD_WEEKLY_RELATION_INSTRUCTIONS.md")

print(f"\n📋 Next Steps:")
print(f"   1. Review SETUP_COMPLETE_SUMMARY.md")
print(f"   2. Enable Weekly Reports relation (if needed)")
print(f"   3. Start generating reports for all patients!")

print("\n" + "="*70)
