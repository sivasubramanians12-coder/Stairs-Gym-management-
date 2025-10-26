"""
Fix weekly and monthly log names to follow proper naming convention:
WEEKLY-[PatientID]-W[WeekNumber]-[Year]
MONTHLY-[PatientID]-[MonthYear]
"""

import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime

# Load environment
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Database IDs
DB_PATIENTS = os.getenv("NOTION_DATABASE_ID_PATIENTS")
DB_WEEKLY = os.getenv("NOTION_DATABASE_ID_WEEKLY")
DB_MONTHLY = os.getenv("NOTION_DATABASE_ID_MONTHLY")


def get_text_from_rich_text(rich_text_array):
    """Extract plain text from Notion rich text array"""
    if not rich_text_array:
        return ""
    return "".join([item.get("plain_text", "") for item in rich_text_array])


def get_patient_id(patient_page_id):
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


print("="*75)
print(" " * 15 + "FIX WEEKLY & MONTHLY LOG NAMING CONVENTION")
print("="*75)

# ========== FIX WEEKLY LOGS ==========
print("\n[1/4] Fixing WEEKLY LOGS...")
weekly_response = notion.databases.query(database_id=DB_WEEKLY)
weekly_logs = weekly_response.get("results", [])
print(f"✅ Found {len(weekly_logs)} weekly logs")

weekly_updates = []

for log in weekly_logs:
    log_id_page = log["id"]
    props = log.get("properties", {})

    # Get current Week ID
    current_week_id = get_text_from_rich_text(props.get("Week ID", {}).get("title", []))

    # Get patient relation
    patient_relations = props.get("patient", {}).get("relation", [])
    if not patient_relations:
        print(f"   ⚠️  Skipping {log_id_page[:8]}... - no patient relation")
        continue

    patient_page_id = patient_relations[0]["id"]
    patient_id = get_patient_id(patient_page_id)

    # Get week start date to determine week number and year
    week_start_obj = props.get("Week Start", {}).get("date", {})
    if not week_start_obj:
        print(f"   ⚠️  Skipping {log_id_page[:8]}... - no week start date")
        continue

    week_start_str = week_start_obj.get("start", "")
    week_start_date = datetime.strptime(week_start_str, "%Y-%m-%d")
    week_number = week_start_date.isocalendar()[1]
    year = week_start_date.year

    # Generate new Week ID: WEEKLY-[PatientID]-W[WeekNumber]-[Year]
    new_week_id = f"WEEKLY-{patient_id}-W{week_number:02d}-{year}"

    if current_week_id != new_week_id:
        weekly_updates.append({
            "log_id": log_id_page,
            "current_id": current_week_id,
            "new_id": new_week_id
        })

print(f"✅ Need to update {len(weekly_updates)} weekly log names")

# Update weekly logs
print("\n[2/4] Updating weekly log names...")
weekly_updated = 0
weekly_failed = 0

for i, update in enumerate(weekly_updates, 1):
    try:
        notion.pages.update(
            page_id=update["log_id"],
            properties={
                "Week ID": {
                    "title": [{"text": {"content": update["new_id"]}}]
                }
            }
        )
        print(f"   [{i}/{len(weekly_updates)}] ✅ {update['current_id']} → {update['new_id']}")
        weekly_updated += 1
    except Exception as e:
        print(f"   [{i}/{len(weekly_updates)}] ❌ Failed: {update['current_id']} - {str(e)[:50]}")
        weekly_failed += 1

# ========== FIX MONTHLY LOGS ==========
print("\n[3/4] Fixing MONTHLY LOGS...")
monthly_response = notion.databases.query(database_id=DB_MONTHLY)
monthly_logs = monthly_response.get("results", [])
print(f"✅ Found {len(monthly_logs)} monthly logs")

monthly_updates = []

for log in monthly_logs:
    log_id_page = log["id"]
    props = log.get("properties", {})

    # Get current Month ID
    current_month_id = get_text_from_rich_text(props.get("Month ID", {}).get("title", []))

    # Get patient relation
    patient_relations = props.get("Patient", {}).get("relation", [])
    if not patient_relations:
        print(f"   ⚠️  Skipping {log_id_page[:8]}... - no patient relation")
        continue

    patient_page_id = patient_relations[0]["id"]
    patient_id = get_patient_id(patient_page_id)

    # Get month start date to determine month name and year
    month_start_obj = props.get("Month Start", {}).get("date", {})
    if not month_start_obj:
        print(f"   ⚠️  Skipping {log_id_page[:8]}... - no month start date")
        continue

    month_start_str = month_start_obj.get("start", "")
    month_start_date = datetime.strptime(month_start_str, "%Y-%m-%d")
    month_name = month_start_date.strftime("%B").upper()[:3]  # JAN, FEB, MAR, etc.
    year = month_start_date.year

    # Generate new Month ID: MONTHLY-[PatientID]-[MonthYear]
    new_month_id = f"MONTHLY-{patient_id}-{month_name}{year}"

    if current_month_id != new_month_id:
        monthly_updates.append({
            "log_id": log_id_page,
            "current_id": current_month_id,
            "new_id": new_month_id
        })

print(f"✅ Need to update {len(monthly_updates)} monthly log names")

# Update monthly logs
print("\n[4/4] Updating monthly log names...")
monthly_updated = 0
monthly_failed = 0

for i, update in enumerate(monthly_updates, 1):
    try:
        notion.pages.update(
            page_id=update["log_id"],
            properties={
                "Month ID": {
                    "title": [{"text": {"content": update["new_id"]}}]
                }
            }
        )
        print(f"   [{i}/{len(monthly_updates)}] ✅ {update['current_id']} → {update['new_id']}")
        monthly_updated += 1
    except Exception as e:
        print(f"   [{i}/{len(monthly_updates)}] ❌ Failed: {update['current_id']} - {str(e)[:50]}")
        monthly_failed += 1

# Summary
print("\n" + "="*75)
print(" " * 30 + "SUMMARY")
print("="*75)

print(f"\n📊 Weekly Logs:")
print(f"   Total Logs: {len(weekly_logs)}")
print(f"   Logs Updated: {weekly_updated}")
print(f"   Logs Failed: {weekly_failed}")
print(f"   Logs Unchanged: {len(weekly_logs) - len(weekly_updates)}")

print(f"\n📊 Monthly Logs:")
print(f"   Total Logs: {len(monthly_logs)}")
print(f"   Logs Updated: {monthly_updated}")
print(f"   Logs Failed: {monthly_failed}")
print(f"   Logs Unchanged: {len(monthly_logs) - len(monthly_updates)}")

if weekly_updated > 0 or monthly_updated > 0:
    print(f"\n✅ Successfully updated log names!")
    print(f"\n📋 New naming formats:")
    print(f"   Weekly:  WEEKLY-[PatientID]-W[WeekNumber]-[Year]")
    print(f"            Example: WEEKLY-001-W43-2025")
    print(f"   Monthly: MONTHLY-[PatientID]-[MonthYear]")
    print(f"            Example: MONTHLY-001-OCT2025")
else:
    print(f"\nℹ️  All logs already follow the correct naming convention")

print("\n" + "="*75)
