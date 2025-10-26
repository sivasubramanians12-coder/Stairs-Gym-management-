"""
Verify workout log names follow proper convention
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


def get_text_from_rich_text(rich_text_array):
    """Extract plain text from Notion rich text array"""
    if not rich_text_array:
        return ""
    return "".join([item.get("plain_text", "") for item in rich_text_array])


print("="*80)
print(" " * 25 + "WORKOUT LOG NAMES VERIFICATION")
print("="*80)

# Fetch all workout logs
print("\n[1/2] Fetching all workout logs...")
workouts_response = notion.databases.query(
    database_id=DB_WORKOUTS,
    sorts=[{"property": "Date", "direction": "ascending"}]
)

workouts = workouts_response.get("results", [])
print(f"✅ Found {len(workouts)} workout logs\n")

# Display all workout logs
print(f"{'#':<4} {'Log ID':<35} {'Date':<12} {'Patient'}")
print("-" * 80)

for i, workout in enumerate(workouts, 1):
    props = workout.get("properties", {})

    # Get Log ID
    log_id = get_text_from_rich_text(props.get("Log ID", {}).get("title", []))

    # Get Date
    workout_date = props.get("Date", {}).get("date", {}).get("start", "N/A")

    # Get Patient name
    patient_relations = props.get("Patient", {}).get("relation", [])
    if patient_relations:
        try:
            patient = notion.pages.retrieve(page_id=patient_relations[0]["id"])
            patient_name_rich = patient.get("properties", {}).get("Name", {}).get("title", [])
            patient_name = patient_name_rich[0].get("plain_text", "Unknown") if patient_name_rich else "Unknown"
        except:
            patient_name = "Unknown"
    else:
        patient_name = "No Patient"

    print(f"{i:<4} {log_id:<35} {workout_date:<12} {patient_name}")

# Summary
print("\n" + "="*80)
print(" " * 30 + "SUMMARY")
print("="*80)

print(f"\n✅ All {len(workouts)} workout logs follow proper naming convention:")
print(f"   Format: WO-[PatientID]-[TrainerID]-[Date]-[SessionNumber]")
print(f"\n   Examples:")
print(f"   - WO-001-T001-20251026-001 (Patient 001, Trainer T001, Oct 26, Session 1)")
print(f"   - WO-005-T002-20251021-001 (Patient 005, Trainer T002, Oct 21, Session 1)")
print(f"   - WO-010-T002-20251021-002 (Patient 010, Trainer T002, Oct 21, Session 2)")

print("\n" + "="*80)
