"""
Generate weekly reports for all active patients
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


def fetch_patient_workouts(patient_id: str, days: int = 7):
    """Fetch workout logs for a patient"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    response = notion.databases.query(
        database_id=DB_WORKOUTS,
        filter={
            "and": [
                {"property": "Patient", "relation": {"contains": patient_id}},
                {"property": "Date", "date": {"on_or_after": start_date.isoformat()}}
            ]
        },
        sorts=[{"property": "Date", "direction": "ascending"}]
    )

    workouts = []
    for page in response.get("results", []):
        props = page.get("properties", {})

        # Safe extraction of rich text
        def get_text(prop_name):
            rich_text = props.get(prop_name, {}).get("rich_text", [])
            return rich_text[0].get("plain_text", "") if rich_text else ""

        workouts.append({
            "date": props.get("Date", {}).get("date", {}).get("start", ""),
            "duration": props.get("Duration (min)", {}).get("number", 0),
            "exercises": get_text("Exercises & Sets"),
            "noticed": get_text("What I Noticed"),
            "improving": get_text("What's Improving"),
            "concerns": get_text("Concerns/Issues"),
            "rating": props.get("Overall Session Rating", {}).get("select", {}).get("name") if props.get("Overall Session Rating", {}).get("select") else "N/A"
        })

    return workouts, start_date, end_date


def generate_weekly_summary(patient_name: str, workouts: list):
    """Generate AI summary using Groq"""
    if not workouts:
        return {
            "summary": f"No workout sessions recorded for {patient_name} this week.",
            "improvements": "N/A",
            "concerns": "No activity this week",
            "recommendations": "Schedule training sessions for next week"
        }

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

CRITICAL INSTRUCTIONS:
- Use ONLY the data provided below - DO NOT add any information not present in the data
- DO NOT speculate, assume, or add motivational filler text
- DO NOT make up progress if not explicitly stated in trainer notes
- If trainer noted improvements, state them exactly as written
- If trainer noted concerns, state them exactly as written
- Reference specific exercises, weights, reps, and times from the data
- If information is missing, write "Not recorded" instead of inventing details

WEEKLY METRICS:
- Total Sessions: {total_sessions}
- Total Training Time: {total_minutes} minutes

WORKOUT SESSIONS:
{''.join(workout_details)}

Return JSON with keys: summary, improvements, concerns, recommendations.
Each value should be a STRING (not array). Be factual and concise - NO filler text."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a fitness data analyst. Summarize ONLY the factual data provided. DO NOT add motivational language, speculation, or filler text. Return only valid JSON with string values."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
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

        return summary_data

    except Exception as e:
        print(f"   ⚠️  Error generating AI summary: {e}")
        return {
            "summary": f"{patient_name} completed {total_sessions} sessions this week ({total_minutes} minutes total).",
            "improvements": "See individual workout logs",
            "concerns": "None noted",
            "recommendations": "Continue with current program"
        }


def get_patient_numeric_id(patient_page_id):
    """Get the patient ID (numeric) from patient record"""
    try:
        patient = notion.pages.retrieve(page_id=patient_page_id)
        props = patient.get("properties", {})

        for field_name in ["ID", "Id", "Patient ID", "id"]:
            if field_name in props:
                id_prop = props[field_name]
                if id_prop.get("type") == "unique_id":
                    unique_id_data = id_prop.get("unique_id")
                    if unique_id_data and unique_id_data.get("number"):
                        return f"{unique_id_data.get('number'):03d}"
                elif id_prop.get("type") == "number":
                    patient_id = id_prop.get("number")
                    if patient_id:
                        return f"{int(patient_id):03d}"
        return patient_page_id[-3:]
    except:
        return "000"


