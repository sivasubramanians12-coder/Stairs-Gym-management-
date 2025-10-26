"""
Check ASSESSMENT LOGS database structure
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
DB_ASSESSMENTS = os.getenv("NOTION_DATABASE_ID_ASSESSMENTS")
DB_PATIENTS = os.getenv("NOTION_DATABASE_ID_PATIENTS")

print("="*70)
print(" " * 15 + "ASSESSMENT LOGS DATABASE CHECK")
print("="*70)

# Check ASSESSMENT LOGS structure
print("\n[1/2] Checking ASSESSMENT LOGS database structure...")
db_assessments = notion.databases.retrieve(database_id=DB_ASSESSMENTS)
props = db_assessments.get('properties', {})

print("\nAvailable properties:")
for prop_name, prop_data in props.items():
    prop_type = prop_data.get('type')
    print(f"   - {prop_name}: {prop_type}")

# Get sample assessments
print("\n[2/2] Fetching sample assessment records...")
assessments_response = notion.databases.query(
    database_id=DB_ASSESSMENTS,
    page_size=3
)

assessments = assessments_response.get("results", [])
print(f"✅ Found {len(assessments)} assessment records\n")

if assessments:
    print("Sample Assessment Data:")
    print("-" * 70)

    for i, assessment in enumerate(assessments[:3], 1):
        props = assessment.get("properties", {})

        # Try to extract assessment info
        print(f"\nAssessment {i}:")

        # Common field names
        field_names = [
            "Assessment ID", "Assessment Date", "Date",
            "Strength Score", "Mobility Score", "Balance Score", "Flexibility Score",
            "Overall Score", "Patient", "Assessed By", "Trainer",
            "Notes", "Assessment Notes"
        ]

        for field in field_names:
            if field in props:
                prop_data = props[field]
                prop_type = prop_data.get("type")

                if prop_type == "title":
                    text = prop_data.get("title", [])
                    value = text[0].get("plain_text", "") if text else "N/A"
                elif prop_type == "number":
                    value = prop_data.get("number", "N/A")
                elif prop_type == "date":
                    date_obj = prop_data.get("date", {})
                    value = date_obj.get("start", "N/A") if date_obj else "N/A"
                elif prop_type == "relation":
                    relations = prop_data.get("relation", [])
                    value = f"{len(relations)} item(s)" if relations else "None"
                elif prop_type == "rich_text":
                    text = prop_data.get("rich_text", [])
                    value = text[0].get("plain_text", "")[:50] if text else "N/A"
                else:
                    value = f"({prop_type})"

                print(f"   {field}: {value}")
else:
    print("\n⚠️  No assessment records found in database")

print("\n" + "="*70)
