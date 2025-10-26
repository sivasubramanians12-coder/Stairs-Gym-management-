"""
Fix workout log names to follow proper naming convention:
WO-[PatientID]-[TrainerID]-[Date]-[SessionNumber]
"""

import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime
from collections import defaultdict

# Load environment
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Database IDs
DB_PATIENTS = os.getenv("NOTION_DATABASE_ID_PATIENTS")
DB_TRAINERS = os.getenv("NOTION_DATABASE_ID_TRAINERS")
DB_WORKOUTS = os.getenv("NOTION_DATABASE_ID_WORKOUTS")


def get_patient_id_from_name(patient_page_id):
    """Get the patient ID (numeric) from patient record"""
    try:
        patient = notion.pages.retrieve(page_id=patient_page_id)
        props = patient.get("properties", {})

        # Try different possible field names for patient ID
        for field_name in ["ID", "Id", "Patient ID", "id"]:
            if field_name in props:
                id_prop = props[field_name]

                # Handle unique_id type
                if id_prop.get("type") == "unique_id":
                    unique_id_data = id_prop.get("unique_id")
                    if unique_id_data and unique_id_data.get("number"):
                        patient_id = unique_id_data.get("number")
                        return f"{patient_id:03d}"  # Format as 001, 002, etc.

                # Handle number type
                elif id_prop.get("type") == "number":
                    patient_id = id_prop.get("number")
                    if patient_id:
                        return f"{int(patient_id):03d}"

        # If no ID field found, use page_id last 3 chars
        return patient_page_id[-3:]

    except Exception as e:
        print(f"   Error getting patient ID: {e}")
        return "000"


def get_trainer_id_from_trainer(trainer_page_id):
    """Get the trainer ID from trainer record"""
    try:
        trainer = notion.pages.retrieve(page_id=trainer_page_id)
        props = trainer.get("properties", {})

        # Try different possible field names for trainer ID
        for field_name in ["ID", "Id", "Trainer ID", "id"]:
            if field_name in props:
                id_prop = props[field_name]

                # Handle unique_id type
                if id_prop.get("type") == "unique_id":
                    unique_id_data = id_prop.get("unique_id")
                    if unique_id_data and unique_id_data.get("number"):
                        trainer_id = unique_id_data.get("number")
                        return f"T{trainer_id:03d}"  # Format as T001, T002, etc.

                # Handle number type
                elif id_prop.get("type") == "number":
                    trainer_id = id_prop.get("number")
                    if trainer_id:
                        return f"T{int(trainer_id):03d}"

        # Fallback to last 3 chars of page_id
        return f"T{trainer_page_id[-3:]}"
    except Exception as e:
        print(f"   Error getting trainer ID: {e}")
        return "T000"


def get_text_from_rich_text(rich_text_array):
    """Extract plain text from Notion rich text array"""
    if not rich_text_array:
        return ""
    return "".join([item.get("plain_text", "") for item in rich_text_array])


print("="*70)
print(" " * 15 + "FIX WORKOUT LOG NAMING CONVENTION")
print("="*70)

# Fetch all workout logs
print("\n[1/4] Fetching all workout logs...")
workouts_response = notion.databases.query(
    database_id=DB_WORKOUTS,
    sorts=[{"property": "Date", "direction": "ascending"}]
)

workouts = workouts_response.get("results", [])
print(f"✅ Found {len(workouts)} workout logs")

# Group workouts by patient and date for session numbering
print("\n[2/4] Analyzing workout logs...")
patient_date_sessions = defaultdict(lambda: defaultdict(int))
workout_updates = []

for workout in workouts:
    workout_id = workout["id"]
    props = workout.get("properties", {})

    # Get current Log ID
    current_log_id = get_text_from_rich_text(props.get("Log ID", {}).get("title", []))

    # Get workout date
    workout_date_obj = props.get("Date", {}).get("date", {})
    if not workout_date_obj:
        print(f"   ⚠️  Skipping {workout_id[:8]}... - no date")
        continue

    workout_date = workout_date_obj.get("start", "")
    workout_date_formatted = workout_date.replace("-", "")  # YYYYMMDD

    # Get patient relation
    patient_relations = props.get("Patient", {}).get("relation", [])
    if not patient_relations:
        print(f"   ⚠️  Skipping {workout_id[:8]}... - no patient relation")
        continue

    patient_page_id = patient_relations[0]["id"]
    patient_id = get_patient_id_from_name(patient_page_id)

    # Get trainer relation
    trainer_relations = props.get("Trainer", {}).get("relation", [])
    if trainer_relations:
        trainer_page_id = trainer_relations[0]["id"]
        trainer_id = get_trainer_id_from_trainer(trainer_page_id)
    else:
        trainer_id = "T000"  # Default if no trainer

    # Increment session number for this patient on this date
    patient_date_sessions[patient_page_id][workout_date] += 1
    session_number = patient_date_sessions[patient_page_id][workout_date]

    # Generate new Log ID
    new_log_id = f"WO-{patient_id}-{trainer_id}-{workout_date_formatted}-{session_number:03d}"

    if current_log_id != new_log_id:
        workout_updates.append({
            "workout_id": workout_id,
            "current_id": current_log_id,
            "new_id": new_log_id
        })

print(f"✅ Need to update {len(workout_updates)} workout log names")

# Update workout logs
print("\n[3/4] Updating workout log names...")
updated_count = 0
failed_count = 0

for i, update in enumerate(workout_updates, 1):
    try:
        notion.pages.update(
            page_id=update["workout_id"],
            properties={
                "Log ID": {
                    "title": [{"text": {"content": update["new_id"]}}]
                }
            }
        )
        print(f"   [{i}/{len(workout_updates)}] ✅ {update['current_id']} → {update['new_id']}")
        updated_count += 1
    except Exception as e:
        print(f"   [{i}/{len(workout_updates)}] ❌ Failed: {update['current_id']} - {str(e)[:50]}")
        failed_count += 1

# Verification
print("\n[4/4] Verification...")
verify_response = notion.databases.query(
    database_id=DB_WORKOUTS,
    page_size=5
)

print("\nSample workout log names:")
for i, workout in enumerate(verify_response.get("results", [])[:5], 1):
    props = workout.get("properties", {})
    log_id = get_text_from_rich_text(props.get("Log ID", {}).get("title", []))
    workout_date = props.get("Date", {}).get("date", {}).get("start", "N/A")
    print(f"   {i}. {log_id} (Date: {workout_date})")

# Summary
print("\n" + "="*70)
print(" " * 25 + "SUMMARY")
print("="*70)

print(f"\n📊 Results:")
print(f"   Total Workout Logs: {len(workouts)}")
print(f"   Logs Updated: {updated_count}")
print(f"   Logs Failed: {failed_count}")
print(f"   Logs Unchanged: {len(workouts) - len(workout_updates)}")

if updated_count > 0:
    print(f"\n✅ Successfully updated {updated_count} workout log names!")
    print(f"\n📋 New naming format: WO-[PatientID]-[TrainerID]-[Date]-[SessionNumber]")
    print(f"   Example: WO-001-T003-20251026-001")
else:
    print(f"\nℹ️  All workout logs already follow the correct naming convention")

print("\n" + "="*70)
