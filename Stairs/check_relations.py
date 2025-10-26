"""
Check database relations
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
print("CHECKING DATABASE RELATIONS")
print("="*60)

# Check WORKOUT LOGS database
print("\n[1] WORKOUT LOGS Database Properties:")
print("-"*60)
db_workouts = notion.databases.retrieve(database_id=DB_WORKOUTS)
for prop_name, prop_data in db_workouts.get('properties', {}).items():
    prop_type = prop_data.get('type')
    if prop_type == 'relation':
        relation_db = prop_data.get('relation', {}).get('database_id')
        synced_prop = prop_data.get('relation', {}).get('synced_property_name')
        print(f"  - {prop_name}: relation")
        print(f"    -> Points to database: {relation_db}")
        print(f"    -> Synced property: {synced_prop}")
    else:
        print(f"  - {prop_name}: {prop_type}")

# Check PATIENTS database
print("\n[2] PATIENTS Database Properties:")
print("-"*60)
db_patients = notion.databases.retrieve(database_id=DB_PATIENTS)
for prop_name, prop_data in db_patients.get('properties', {}).items():
    prop_type = prop_data.get('type')
    if prop_type == 'relation':
        relation_db = prop_data.get('relation', {}).get('database_id')
        synced_prop = prop_data.get('relation', {}).get('synced_property_name')
        print(f"  - {prop_name}: relation")
        print(f"    -> Points to database: {relation_db}")
        print(f"    -> Synced property: {synced_prop}")
    else:
        print(f"  - {prop_name}: {prop_type}")

print("\n" + "="*60)
print("ANALYSIS")
print("="*60)

# Find the relation from WORKOUT LOGS to PATIENTS
workout_patient_relation = None
for prop_name, prop_data in db_workouts.get('properties', {}).items():
    if prop_data.get('type') == 'relation':
        relation_db = prop_data.get('relation', {}).get('database_id')
        if relation_db == DB_PATIENTS:
            workout_patient_relation = prop_name
            synced_prop = prop_data.get('relation', {}).get('synced_property_name')
            print(f"\n✅ WORKOUT LOGS -> PATIENTS relation found:")
            print(f"   Property in WORKOUT LOGS: '{prop_name}'")
            print(f"   Synced property in PATIENTS: '{synced_prop}'")
            break

if not workout_patient_relation:
    print(f"\n❌ No relation found from WORKOUT LOGS to PATIENTS!")
    print(f"   You need to create this relation in Notion.")

print("\n" + "="*60)
