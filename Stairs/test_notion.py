"""
Simple test script to verify Notion integration and report generation
Run this before starting the full API server
"""

import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import os
from dotenv import load_dotenv
from notion_client import Client
from groq import Groq
from datetime import datetime, timedelta
import json

# Load environment
load_dotenv()

# Initialize clients
print("Initializing clients...")
try:
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    print("✅ Clients initialized successfully\n")
except Exception as e:
    print(f"❌ Error initializing clients: {e}")
    exit(1)

# Database IDs
DB_PATIENTS = os.getenv("NOTION_DATABASE_ID_PATIENTS")
DB_WORKOUTS = os.getenv("NOTION_DATABASE_ID_WORKOUTS")
DB_WEEKLY = os.getenv("NOTION_DATABASE_ID_WEEKLY")

print("="*60)
print("STAIRS GYM - NOTION INTEGRATION TEST")
print("="*60)

# Test 1: Fetch Patients
print("\n[TEST 1] Fetching active patients from Notion...")
try:
    response = notion.databases.query(
        database_id=DB_PATIENTS,
        filter={
            "property": "Status",
            "select": {"equals": "Active"}
        }
    )

    patients = []
    for page in response.get("results", []):
        props = page.get("properties", {})
        name_prop = props.get("Name", {}).get("title", [])
        name = name_prop[0].get("plain_text", "") if name_prop else "Unknown"

        patients.append({
            "id": page.get("id"),
            "name": name
        })

    print(f"✅ Found {len(patients)} active patients:")
    for i, patient in enumerate(patients[:5], 1):  # Show first 5
        print(f"   {i}. {patient['name']} (ID: {patient['id'][:8]}...)")

    if len(patients) > 5:
        print(f"   ... and {len(patients) - 5} more")

    if not patients:
        print("⚠️  No active patients found. Make sure you have patients with Status='Active'")
        exit(1)

except Exception as e:
    print(f"❌ Error fetching patients: {e}")
    exit(1)

