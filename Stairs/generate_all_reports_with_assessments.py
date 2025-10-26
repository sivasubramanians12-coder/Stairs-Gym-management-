"""
Generate weekly and monthly reports for all patients with assessment integration
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
DB_ASSESSMENTS = os.getenv("NOTION_DATABASE_ID_ASSESSMENTS")


def get_text_from_rich_text(rich_text_array):
    """Extract plain text from Notion rich text array"""
    if not rich_text_array:
        return ""
    return "".join([item.get("plain_text", "") for item in rich_text_array])


def fetch_patient_workouts(patient_id: str, start_date: datetime, end_date: datetime):
    """Fetch workout logs for a patient in date range"""
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


def fetch_patient_assessments(patient_id: str, start_date: datetime, end_date: datetime):
    """Fetch assessment logs for a patient in date range"""
    response = notion.databases.query(
        database_id=DB_ASSESSMENTS,
        filter={
            "and": [
                {"property": "Patient", "relation": {"contains": patient_id}},
                {"property": "Assessment Date", "date": {"on_or_after": start_date.isoformat()}}
            ]
        },
        sorts=[{"property": "Assessment Date", "direction": "descending"}]
    )

    assessments = []
    for page in response.get("results", []):
        props = page.get("properties", {})
        assessments.append({
            "assessment_id": get_text_from_rich_text(props.get("Assessment ID", {}).get("title", [])),
            "date": props.get("Assessment Date", {}).get("date", {}).get("start", ""),
            "strength_score": props.get("Strength Score", {}).get("number"),
            "mobility_score": props.get("Mobility Score", {}).get("number"),
            "balance_score": props.get("Balance Score", {}).get("number"),
            "flexibility_score": props.get("Flexibility Score", {}).get("number"),
            "goals": get_text_from_rich_text(props.get("Goals Set", {}).get("rich_text", [])),
            "program": get_text_from_rich_text(props.get("Program Suggested", {}).get("rich_text", [])),
            "trainer_notes": get_text_from_rich_text(props.get("Trainer Notes", {}).get("rich_text", []))
        })

    return assessments


def update_patient_assessment_scores(patient_id: str, assessment: dict):
    """Update patient record with latest assessment scores"""
    try:
        update_props = {}

        if assessment.get("strength_score") is not None:
            update_props["Current Strength Score"] = {"number": assessment["strength_score"]}

        if assessment.get("mobility_score") is not None:
            update_props["Current Mobility Score"] = {"number": assessment["mobility_score"]}

        if assessment.get("balance_score") is not None:
            update_props["Current Balance Score"] = {"number": assessment["balance_score"]}

        if assessment.get("flexibility_score") is not None:
            update_props["Current Flexibility Score"] = {"number": assessment["flexibility_score"]}

        # Calculate overall score
        scores = [
            assessment.get("strength_score"),
            assessment.get("mobility_score"),
            assessment.get("balance_score"),
            assessment.get("flexibility_score")
        ]
        valid_scores = [s for s in scores if s is not None]
        if valid_scores:
            overall_score = sum(valid_scores) / len(valid_scores)
            update_props["Current Overall Score"] = {"number": round(overall_score, 1)}

        # Update last assessment date
        if assessment.get("date"):
            update_props["Last Assessment Date"] = {"date": {"start": assessment["date"]}}

        if update_props:
            notion.pages.update(page_id=patient_id, properties=update_props)
            return True

        return False
    except Exception as e:
        return False


def generate_weekly_summary_with_groq(patient_name: str, workouts: list, assessments: list):
    """Generate AI summary using Groq, including assessment data"""

    if not workouts and not assessments:
        return {
            "summary": f"No workout sessions or assessments recorded for {patient_name} this week.",
            "improvements": "N/A",
            "concerns": "No activity this week",
            "recommendations": "Schedule training sessions and assessment for next week"
        }

    # Prepare workout details
    workout_summary = f"{len(workouts)} sessions, {sum([w['duration'] for w in workouts])} minutes total"

    # Prepare workout details
    workout_details = []
    for i, workout in enumerate(workouts, 1):
        detail = f"""
