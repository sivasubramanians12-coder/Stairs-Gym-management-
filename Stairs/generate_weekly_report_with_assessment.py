"""
Generate weekly reports with assessment information
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
        print(f"   ⚠️  Error updating patient scores: {e}")
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

    # Prepare assessment details
    assessment_details = ""
    if assessments:
        assessment = assessments[0]  # Most recent
        assessment_details = f"""
ASSESSMENT CONDUCTED THIS WEEK:
Date: {assessment['date']}
- Strength Score: {assessment['strength_score']}/100
- Mobility Score: {assessment['mobility_score']}/100
- Balance Score: {assessment['balance_score']}/100
- Flexibility Score: {assessment['flexibility_score']}/100
- Goals Set: {assessment['goals'] or 'Not specified'}
- Program Suggested: {assessment['program'] or 'Not specified'}
- Trainer Notes: {assessment['trainer_notes'] or 'None'}
"""

    total_sessions = len(workouts)
    total_minutes = sum([w['duration'] for w in workouts])

    prompt = f"""Generate a comprehensive weekly summary for {patient_name}.

WEEKLY METRICS:
- Total Sessions: {total_sessions}
- Total Training Time: {total_minutes} minutes

{assessment_details}

WORKOUT SESSIONS:
{''.join(workout_details) if workout_details else 'No workouts this week'}

Return JSON with keys: summary, improvements, concerns, recommendations.
{f"Important: Include assessment results in the summary and recommendations." if assessments else ""}
Each value should be a STRING (not array). Be motivating and specific."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a fitness coach. Return only valid JSON with string values. Include assessment data when available."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600,
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
            "summary": f"{patient_name} completed {total_sessions} sessions this week ({total_minutes} minutes total)." +
                      (f" Assessment conducted on {assessments[0]['date']}." if assessments else ""),
            "improvements": "See individual workout logs",
            "concerns": "None noted",
            "recommendations": "Continue with current program"
        }


def save_weekly_report(patient_id: str, patient_name: str, workouts: list, assessments: list,
                      start_date: datetime, end_date: datetime, summary_data: dict):
    """Save weekly report to Notion with assessment info"""

    total_sessions = len(workouts)
    total_minutes = sum([w['duration'] for w in workouts if w['duration']])

    # Calculate attendance rate (assuming 3 sessions per week as target)
    target_sessions = 3
    attendance_rate = min((total_sessions / target_sessions) * 100, 100)

    week_number = start_date.isocalendar()[1]
    year = start_date.year
    week_id = f"WEEKLY-{patient_name.replace(' ', '')}-W{week_number:02d}-{year}"

    # Check if report already exists
    existing = notion.databases.query(
        database_id=DB_WEEKLY,
        filter={"property": "Week ID", "title": {"equals": week_id}}
    )

    if existing.get("results"):
        return None, "Report already exists"

    # Add assessment info to summary if available
    assessment_text = ""
    if assessments:
        assessment = assessments[0]
        assessment_text = f"\n\nASSESSMENT ({assessment['date']}):\n"
        assessment_text += f"Strength: {assessment['strength_score']}, "
        assessment_text += f"Mobility: {assessment['mobility_score']}, "
        assessment_text += f"Balance: {assessment['balance_score']}, "
        assessment_text += f"Flexibility: {assessment['flexibility_score']}\n"
        if assessment.get('goals'):
            assessment_text += f"Goals: {assessment['goals']}"

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
            "rich_text": [{"text": {"content": (summary_data.get("summary", "") + assessment_text)[:2000]}}]
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
    print(" " * 10 + "WEEKLY REPORT GENERATION (WITH ASSESSMENTS)")
    print("="*70)

    # Get first patient
    print("\n[1/7] Fetching patient...")
    patients_response = notion.databases.query(
        database_id=DB_PATIENTS,
        filter={"property": "Status", "select": {"equals": "Active"}},
        page_size=1
    )

    patient_id = patients_response["results"][0]["id"]
    patient_props = patients_response["results"][0]["properties"]
    patient_name = patient_props.get("Name", {}).get("title", [])[0].get("plain_text", "")
    print(f"✅ Testing with: {patient_name}")

    # Set date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Fetch workouts
    print("\n[2/7] Fetching workout logs...")
    workouts = fetch_patient_workouts(patient_id, start_date, end_date)
    print(f"✅ Found {len(workouts)} workout sessions")

    # Fetch assessments
    print("\n[3/7] Fetching assessments...")
    assessments = fetch_patient_assessments(patient_id, start_date, end_date)
    print(f"✅ Found {len(assessments)} assessment(s)")

    if assessments:
        print(f"   📊 Latest assessment: {assessments[0]['date']}")
        print(f"   - Strength: {assessments[0]['strength_score']}")
        print(f"   - Mobility: {assessments[0]['mobility_score']}")
        print(f"   - Balance: {assessments[0]['balance_score']}")
        print(f"   - Flexibility: {assessments[0]['flexibility_score']}")

    # Update patient scores
    if assessments:
        print("\n[4/7] Updating patient record with assessment scores...")
        success = update_patient_assessment_scores(patient_id, assessments[0])
        if success:
            print(f"✅ Patient scores updated")
        else:
            print(f"⚠️  Could not update patient scores")
    else:
        print("\n[4/7] No assessments to update")

    # Generate AI summary
    print("\n[5/7] Generating AI summary with Groq...")
    summary_data = generate_weekly_summary_with_groq(patient_name, workouts, assessments)
    print(f"✅ AI summary generated")
    print(f"   Summary preview: {summary_data.get('summary', 'N/A')[:80]}...")

    # Save to Notion
    print("\n[6/7] Saving weekly report to Notion...")
    report_id, result = save_weekly_report(
        patient_id, patient_name, workouts, assessments,
        start_date, end_date, summary_data
    )

    if report_id:
        print(f"✅ Report created: {result}")
    else:
        print(f"⚠️  {result}")

    # Verification
    print("\n[7/7] Verification...")
    week_number = start_date.isocalendar()[1]
    year = start_date.year
    week_id = f"WEEKLY-{patient_name.replace(' ', '')}-W{week_number:02d}-{year}"

    verify_response = notion.databases.query(
        database_id=DB_WEEKLY,
        filter={"property": "Week ID", "title": {"equals": week_id}}
    )

    if verify_response.get("results"):
        page_url = verify_response["results"][0].get("url")
        print(f"✅ Report found in Notion!")
        print(f"\n   🔗 View: {page_url}")
    else:
        print(f"⚠️  Could not verify report")

    # Summary
    print("\n" + "="*70)
    print(" " * 25 + "SUMMARY")
    print("="*70)

    print(f"\n📊 Results:")
    print(f"   Patient: {patient_name}")
    print(f"   Workouts: {len(workouts)} sessions ({sum([w['duration'] for w in workouts])} min)")
    print(f"   Assessments: {len(assessments)}")
    if assessments:
        print(f"   Latest Assessment: {assessments[0]['date']}")
        print(f"   Patient Record: {'✅ Updated' if assessments else 'N/A'}")

    print(f"\n✅ Weekly report generation complete!")
    print("\n" + "="*70)
