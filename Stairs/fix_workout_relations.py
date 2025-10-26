"""
Fix workout log relations to populate back in PATIENTS database
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

print("="*60)
print("FIXING WORKOUT LOG RELATIONS")
print("="*60)

# Get all workout logs
print("\n[1/3] Fetching all workout logs...")
workouts_response = notion.databases.query(database_id=DB_WORKOUTS)
workout_logs = workouts_response.get("results", [])
print(f"✅ Found {len(workout_logs)} workout logs")

# Check and update each workout log
print("\n[2/3] Updating relations...")
updated_count = 0

for workout in workout_logs:
    workout_id = workout.get("id")
    props = workout.get("properties", {})

    # Check if "Patient" relation exists and has a value
    patient_relation = props.get("Patient", {}).get("relation", [])
    emoji_relation = props.get("👫 PATIENTS", {}).get("relation", [])

    if patient_relation and len(patient_relation) > 0:
        patient_id = patient_relation[0]["id"]
        print(f"   ✅ Workout {workout_id[:8]}... already has Patient relation")

        # Also update the emoji relation if it exists
        if "👫 PATIENTS" in props:
            try:
                notion.pages.update(
                    page_id=workout_id,
                    properties={
                        "👫 PATIENTS": {"relation": [{"id": patient_id}]}
                    }
                )
                print(f"      ✅ Updated emoji relation too")
                updated_count += 1
            except Exception as e:
                print(f"      ⚠️  Could not update emoji relation: {e}")
    elif emoji_relation and len(emoji_relation) > 0:
        patient_id = emoji_relation[0]["id"]
        print(f"   ✅ Workout {workout_id[:8]}... has emoji relation")

        # Copy to Patient relation
        try:
            notion.pages.update(
                page_id=workout_id,
                properties={
                    "Patient": {"relation": [{"id": patient_id}]}
                }
            )
            print(f"      ✅ Copied to Patient relation")
            updated_count += 1
        except Exception as e:
            print(f"      ⚠️  Could not copy: {e}")
    else:
        print(f"   ⚠️  Workout {workout_id[:8]}... has NO patient relation!")

print(f"\n[3/3] Summary:")
print(f"✅ Updated {updated_count} workout logs")

print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

# Check one patient to see if workouts appear
print("\nChecking if relations now appear in PATIENTS database...")
patients_response = notion.databases.query(
    database_id=DB_PATIENTS,
    filter={"property": "Status", "select": {"equals": "Active"}},
    page_size=1
)

if patients_response.get("results"):
    patient = patients_response["results"][0]
    patient_props = patient.get("properties", {})
    patient_name = patient_props.get("Name", {}).get("title", [])[0].get("plain_text", "")

    workout_logs_relation = patient_props.get("Workout logs", {}).get("relation", [])

    print(f"\nPatient: {patient_name}")
    print(f"Workout logs showing: {len(workout_logs_relation)} items")

    if len(workout_logs_relation) > 0:
        print(f"✅ SUCCESS! Workouts are now populating in PATIENTS database!")
    else:
        print(f"❌ Still not populating. This means the relation is NOT two-way.")
        print(f"\n📋 MANUAL FIX NEEDED:")
        print(f"   1. Open Notion and go to WORKOUT LOGS database")
        print(f"   2. Click on the 'Patient' or '👫 PATIENTS' property settings")
        print(f"   3. In the relation settings, make sure it's synced with 'Workout logs' property in PATIENTS")
        print(f"   4. If not synced, you'll need to recreate the relation as a two-way relation")

print("\n" + "="*60)
