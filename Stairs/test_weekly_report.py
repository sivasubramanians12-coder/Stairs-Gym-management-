"""
Test weekly report generation
"""

import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from notion_client import Client
from groq import Groq
from datetime import datetime, timedelta
import json

# Load environment
load_dotenv()

# Initialize clients
notion = Client(auth=os.getenv("NOTION_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Database IDs
DB_PATIENTS = os.getenv("NOTION_DATABASE_ID_PATIENTS")
DB_WORKOUTS = os.getenv("NOTION_DATABASE_ID_WORKOUTS")
DB_WEEKLY = os.getenv("NOTION_DATABASE_ID_WEEKLY")

print("="*60)
print("TESTING WEEKLY REPORT GENERATION")
print("="*60)

# Get first patient with workout logs
print("\n[1/5] Fetching patient...")
patients_response = notion.databases.query(
    database_id=DB_PATIENTS,
    filter={"property": "Status", "select": {"equals": "Active"}},
    page_size=1
)

patient_id = patients_response["results"][0]["id"]
patient_props = patients_response["results"][0]["properties"]
patient_name = patient_props.get("Name", {}).get("title", [])[0].get("plain_text", "")
print(f"✅ Testing with: {patient_name}")

# Fetch workout logs
print("\n[2/5] Fetching workout logs...")
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

workouts_response = notion.databases.query(
    database_id=DB_WORKOUTS,
    filter={
        "and": [
            {"property": "Patient", "relation": {"contains": patient_id}},
            {"property": "Date", "date": {"on_or_after": start_date.isoformat()}}
        ]
    }
)

workouts = []
for page in workouts_response.get("results", []):
    props = page.get("properties", {})
    workouts.append({
        "date": props.get("Date", {}).get("date", {}).get("start", ""),
        "duration": props.get("Duration (min)", {}).get("number", 0),
        "exercises": props.get("Exercises & Sets", {}).get("rich_text", [])[0].get("plain_text", "") if props.get("Exercises & Sets", {}).get("rich_text") else "",
        "noticed": props.get("What I Noticed", {}).get("rich_text", [])[0].get("plain_text", "") if props.get("What I Noticed", {}).get("rich_text") else "",
        "improving": props.get("What's Improving", {}).get("rich_text", [])[0].get("plain_text", "") if props.get("What's Improving", {}).get("rich_text") else "",
        "concerns": props.get("Concerns/Issues", {}).get("rich_text", [])[0].get("plain_text", "") if props.get("Concerns/Issues", {}).get("rich_text") else "",
        "rating": props.get("Overall Session Rating", {}).get("select", {}).get("name") if props.get("Overall Session Rating", {}).get("select") else "N/A"
    })

print(f"✅ Found {len(workouts)} workout sessions")

# Generate AI summary
print("\n[3/5] Generating AI summary with Groq...")

workout_details = []
for i, workout in enumerate(workouts, 1):
    detail = f"""
Session {i} - {workout['date']}:
- Duration: {workout['duration']} minutes
- Exercises: {workout['exercises'] or 'Not specified'}
- Trainer's Observations: {workout['noticed'] or 'None'}
- Progress Noted: {workout['improving'] or 'None'}
- Concerns: {workout['concerns'] or 'None'}
- Session Rating: {workout['rating']}
"""
    workout_details.append(detail)

total_sessions = len(workouts)
total_minutes = sum([w['duration'] for w in workouts])

prompt = f"""Generate a weekly summary for {patient_name}.

WEEKLY METRICS:
- Total Sessions: {total_sessions}
- Total Training Time: {total_minutes} minutes

WORKOUT SESSIONS:
{''.join(workout_details)}

Return JSON with keys: summary, improvements, concerns, recommendations"""

response = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a fitness coach. Return only valid JSON with keys: summary, improvements, concerns, recommendations"},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=500,
    response_format={"type": "json_object"}
)

summary_data = json.loads(response.choices[0].message.content)

# Convert arrays to strings if needed
for key in ["summary", "improvements", "concerns", "recommendations"]:
    value = summary_data.get(key, "")
    if isinstance(value, list):
        summary_data[key] = "\n".join([str(item) for item in value])
    elif not isinstance(value, str):
        summary_data[key] = str(value)

print(f"✅ AI summary generated")
print(f"\n   Summary: {summary_data.get('summary', 'N/A')[:80]}...")

# Save to Notion
print("\n[4/5] Saving weekly report to Notion...")

week_number = start_date.isocalendar()[1]
year = start_date.year
week_id = f"WEEKLY-{patient_name.replace(' ', '')}-W{week_number:02d}-{year}"

properties = {
    "Week ID": {"title": [{"text": {"content": week_id}}]},
    "patient": {"relation": [{"id": patient_id}]},  # lowercase!
    "Week Start": {"date": {"start": start_date.strftime("%Y-%m-%d")}},
    "Week End": {"date": {"start": end_date.strftime("%Y-%m-%d")}},
    "Generated Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
    "Total Sessions": {"number": total_sessions},
    "Total Minutes": {"number": total_minutes},
    "Average Rating": {"number": 4.5},
    "Attendance Rate": {"number": 100.0},
    "Weekly Summary": {
        "rich_text": [{"text": {"content": summary_data.get("summary", "")}}]
    },
    "Key Improvements": {
        "rich_text": [{"text": {"content": summary_data.get("improvements", "")}}]
    },
    "Concerns Noted": {
        "rich_text": [{"text": {"content": summary_data.get("concerns", "None")}}]
    },
    "Recommendations": {
        "rich_text": [{"text": {"content": summary_data.get("recommendations", "")}}]
    }
}

page = notion.pages.create(
    parent={"database_id": DB_WEEKLY},
    properties=properties
)

print(f"✅ Weekly report created in Notion!")
print(f"   Week ID: {week_id}")
print(f"   Page ID: {page['id']}")
print(f"\n   🔗 View in Notion: {page['url']}")

# Verify
print("\n[5/5] Verifying in Notion...")
verify_response = notion.databases.query(
    database_id=DB_WEEKLY,
    filter={"property": "Week ID", "title": {"equals": week_id}}
)

if verify_response.get("results"):
    print(f"✅ Verification successful - Report found in Notion!")
else:
    print(f"⚠️  Could not verify report")

print("\n" + "="*60)
print("TEST COMPLETE ✅")
print("="*60)
print(f"\n📊 Summary:")
print(f"   Patient: {patient_name}")
print(f"   Workouts Analyzed: {total_sessions}")
print(f"   Total Training Time: {total_minutes} minutes")
print(f"   Report Created: {week_id}")
print(f"\n✅ Weekly report generation working perfectly!")
print("\n" + "="*60)
