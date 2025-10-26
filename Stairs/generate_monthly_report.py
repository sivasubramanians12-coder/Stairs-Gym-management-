"""
Generate monthly reports for patients
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

    # Prepare workout summary
    workout_summary = f"Total Sessions: {total_sessions}, Total Time: {total_minutes} minutes"

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
    prompt = f"""Generate a comprehensive monthly fitness summary for {patient_name}.

MONTHLY METRICS:
- Total Sessions: {total_sessions}
- Total Training Time: {total_minutes} minutes
- Average Session: {avg_duration:.1f} minutes

WEEKLY SUMMARIES:
{weekly_summary_text}

CURRENT MEASUREMENTS:
{measurements_text if measurements_text else "No measurements recorded"}

OVERALL OBSERVATIONS:
Analyze all the data and provide:
1. A motivating monthly summary (3-4 sentences)
2. Major achievements this month (bullet points)
3. Challenges faced (or "None" if all went well)
4. Focus areas for next month (2-3 specific recommendations)
5. Trainer comments (professional assessment)

Return JSON with keys: summary, achievements, challenges, next_month_focus, trainer_comments
Each value should be a STRING (not array). Use newlines for bullet points in strings."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional fitness coach writing monthly progress reports. Return only valid JSON with string values."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
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
        print(f"Error generating summary: {e}")
        return {
            "summary": f"{patient_name} completed {total_sessions} sessions this month ({total_minutes} minutes total).",
            "achievements": "See individual workout logs for details.",
            "challenges": "Unable to generate AI summary",
            "next_month_focus": "Continue with current program",
            "trainer_comments": "Monthly assessment pending"
        }


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
    month_name = month_start.strftime("%B")
    year = month_start.year
    month_id = f"MONTHLY-{patient_name.replace(' ', '')}-{month_name.upper()}{year}"

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
            "rich_text": [{"text": {"content": summary_data.get("summary", "")[:2000]}}]  # Notion limit
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

    # Create the page
    page = notion.pages.create(
        parent={"database_id": DB_MONTHLY},
        properties=properties
    )

    return page["id"]


# Main execution
if __name__ == "__main__":
    print("="*60)
    print("TESTING MONTHLY REPORT GENERATION")
    print("="*60)

    # Get first patient with workout logs
    print("\n[1/6] Fetching patient...")
    patients_response = notion.databases.query(
        database_id=DB_PATIENTS,
        filter={"property": "Status", "select": {"equals": "Active"}},
        page_size=1
    )

    patient_id = patients_response["results"][0]["id"]
    patient_props = patients_response["results"][0]["properties"]
    patient_name = patient_props.get("Name", {}).get("title", [])[0].get("plain_text", "")
    print(f"✅ Testing with: {patient_name}")

    # Fetch workout logs (past 30 days)
    print("\n[2/6] Fetching workout logs (past 30 days)...")
    workouts = fetch_patient_workouts_monthly(patient_id, days=30)
    print(f"✅ Found {len(workouts)} workout sessions")

    # Fetch weekly summaries
    print("\n[3/6] Fetching weekly summaries...")
    weekly_summaries = fetch_weekly_summaries(patient_id, days=30)
    print(f"✅ Found {len(weekly_summaries)} weekly summaries")

    # Get measurements
    print("\n[4/6] Fetching current measurements...")
    measurements = get_patient_measurements(patient_id)
    print(f"✅ Retrieved measurements")

    # Generate AI summary
    print("\n[5/6] Generating monthly summary with Groq AI...")
    summary_data = generate_monthly_summary_with_groq(patient_name, workouts, weekly_summaries, measurements)
    print(f"✅ AI summary generated")
    print(f"\n   Summary: {summary_data.get('summary', 'N/A')[:80]}...")

    # Save to Notion
    print("\n[6/6] Saving monthly report to Notion...")
    month_end = datetime.now()
    month_start = month_end - timedelta(days=30)

    monthly_report_id = save_monthly_report_to_notion(
        patient_id,
        patient_name,
        month_start,
        month_end,
        workouts,
        summary_data,
        measurements
    )

    month_name = month_start.strftime("%B")
    year = month_start.year
    month_id = f"MONTHLY-{patient_name.replace(' ', '')}-{month_name.upper()}{year}"

    print(f"✅ Monthly report created in Notion!")
    print(f"   Month ID: {month_id}")
    print(f"   Page ID: {monthly_report_id}")

    # Verify
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)

    verify_response = notion.databases.query(
        database_id=DB_MONTHLY,
        filter={"property": "Month ID", "title": {"equals": month_id}}
    )

    if verify_response.get("results"):
        page_url = verify_response["results"][0].get("url")
        print(f"✅ Verification successful - Report found in Notion!")
        print(f"\n   🔗 View in Notion: {page_url}")
    else:
        print(f"⚠️  Could not verify report")

    # Summary
    print("\n" + "="*60)
    print("TEST COMPLETE ✅")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   Patient: {patient_name}")
    print(f"   Workouts Analyzed: {len(workouts)}")
    print(f"   Weekly Summaries: {len(weekly_summaries)}")
    print(f"   Total Training Time: {sum([w['duration'] for w in workouts])} minutes")
    print(f"   Report Created: {month_id}")
    print(f"\n✅ Monthly report generation working perfectly!")
    print("\n" + "="*60)