# Test 2: Fetch Workout Logs for first patient
print(f"\n[TEST 2] Fetching workout logs for {patients[0]['name']}...")
try:
    patient_id = patients[0]['id']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    response = notion.databases.query(
        database_id=DB_WORKOUTS,
        filter={
            "and": [
                {
                    "property": "Patient",
                    "relation": {"contains": patient_id}
                },
                {
                    "property": "Date",
                    "date": {"on_or_after": start_date.isoformat()}
                }
            ]
        }
    )

    workout_count = len(response.get("results", []))
    print(f"✅ Found {workout_count} workout sessions in the past 7 days")

    if workout_count == 0:
        print("⚠️  No workout logs found for this patient")
        print("   You'll need to add some workout logs to test report generation")

        # Ask if they want to create a sample workout
        print("\n❓ Would you like to create a sample workout log? (yes/no)")
        create_sample = input().lower().strip()

        if create_sample == 'yes':
            print("\n[CREATING SAMPLE] Adding a test workout log...")
            try:
                # Get first trainer
                trainers_response = notion.databases.query(
                    database_id=os.getenv("NOTION_DATABASE_ID_TRAINERS"),
                    page_size=1
                )
                trainer_id = trainers_response["results"][0]["id"] if trainers_response["results"] else None

                # Create sample workout
                workout_props = {
                    "Log ID": {
                        "title": [{"text": {"content": f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"}}]
                    },
                    "Patient": {"relation": [{"id": patient_id}]},
                    "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
                    "Duration (min)": {"number": 60},
                    "Exercises & Sets": {
                        "rich_text": [{"text": {"content": "Bench Press 3x10 @ 80kg, Squats 3x12 @ 100kg, Shoulder Press 3x8 @ 40kg"}}]
                    },
                    "Focus Areas": {"multi_select": [{"name": "Strength"}, {"name": "Core"}]},
                    "What I Noticed": {
                        "rich_text": [{"text": {"content": "Good form on all exercises, energy levels high"}}]
                    },
                    "What's Improving": {
                        "rich_text": [{"text": {"content": "Strength increasing, better depth on squats"}}]
                    },
                    "Concerns/Issues": {
                        "rich_text": [{"text": {"content": "Slight lower back tightness, advised stretching"}}]
                    },
                    "Overall Session Rating": {"select": {"name": "Excellent"}}
                }

                if trainer_id:
                    workout_props["Trainer"] = {"relation": [{"id": trainer_id}]}

                workout_page = notion.pages.create(
                    parent={"database_id": DB_WORKOUTS},
                    properties=workout_props
                )

                print(f"✅ Sample workout created successfully!")
                workout_count = 1

            except Exception as e:
                print(f"❌ Error creating sample workout: {e}")

    # Show workout details
    if workout_count > 0:
        print("\n   Workout sessions:")
        for i, workout in enumerate(response.get("results", [])[:3], 1):
            props = workout.get("properties", {})
            date = props.get("Date", {}).get("date", {}).get("start", "N/A")
            duration = props.get("Duration (min)", {}).get("number", 0)
            rating_obj = props.get("Overall Session Rating", {}).get("select")
            rating = rating_obj.get("name") if rating_obj else "N/A"
            print(f"   {i}. {date} - {duration} min - Rating: {rating}")

except Exception as e:
    print(f"❌ Error fetching workout logs: {e}")
    exit(1)

# Test 3: Test Groq AI Summary Generation
if workout_count > 0:
    print(f"\n[TEST 3] Testing AI summary generation with Groq...")
    try:
        test_prompt = f"""Generate a weekly summary for a gym patient.

WEEKLY METRICS:
- Total Sessions: {workout_count}
- Total Training Time: {workout_count * 60} minutes

Structure your response as JSON with these keys:
{{
  "summary": "Overall week summary (2-3 sentences)",
  "improvements": "Specific improvements noticed",
  "concerns": "Any concerns or 'None'",
  "recommendations": "Recommendations for next week"
}}

Return ONLY the JSON object."""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a fitness coach. Return only valid JSON."},
                {"role": "user", "content": test_prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )

        summary_text = response.choices[0].message.content
        summary_data = json.loads(summary_text)

        print(f"✅ AI summary generated successfully!")
        print(f"\n   Summary: {summary_data.get('summary', 'N/A')[:100]}...")

    except Exception as e:
        print(f"❌ Error generating AI summary: {e}")
        print(f"   Check your GROQ_API_KEY in .env file")
        exit(1)

# Test 4: Create Weekly Report in Notion
print(f"\n[TEST 4] Creating weekly report in Notion...")
try:
    week_end = datetime.now()
    week_start = week_end - timedelta(days=7)
    week_number = week_start.isocalendar()[1]
    year = week_start.year

    patient_name = patients[0]['name'].replace(' ', '')
    week_id = f"WEEKLY-{patient_name}-W{week_number:02d}-{year}"

    properties = {
        "Week ID": {
            "title": [{"text": {"content": week_id}}]
        },
        "Patient": {
            "relation": [{"id": patients[0]['id']}]
        },
        "Week Start": {
            "date": {"start": week_start.strftime("%Y-%m-%d")}
        },
        "Week End": {
            "date": {"start": week_end.strftime("%Y-%m-%d")}
        },
        "Generated Date": {
            "date": {"start": datetime.now().strftime("%Y-%m-%d")}
        },
        "Total Sessions": {
            "number": workout_count
        },
        "Total Minutes": {
            "number": workout_count * 60
        },
        "Average Rating": {
            "number": 4.0
        },
        "Attendance Rate": {
            "number": 100.0
        },
        "Weekly Summary": {
            "rich_text": [{"text": {"content": summary_data.get("summary", "Test summary")}}]
        },
        "Key Improvements": {
            "rich_text": [{"text": {"content": summary_data.get("improvements", "Test improvements")}}]
        },
        "Concerns Noted": {
            "rich_text": [{"text": {"content": summary_data.get("concerns", "None")}}]
        },
        "Recommendations": {
            "rich_text": [{"text": {"content": summary_data.get("recommendations", "Test recommendations")}}]
        }
    }

    page = notion.pages.create(
        parent={"database_id": DB_WEEKLY},
        properties=properties
    )

    print(f"✅ Weekly report created successfully!")
    print(f"   Week ID: {week_id}")
    print(f"   Notion Page ID: {page['id']}")
    print(f"\n   🔗 View in Notion: {page['url']}")

except Exception as e:
    print(f"❌ Error creating weekly report: {e}")
    print(f"   Error details: {str(e)}")
    exit(1)

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print("✅ All tests passed successfully!")
print(f"✅ Notion connection: Working")
print(f"✅ Patient data: {len(patients)} patients found")
print(f"✅ Workout logs: {workout_count} workouts found")
print(f"✅ Groq AI: Summary generated")
print(f"✅ Weekly report: Created in Notion")
print("\n🚀 You're ready to run the full API server!")
print("   Next step: python main.py")
print("="*60)