Session {i} - {workout['date']}:
- Duration: {workout['duration']} minutes
- Exercises: {workout['exercises'] or 'Not specified'}
- Trainer Observations: {workout['noticed'] or 'None'}
- Progress Noted: {workout['improving'] or 'None'}
- Concerns: {workout['concerns'] or 'None'}
- Rating: {workout['rating']}
"""
        workout_details.append(detail)

    # Prepare assessment details
    assessment_details = ""
    if assessments:
        assessment = assessments[0]
        assessment_details = f"""
ASSESSMENT CONDUCTED: {assessment['date']}
- Strength Score: {assessment['strength_score']}/100
- Mobility Score: {assessment['mobility_score']}/100
- Balance Score: {assessment['balance_score']}/100
- Flexibility Score: {assessment['flexibility_score']}/100
- Goals Set: {assessment['goals'] or 'Not specified'}
- Program Suggested: {assessment['program'] or 'Not specified'}
- Trainer Notes: {assessment['trainer_notes'] or 'None'}
"""

    prompt = f"""Generate weekly summary for {patient_name}.

CRITICAL INSTRUCTIONS:
- Use ONLY the data provided below - DO NOT add any information not present
- DO NOT speculate, assume, or add motivational filler text
- DO NOT make up progress if not explicitly stated in trainer notes
- If trainer noted improvements, state them exactly as written
- If assessment was conducted, reference the actual scores provided
- Reference specific exercises, weights, reps from workout data
- If information is missing, write "Not recorded" instead of inventing details

WEEKLY METRICS:
- Total Sessions: {len(workouts)}
- Total Training Time: {sum([w['duration'] for w in workouts])} minutes

WORKOUT SESSIONS:
{''.join(workout_details)}

{assessment_details}

