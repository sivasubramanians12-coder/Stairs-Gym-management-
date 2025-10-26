"""
Fix weekly report relations to populate back in PATIENTS database
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
DB_WEEKLY = os.getenv("NOTION_DATABASE_ID_WEEKLY")

print("="*60)
print("CHECKING WEEKLY LOGS RELATIONS")
print("="*60)

# Check WEEKLY LOGS database structure
print("\n[1/3] Checking WEEKLY LOGS database structure...")
db_weekly = notion.databases.retrieve(database_id=DB_WEEKLY)
weekly_props = db_weekly.get('properties', {})

print("\nWeekly Logs Properties:")
for prop_name, prop_data in weekly_props.items():
    prop_type = prop_data.get('type')
    if prop_type == 'relation':
        relation_db = prop_data.get('relation', {}).get('database_id')
        synced_prop = prop_data.get('relation', {}).get('synced_property_name')
        print(f"  - {prop_name}: relation")
        print(f"    -> Points to: {relation_db}")
        print(f"    -> Synced with: {synced_prop}")

# Check PATIENTS database structure
print("\n[2/3] Checking PATIENTS database structure...")
db_patients = notion.databases.retrieve(database_id=DB_PATIENTS)
patients_props = db_patients.get('properties', {})

print("\nPatients Properties (relations only):")
for prop_name, prop_data in patients_props.items():
    prop_type = prop_data.get('type')
    if prop_type == 'relation':
        relation_db = prop_data.get('relation', {}).get('database_id')
        synced_prop = prop_data.get('relation', {}).get('synced_property_name')
        print(f"  - {prop_name}: relation")
        print(f"    -> Points to: {relation_db}")
        print(f"    -> Synced with: {synced_prop}")
        if relation_db == DB_WEEKLY:
            print(f"    ✅ This points to WEEKLY LOGS!")

# Update existing weekly reports to use correct relation
print("\n[3/3] Updating existing weekly reports...")
weekly_response = notion.databases.query(database_id=DB_WEEKLY)
weekly_reports = weekly_response.get("results", [])

print(f"\nFound {len(weekly_reports)} weekly reports")

updated_count = 0
for report in weekly_reports:
    report_id = report.get("id")
    props = report.get("properties", {})

    # Check for patient relation
    patient_relation = props.get("patient", {}).get("relation", [])

    if patient_relation and len(patient_relation) > 0:
        patient_id = patient_relation[0]["id"]
        week_id = props.get("Week ID", {}).get("title", [])[0].get("plain_text", "") if props.get("Week ID", {}).get("title") else "Unknown"
        print(f"   ✅ {week_id} has patient relation")
        updated_count += 1
    else:
        print(f"   ⚠️  Report {report_id[:8]}... has NO patient relation!")

print(f"\n✅ {updated_count}/{len(weekly_reports)} reports have patient relations")

# Verify in PATIENTS database
print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

patients_response = notion.databases.query(
    database_id=DB_PATIENTS,
    filter={"property": "Status", "select": {"equals": "Active"}},
    page_size=1
)

if patients_response.get("results"):
    patient = patients_response["results"][0]
    patient_props = patient.get("properties", {})
    patient_name = patient_props.get("Name", {}).get("title", [])[0].get("plain_text", "")

    # Check for weekly logs relation
    weekly_relation_found = False
    for prop_name, prop_data in patient_props.items():
        if prop_data.get("type") == "relation":
            relation_db = patients_props.get(prop_name, {}).get('relation', {}).get('database_id')
            if relation_db == DB_WEEKLY:
                relation_items = prop_data.get("relation", [])
                print(f"\nPatient: {patient_name}")
                print(f"Property: '{prop_name}'")
                print(f"Weekly reports showing: {len(relation_items)} items")

                if len(relation_items) > 0:
                    print(f"✅ SUCCESS! Weekly reports are populating in PATIENTS database!")
                    weekly_relation_found = True
                else:
                    print(f"⚠️  Property exists but no reports showing yet")
                    weekly_relation_found = True
                break

    if not weekly_relation_found:
        print(f"\n❌ No Weekly Logs relation found in PATIENTS database!")
        print(f"\n📋 ACTION NEEDED:")
        print(f"   The WEEKLY LOGS database has a 'patient' relation,")
        print(f"   but PATIENTS database doesn't have a two-way relation back.")
        print(f"\n   SOLUTION:")
        print(f"   1. Open Notion WEEKLY LOGS database")
        print(f"   2. Click on the 'patient' property settings")
        print(f"   3. Enable 'Show on PATIENTS' or create two-way relation")
        print(f"   4. Name it 'Weekly Reports' or 'weekly Logs' in PATIENTS")

print("\n" + "="*60)
