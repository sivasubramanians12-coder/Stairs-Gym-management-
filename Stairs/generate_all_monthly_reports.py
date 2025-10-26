"""
Generate monthly reports for all active patients
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
DB_MONTHLY = os.getenv("NOTION_DATABASE_ID_MONTHLY")


def get_text_from_rich_text(rich_text_array):
    """Extract plain text from Notion rich text array"""
    if not rich_text_array:
        return ""
    return "".join([item.get("plain_text", "") for item in rich_text_array])


def fetch_patient_workouts_monthly(patient_id: str, days: int = 30):
    """Fetch all workout logs for a patient for the past month"""
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
        workouts.append({
            "date": props.get("Date", {}).get("date", {}).get("start", ""),
            "duration": props.get("Duration (min)", {}).get("number", 0),
            "exercises": get_text_from_rich_text(props.get("Exercises & Sets", {}).get("rich_text", [])),
            "noticed": get_text_from_rich_text(props.get("What I Noticed", {}).get("rich_text", [])),
            "improving": get_text_from_rich_text(props.get("What's Improving", {}).get("rich_text", [])),
            "concerns": get_text_from_rich_text(props.get("Concerns/Issues", {}).get("rich_text", [])),
            "rating": props.get("Overall Session Rating", {}).get("select", {}).get("name") if props.get("Overall Session Rating", {}).get("select") else "N/A"
        })

    return workouts


def fetch_weekly_summaries(patient_id: str, days: int = 30):
    """Fetch weekly summaries for the patient"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    response = notion.databases.query(
        database_id=DB_WEEKLY,
        filter={
            "and": [
                {"property": "patient", "relation": {"contains": patient_id}},
                {"property": "Week Start", "date": {"on_or_after": start_date.isoformat()}}
            ]
        },
        sorts=[{"property": "Week Start", "direction": "ascending"}]
    )

    summaries = []
    for page in response.get("results", []):
        props = page.get("properties", {})
        summaries.append({
            "week_id": get_text_from_rich_text(props.get("Week ID", {}).get("title", [])),
            "summary": get_text_from_rich_text(props.get("Weekly Summary", {}).get("rich_text", [])),
            "improvements": get_text_from_rich_text(props.get("Key Improvements", {}).get("rich_text", [])),
            "sessions": props.get("Total Sessions", {}).get("number", 0)
        })

    return summaries


def get_patient_measurements(patient_id: str):
    """Get current patient measurements"""
    patient = notion.pages.retrieve(page_id=patient_id)
    props = patient.get("properties", {})

    return {
        "weight": props.get("Weight (kg)", {}).get("number"),
        "height": props.get("Height (cm)", {}).get("number"),
        "chest": props.get("Chest (cm)", {}).get("number"),
        "waist": props.get("Waist (cm)", {}).get("number"),
        "hips": props.get("Hips (cm)", {}).get("number"),
        "thigh": props.get("Thigh (cm)", {}).get("number"),
        "arm": props.get("Arm (cm)", {}).get("number")
    }


