"""
Create sample workout logs for testing
"""

import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime, timedelta

# Load environment
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Database IDs
DB_PATIENTS = os.getenv("NOTION_DATABASE_ID_PATIENTS")
DB_TRAINERS = os.getenv("NOTION_DATABASE_ID_TRAINERS")
DB_WORKOUTS = os.getenv("NOTION_DATABASE_ID_WORKOUTS")

print("="*60)
print("CREATING SAMPLE WORKOUT LOGS")
print("="*60)

# Get first 3 active patients
print("\n[1/4] Fetching patients...")
patients_response = notion.databases.query(
    database_id=DB_PATIENTS,
    filter={"property": "Status", "select": {"equals": "Active"}},
    page_size=3
)

patients = []
for page in patients_response.get("results", []):
    props = page.get("properties", {})
    name_prop = props.get("Name", {}).get("title", [])
    name = name_prop[0].get("plain_text", "") if name_prop else "Unknown"
    patients.append({"id": page.get("id"), "name": name})

print(f"✅ Found {len(patients)} patients")

# Get first trainer
print("\n[2/4] Fetching trainer...")
trainers_response = notion.databases.query(
    database_id=DB_TRAINERS,
    page_size=1
)
trainer_id = trainers_response["results"][0]["id"] if trainers_response["results"] else None
print(f"✅ Trainer ID: {trainer_id[:8]}...")

# Create sample workouts for each patient
print("\n[3/4] Creating sample workout logs...")

sample_workouts = [
    {
        "days_ago": 1,
        "duration": 60,
        "exercises": "Bench Press 3x10 @ 80kg, Squats 3x12 @ 100kg, Shoulder Press 3x8 @ 40kg",
        "focus_areas": ["Strength", "Core"],
        "noticed": "Excellent form on all exercises, high energy levels throughout session",
        "improving": "Strength increasing steadily, better depth on squats, shoulder stability improved",
        "concerns": "Slight lower back tightness after squats, advised stretching routine",
        "rating": "Excellent"
    },
    {
        "days_ago": 3,
        "duration": 45,
        "exercises": "Deadlifts 3x8 @ 120kg, Pull-ups 3x8, Barbell Rows 3x10 @ 70kg",
        "focus_areas": ["Strength"],
        "noticed": "Good progression on deadlifts, maintaining proper back alignment",
        "improving": "Pull-up count increasing, grip strength better",
        "concerns": "None - session went smoothly",
        "rating": "Good"
    },
    {
        "days_ago": 5,
        "duration": 50,
        "exercises": "Leg Press 3x15 @ 150kg, Lunges 3x12 per leg, Calf Raises 3x20",
        "focus_areas": ["Strength", "Mobility"],
        "noticed": "Better balance during lunges, more controlled movements",
        "improving": "Leg strength improving, mobility in hip flexors better",
        "concerns": "Minor knee discomfort on leg press - reduced weight slightly",
        "rating": "Good"
    }
]

created_count = 0
session_counter = {}  # Track session numbers per patient per date

for patient in patients:
    print(f"\n   Creating workouts for {patient['name']}...")

    # Get patient ID
    try:
        patient_page = notion.pages.retrieve(page_id=patient['id'])
        patient_props = patient_page.get("properties", {})
        patient_id = None

        # Get ID field
        for field_name in ["ID", "Id", "Patient ID", "id"]:
            if field_name in patient_props:
                id_prop = patient_props[field_name]
                if id_prop.get("type") == "unique_id":
                    unique_id_data = id_prop.get("unique_id")
                    if unique_id_data and unique_id_data.get("number"):
                        patient_id = f"{unique_id_data.get('number'):03d}"
                        break
                elif id_prop.get("type") == "number":
                    num = id_prop.get("number")
                    if num:
                        patient_id = f"{int(num):03d}"
                        break

        if not patient_id:
            patient_id = patient['id'][-3:]
    except:
        patient_id = patient['id'][-3:]

    # Get trainer ID
    trainer_page = notion.pages.retrieve(page_id=trainer_id)
    trainer_props = trainer_page.get("properties", {})
    trainer_numeric_id = "000"

    for field_name in ["ID", "Id", "Trainer ID", "id"]:
        if field_name in trainer_props:
            id_prop = trainer_props[field_name]
            if id_prop.get("type") == "unique_id":
                unique_id_data = id_prop.get("unique_id")
                if unique_id_data and unique_id_data.get("number"):
                    trainer_numeric_id = f"{unique_id_data.get('number'):03d}"
                    break
            elif id_prop.get("type") == "number":
                num = id_prop.get("number")
                if num:
                    trainer_numeric_id = f"{int(num):03d}"
                    break

    for workout in sample_workouts:
        workout_date = (datetime.now() - timedelta(days=workout["days_ago"])).strftime("%Y-%m-%d")
        workout_date_formatted = workout_date.replace("-", "")

        # Track session number for this patient on this date
        session_key = f"{patient['id']}-{workout_date}"
        session_counter[session_key] = session_counter.get(session_key, 0) + 1
        session_number = session_counter[session_key]

        # Generate proper Log ID: WO-[PatientID]-[TrainerID]-[Date]-[SessionNumber]
        log_id = f"WO-{patient_id}-T{trainer_numeric_id}-{workout_date_formatted}-{session_number:03d}"

        workout_props = {
            "Log ID": {
                "title": [{"text": {"content": log_id}}]
            },
            "Patient": {"relation": [{"id": patient['id']}]},
            "Date": {"date": {"start": workout_date}},
            "Duration (min)": {"number": workout["duration"]},
            "Exercises & Sets": {
                "rich_text": [{"text": {"content": workout["exercises"]}}]
            },
            "Focus Areas": {"multi_select": [{"name": area} for area in workout["focus_areas"]]},
            "What I Noticed": {
                "rich_text": [{"text": {"content": workout["noticed"]}}]
            },
            "What's Improving": {
                "rich_text": [{"text": {"content": workout["improving"]}}]
            },
            "Concerns/Issues": {
                "rich_text": [{"text": {"content": workout["concerns"]}}]
            },
            "Overall Session Rating": {"select": {"name": workout["rating"]}}
        }

        if trainer_id:
            workout_props["Trainer"] = {"relation": [{"id": trainer_id}]}

        try:
            notion.pages.create(
                parent={"database_id": DB_WORKOUTS},
                properties=workout_props
            )
            created_count += 1
            print(f"   ✅ Created workout from {workout['days_ago']} days ago")
        except Exception as e:
            print(f"   ❌ Error: {e}")

print(f"\n[4/4] Summary:")
print(f"✅ Created {created_count} workout logs total")
print(f"✅ Data ready for testing weekly reports!")

print("\n" + "="*60)
print("NEXT STEP: Run python test_notion.py")
print("="*60)