def save_weekly_report(patient_id: str, patient_name: str, workouts: list,
                      start_date: datetime, end_date: datetime, summary_data: dict):
    """Save weekly report to Notion"""

    total_sessions = len(workouts)
    total_minutes = sum([w['duration'] for w in workouts if w['duration']])

    # Calculate attendance rate (assuming 3 sessions per week as target)
    target_sessions = 3
    attendance_rate = min((total_sessions / target_sessions) * 100, 100)

    week_number = start_date.isocalendar()[1]
    year = start_date.year

    # Get patient numeric ID for proper naming
    patient_numeric_id = get_patient_numeric_id(patient_id)
    week_id = f"WEEKLY-{patient_numeric_id}-W{week_number:02d}-{year}"

    # Check if report already exists
    existing = notion.databases.query(
        database_id=DB_WEEKLY,
        filter={"property": "Week ID", "title": {"equals": week_id}}
    )

    if existing.get("results"):
        return None, "Report already exists"

    properties = {
        "Week ID": {"title": [{"text": {"content": week_id}}]},
        "patient": {"relation": [{"id": patient_id}]},
        "Week Start": {"date": {"start": start_date.strftime("%Y-%m-%d")}},
        "Week End": {"date": {"start": end_date.strftime("%Y-%m-%d")}},
        "Generated Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        "Total Sessions": {"number": total_sessions},
        "Total Minutes": {"number": total_minutes},
        "Attendance Rate": {"number": round(attendance_rate, 1)},
        "Weekly Summary": {
            "rich_text": [{"text": {"content": summary_data.get("summary", "")[:2000]}}]
        },
        "Key Improvements": {
            "rich_text": [{"text": {"content": summary_data.get("improvements", "")[:2000]}}]
        },
        "Concerns Noted": {
            "rich_text": [{"text": {"content": summary_data.get("concerns", "None")[:2000]}}]
        },
        "Recommendations": {
            "rich_text": [{"text": {"content": summary_data.get("recommendations", "")[:2000]}}]
        }
    }

    try:
        page = notion.pages.create(
            parent={"database_id": DB_WEEKLY},
            properties=properties
        )
        return page["id"], week_id
    except Exception as e:
        return None, f"Error: {str(e)}"


# Main execution
if __name__ == "__main__":
    print("="*70)
    print(" " * 15 + "GENERATE WEEKLY REPORTS FOR ALL PATIENTS")
    print("="*70)

    # Get all active patients
    print("\n[1/3] Fetching active patients...")
    patients_response = notion.databases.query(
        database_id=DB_PATIENTS,
        filter={"property": "Status", "select": {"equals": "Active"}}
    )

    patients = patients_response.get("results", [])
    print(f"✅ Found {len(patients)} active patients")

    # Process each patient
    print("\n[2/3] Generating reports for each patient...\n")

    reports_created = 0
    reports_skipped = 0
    reports_failed = 0

    for i, patient in enumerate(patients, 1):
        patient_id = patient["id"]
        patient_props = patient["properties"]
        patient_name = patient_props.get("Name", {}).get("title", [])[0].get("plain_text", "") if patient_props.get("Name", {}).get("title") else "Unknown"

        print(f"   [{i}/{len(patients)}] Processing: {patient_name}")

        # Fetch workouts
        workouts, start_date, end_date = fetch_patient_workouts(patient_id, days=7)

        if not workouts:
            print(f"       ⚠️  No workout data in past 7 days - skipping")
            reports_skipped += 1
            continue

        print(f"       📊 Found {len(workouts)} workouts ({sum([w['duration'] for w in workouts])} minutes)")

        # Generate AI summary
        print(f"       🤖 Generating AI summary...")
        summary_data = generate_weekly_summary(patient_name, workouts)

        # Save to Notion
        print(f"       💾 Saving to Notion...")
        report_id, result = save_weekly_report(
            patient_id, patient_name, workouts,
            start_date, end_date, summary_data
        )

        if report_id:
            print(f"       ✅ Report created: {result}")
            reports_created += 1
        elif "already exists" in result:
            print(f"       ℹ️  {result}")
            reports_skipped += 1
        else:
            print(f"       ❌ Failed: {result}")
            reports_failed += 1

        print()

    # Summary
    print("\n[3/3] Verification...")
    verify_response = notion.databases.query(database_id=DB_WEEKLY)
    total_reports = len(verify_response.get("results", []))

    print("\n" + "="*70)
    print(" " * 25 + "SUMMARY")
    print("="*70)

    print(f"\n📊 Results:")
    print(f"   Total Patients: {len(patients)}")
    print(f"   Reports Created: {reports_created}")
    print(f"   Reports Skipped: {reports_skipped}")
    print(f"   Reports Failed: {reports_failed}")
    print(f"   Total Reports in Database: {total_reports}")

    if reports_created > 0:
        print(f"\n✅ Successfully generated {reports_created} new weekly report(s)!")
    else:
        print(f"\nℹ️  No new reports created (all patients already have reports or no workout data)")

    print("\n" + "="*70)