def generate_monthly_summary_with_groq(patient_name: str, workouts: list, weekly_summaries: list, measurements: dict):
    """Generate comprehensive monthly summary using Groq AI"""

    if not workouts:
        return {
            "summary": f"No workout sessions recorded for {patient_name} this month.",
            "achievements": "N/A",
            "challenges": "No activity this month",
            "next_month_focus": "Schedule regular training sessions",
            "trainer_comments": "Need to establish consistent training schedule"
        }

    # Calculate metrics
    total_sessions = len(workouts)
    total_minutes = sum([w['duration'] for w in workouts if w['duration']])
    avg_duration = total_minutes / total_sessions if total_sessions > 0 else 0

    # Prepare weekly summaries
    weekly_summary_text = ""
    if weekly_summaries:
        weekly_summary_text = "\n".join([
            f"Week {i+1}: {s['sessions']} sessions - {s['summary'][:100]}..."
            for i, s in enumerate(weekly_summaries)
        ])
    else:
        weekly_summary_text = "No weekly summaries available"

    # Prepare measurements
    measurements_text = "\n".join([
        f"- {k.capitalize()}: {v} {('kg' if k == 'weight' else 'cm')}"
        for k, v in measurements.items() if v is not None
    ])

    # Create prompt for Groq
    prompt = f"""Generate a monthly fitness summary for {patient_name}.

CRITICAL INSTRUCTIONS:
- Use ONLY the data provided below - DO NOT add any information not present
- DO NOT speculate, assume, or add motivational filler text
- DO NOT invent achievements or challenges not stated in weekly summaries
- State facts from weekly summaries and measurements ONLY
- If weekly summaries mention specific improvements, reference them exactly
- If data is missing, write "Not recorded" instead of making assumptions
- DO NOT make predictions or add generic recommendations
- Reference specific exercises, metrics, or measurements from the data provided

MONTHLY METRICS:
- Total Sessions: {total_sessions}
- Total Training Time: {total_minutes} minutes
- Average Session: {avg_duration:.1f} minutes

WEEKLY SUMMARIES:
{weekly_summary_text}

CURRENT MEASUREMENTS:
{measurements_text if measurements_text else "No measurements recorded"}

Provide factual summary using ONLY the data above:
1. Monthly summary (2-3 factual sentences based on metrics and weekly summaries)
2. Achievements (ONLY if explicitly stated in weekly summaries)
3. Challenges (ONLY if explicitly noted in weekly summaries, otherwise "None noted")
4. Next month focus (based ONLY on concerns or recommendations from weekly data)
5. Trainer comments (factual assessment based on provided data only)

Return JSON with keys: summary, achievements, challenges, next_month_focus, trainer_comments
Each value should be a STRING (not array). Be factual and concise - NO filler text."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a fitness data analyst. Summarize ONLY the factual data provided from weekly reports and measurements. DO NOT add motivational language, speculation, assumptions, or filler text. Return only valid JSON with string values."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )

        summary_data = json.loads(response.choices[0].message.content)

        # Ensure all values are strings
        for key in ["summary", "achievements", "challenges", "next_month_focus", "trainer_comments"]:
            value = summary_data.get(key, "")
            if isinstance(value, list):
                summary_data[key] = "\n".join([str(item) for item in value])
            elif not isinstance(value, str):
                summary_data[key] = str(value)

        return summary_data

    except Exception as e:
        print(f"       ⚠️  Error generating summary: {e}")
        return {
            "summary": f"{patient_name} completed {total_sessions} sessions this month ({total_minutes} minutes total).",
            "achievements": "See individual workout logs for details.",
            "challenges": "Unable to generate AI summary",
            "next_month_focus": "Continue with current program",
            "trainer_comments": "Monthly assessment pending"
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


def save_monthly_report_to_notion(patient_id: str, patient_name: str, month_start: datetime,
                                  month_end: datetime, workouts: list, summary_data: dict,
                                  measurements: dict):
    """Save monthly report to Notion MONTHLY LOGS database"""

    # Calculate metrics
    total_sessions = len(workouts)
    total_minutes = sum([w['duration'] for w in workouts if w['duration']])

    # Calculate attendance rate (assuming 12 sessions per month as target)
    target_sessions = 12
    attendance_rate = min((total_sessions / target_sessions) * 100, 100)

    # Generate month ID
    month_name = month_start.strftime("%B").upper()[:3]  # JAN, FEB, MAR, etc.
    year = month_start.year

    # Get patient numeric ID for proper naming
    patient_numeric_id = get_patient_numeric_id(patient_id)
    month_id = f"MONTHLY-{patient_numeric_id}-{month_name}{year}"

    # Check if report already exists
    existing = notion.databases.query(
        database_id=DB_MONTHLY,
        filter={"property": "Month ID", "title": {"equals": month_id}}
    )

    if existing.get("results"):
        return None, "Report already exists"

    # Create properties
    properties = {
        "Month ID": {
            "title": [{"text": {"content": month_id}}]
        },
        "Patient": {
            "relation": [{"id": patient_id}]
        },
        "Month Start": {
            "date": {"start": month_start.strftime("%Y-%m-%d")}
        },
        "Month End": {
            "date": {"start": month_end.strftime("%Y-%m-%d")}
        },
        "Generated Date": {
            "date": {"start": datetime.now().strftime("%Y-%m-%d")}
        },
        "Total Sessions": {
            "number": total_sessions
        },
        "Total Minutes": {
            "number": total_minutes
        },
        "Attendance Rate": {
            "number": round(attendance_rate, 1)
        },
        "Monthly Summary": {
            "rich_text": [{"text": {"content": summary_data.get("summary", "")[:2000]}}]
        },
        "Major Achievements": {
            "rich_text": [{"text": {"content": summary_data.get("achievements", "")[:2000]}}]
        },
        "Challenges": {
            "rich_text": [{"text": {"content": summary_data.get("challenges", "None")[:2000]}}]
        },
        "Next Month Focus": {
            "rich_text": [{"text": {"content": summary_data.get("next_month_focus", "")[:2000]}}]
        },
        "Trainer Comments": {
            "rich_text": [{"text": {"content": summary_data.get("trainer_comments", "")[:2000]}}]
        }
    }

    # Add measurements if available
    if measurements.get("weight"):
        properties["End Weight"] = {"number": measurements["weight"]}

    try:
        page = notion.pages.create(
            parent={"database_id": DB_MONTHLY},
            properties=properties
        )
        return page["id"], month_id
    except Exception as e:
        return None, f"Error: {str(e)}"


# Main execution
if __name__ == "__main__":
    print("="*70)
    print(" " * 15 + "GENERATE MONTHLY REPORTS FOR ALL PATIENTS")
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

        # Fetch workouts (past 30 days)
        workouts = fetch_patient_workouts_monthly(patient_id, days=30)

        if not workouts or len(workouts) < 3:
            print(f"       ⚠️  Insufficient workout data (need at least 3 sessions) - skipping")
            reports_skipped += 1
            continue

        print(f"       📊 Found {len(workouts)} workouts ({sum([w['duration'] for w in workouts])} minutes)")

        # Fetch weekly summaries
        print(f"       📅 Fetching weekly summaries...")
        weekly_summaries = fetch_weekly_summaries(patient_id, days=30)
        print(f"       📄 Found {len(weekly_summaries)} weekly summaries")

        # Get measurements
        print(f"       📏 Fetching measurements...")
        measurements = get_patient_measurements(patient_id)

        # Generate AI summary
        print(f"       🤖 Generating monthly summary...")
        summary_data = generate_monthly_summary_with_groq(patient_name, workouts, weekly_summaries, measurements)

        # Save to Notion
        print(f"       💾 Saving to Notion...")
        month_end = datetime.now()
        month_start = month_end - timedelta(days=30)

        report_id, result = save_monthly_report_to_notion(
            patient_id, patient_name, month_start, month_end,
            workouts, summary_data, measurements
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
    verify_response = notion.databases.query(database_id=DB_MONTHLY)
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
        print(f"\n✅ Successfully generated {reports_created} new monthly report(s)!")
    else:
        print(f"\nℹ️  No new reports created (all patients already have reports or insufficient workout data)")

    print("\n" + "="*70)