Return JSON with keys: summary, improvements, concerns, recommendations.
Each value should be a STRING (not array). Be factual and concise - NO filler text."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a fitness data analyst. Summarize ONLY the factual data provided from workouts and assessments. DO NOT add motivational language, speculation, or filler text. Return only valid JSON with string values."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )

        summary_data = json.loads(response.choices[0].message.content)

        for key in ["summary", "improvements", "concerns", "recommendations"]:
            value = summary_data.get(key, "")
            if isinstance(value, list):
                summary_data[key] = "\n".join([str(item) for item in value])
            elif not isinstance(value, str):
                summary_data[key] = str(value)

        return summary_data

    except Exception as e:
        return {
            "summary": f"{patient_name}: {workout_summary}" + (f". Assessment on {assessments[0]['date']}" if assessments else ""),
            "improvements": "See workout logs",
            "concerns": "None",
            "recommendations": "Continue program"
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


def save_weekly_report(patient_id: str, patient_name: str, workouts: list, assessments: list,
                      start_date: datetime, end_date: datetime, summary_data: dict):
    """Save weekly report to Notion"""

    total_sessions = len(workouts)
    total_minutes = sum([w['duration'] for w in workouts if w['duration']])
    attendance_rate = min((total_sessions / 3) * 100, 100)

    week_number = start_date.isocalendar()[1]
    year = start_date.year

    # Get patient numeric ID for proper naming
    patient_numeric_id = get_patient_numeric_id(patient_id)
    week_id = f"WEEKLY-{patient_numeric_id}-W{week_number:02d}-{year}"

    # Check if exists
    existing = notion.databases.query(
        database_id=DB_WEEKLY,
        filter={"property": "Week ID", "title": {"equals": week_id}}
    )

    if existing.get("results"):
        return None, "exists"

    # Add assessment info
    assessment_text = ""
    if assessments:
        a = assessments[0]
        assessment_text = f"\n\nASSESSMENT ({a['date']}): Str:{a['strength_score']}, Mob:{a['mobility_score']}, Bal:{a['balance_score']}, Flex:{a['flexibility_score']}"

    properties = {
        "Week ID": {"title": [{"text": {"content": week_id}}]},
        "patient": {"relation": [{"id": patient_id}]},
        "Week Start": {"date": {"start": start_date.strftime("%Y-%m-%d")}},
        "Week End": {"date": {"start": end_date.strftime("%Y-%m-%d")}},
        "Generated Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        "Total Sessions": {"number": total_sessions},
        "Total Minutes": {"number": total_minutes},
        "Attendance Rate": {"number": round(attendance_rate, 1)},
        "Weekly Summary": {"rich_text": [{"text": {"content": (summary_data.get("summary", "") + assessment_text)[:2000]}}]},
        "Key Improvements": {"rich_text": [{"text": {"content": summary_data.get("improvements", "")[:2000]}}]},
        "Concerns Noted": {"rich_text": [{"text": {"content": summary_data.get("concerns", "None")[:2000]}}]},
        "Recommendations": {"rich_text": [{"text": {"content": summary_data.get("recommendations", "")[:2000]}}]}
    }

    try:
        page = notion.pages.create(parent={"database_id": DB_WEEKLY}, properties=properties)
        return page["id"], week_id
    except Exception as e:
        return None, f"error: {str(e)[:50]}"


# Main execution
if __name__ == "__main__":
    print("="*75)
    print(" " * 10 + "GENERATE REPORTS WITH ASSESSMENTS FOR ALL PATIENTS")
    print("="*75)

    # Get all active patients
    print("\n[1/2] Fetching active patients...")
    patients_response = notion.databases.query(
        database_id=DB_PATIENTS,
        filter={"property": "Status", "select": {"equals": "Active"}}
    )

    patients = patients_response.get("results", [])
    print(f"✅ Found {len(patients)} active patients")

    # Process each patient
    print("\n[2/2] Generating weekly reports...\n")

    reports_created = 0
    reports_skipped = 0
    patients_with_assessments = 0
    patients_updated = 0

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    for i, patient in enumerate(patients, 1):
        patient_id = patient["id"]
        patient_props = patient["properties"]
        patient_name = patient_props.get("Name", {}).get("title", [])[0].get("plain_text", "") if patient_props.get("Name", {}).get("title") else "Unknown"

        print(f"   [{i}/{len(patients)}] {patient_name}")

        # Fetch data
        workouts = fetch_patient_workouts(patient_id, start_date, end_date)
        assessments = fetch_patient_assessments(patient_id, start_date, end_date)

        if not workouts and not assessments:
            print(f"       ⚠️  No data - skipping")
            reports_skipped += 1
            continue

        print(f"       📊 {len(workouts)} workouts, {len(assessments)} assessment(s)")

        # Update patient scores if assessment exists
        if assessments:
            patients_with_assessments += 1
            if update_patient_assessment_scores(patient_id, assessments[0]):
                patients_updated += 1
                print(f"       ✅ Patient scores updated")

        # Generate summary
        summary_data = generate_weekly_summary_with_groq(patient_name, workouts, assessments)

        # Save report
        report_id, result = save_weekly_report(
            patient_id, patient_name, workouts, assessments,
            start_date, end_date, summary_data
        )

        if report_id:
            print(f"       ✅ Report: {result}")
            reports_created += 1
        elif result == "exists":
            print(f"       ℹ️  Report exists")
            reports_skipped += 1
        else:
            print(f"       ❌ Failed: {result}")

        print()

    # Summary
    print("="*75)
    print(" " * 30 + "SUMMARY")
    print("="*75)

    print(f"\n📊 Results:")
    print(f"   Total Patients: {len(patients)}")
    print(f"   Reports Created: {reports_created}")
    print(f"   Reports Skipped: {reports_skipped}")
    print(f"   Patients with Assessments: {patients_with_assessments}")
    print(f"   Patient Records Updated: {patients_updated}")

    if reports_created > 0 or patients_updated > 0:
        print(f"\n✅ Successfully generated {reports_created} report(s)")
        print(f"✅ Updated {patients_updated} patient record(s) with assessment data")
    else:
        print(f"\nℹ️  No new reports created")

    print("\n" + "="*75)
