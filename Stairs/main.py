from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from groq import Groq
from notion_client import Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Stairs Gym - Weekly Reports API")

# Initialize Notion and Groq clients
notion = Client(auth=os.getenv("NOTION_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database IDs from environment
DB_PATIENTS = os.getenv("NOTION_DATABASE_ID_PATIENTS")
DB_TRAINERS = os.getenv("NOTION_DATABASE_ID_TRAINERS")
DB_ASSESSMENTS = os.getenv("NOTION_DATABASE_ID_ASSESSMENTS")
DB_WORKOUTS = os.getenv("NOTION_DATABASE_ID_WORKOUTS")
DB_WEEKLY = os.getenv("NOTION_DATABASE_ID_WEEKLY")
DB_MONTHLY = os.getenv("NOTION_DATABASE_ID_MONTHLY")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_text_from_rich_text(rich_text_array):
    """Extract plain text from Notion rich text array"""
    if not rich_text_array:
        return ""
    return "".join([item.get("plain_text", "") for item in rich_text_array])


def get_title_from_title_array(title_array):
    """Extract plain text from Notion title array"""
    if not title_array:
        return ""
    return "".join([item.get("plain_text", "") for item in title_array])


def get_select_value(select_obj):
    """Extract value from Notion select property"""
    if not select_obj:
        return None
    return select_obj.get("name")


def get_relation_ids(relation_array):
    """Extract IDs from Notion relation array"""
    if not relation_array:
        return []
    return [item.get("id") for item in relation_array]


# ============================================================================
# CORE FUNCTIONS FOR WEEKLY REPORTS
# ============================================================================

def fetch_patient_workout_logs(patient_id: str, days: int = 7) -> List[Dict[str, Any]]:
    """
    Fetch all workout logs for a patient for the past N days

    Args:
        patient_id: Notion page ID of the patient
        days: Number of days to look back (default: 7)

    Returns:
        List of workout log records with trainer comments
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Query workout logs database
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
        },
        sorts=[{"property": "Date", "direction": "ascending"}]
    )

    workouts = []
    for page in response.get("results", []):
        props = page.get("properties", {})

        workout = {
            "id": page.get("id"),
            "date": props.get("Date", {}).get("date", {}).get("start", ""),
            "duration": props.get("Duration (min)", {}).get("number", 0),
            "exercises": get_text_from_rich_text(props.get("Exercises & Sets", {}).get("rich_text", [])),
            "focus_areas": [item.get("name") for item in props.get("Focus Areas", {}).get("multi_select", [])],
            "noticed": get_text_from_rich_text(props.get("What I Noticed", {}).get("rich_text", [])),
            "improving": get_text_from_rich_text(props.get("What's Improving", {}).get("rich_text", [])),
            "concerns": get_text_from_rich_text(props.get("Concerns/Issues", {}).get("rich_text", [])),
            "rating": get_select_value(props.get("Overall Session Rating", {}).get("select")),
            "patient_rating": get_select_value(props.get("Patient Self-Rating", {}).get("select")),
            "patient_comments": get_text_from_rich_text(props.get("Patient Comments", {}).get("rich_text", []))
        }
        workouts.append(workout)

    return workouts


def generate_weekly_summary_with_groq(patient_name: str, workouts: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Generate a comprehensive weekly summary using Groq AI (Llama models)

    Args:
        patient_name: Name of the patient
        workouts: List of workout log dictionaries

    Returns:
        Dictionary with summary, improvements, concerns, and recommendations
    """
    if not workouts:
        return {
            "summary": f"No workout sessions recorded for {patient_name} this week.",
            "improvements": "N/A",
            "concerns": "No activity this week",
            "recommendations": "Schedule sessions for next week"
        }

    # Prepare workout data for Groq
    workout_details = []
    for i, workout in enumerate(workouts, 1):
        detail = f"""
Session {i} - {workout['date']}:
- Duration: {workout['duration']} minutes
- Exercises: {workout['exercises'] or 'Not specified'}
- Focus Areas: {', '.join(workout['focus_areas']) or 'General'}
- Trainer's Observations: {workout['noticed'] or 'None'}
- Progress Noted: {workout['improving'] or 'None'}
- Concerns: {workout['concerns'] or 'None'}
- Session Rating: {workout['rating'] or 'Not rated'}
- Patient Self-Rating: {workout['patient_rating'] or 'Not provided'}
- Patient Comments: {workout['patient_comments'] or 'None'}
"""
        workout_details.append(detail)

    # Calculate metrics
    total_sessions = len(workouts)
    total_minutes = sum([w['duration'] for w in workouts if w['duration']])
    avg_duration = total_minutes / total_sessions if total_sessions > 0 else 0

    # Create prompt for Groq
    system_prompt = """You are a professional fitness coach writing a weekly progress summary for a gym patient.

Your task is to analyze the workout data and create a motivating, personalized weekly summary.

Structure your response as JSON with these exact keys:
{
  "summary": "Overall week summary (2-3 sentences, positive and encouraging)",
  "improvements": "Specific improvements noticed this week (bullet points)",
  "concerns": "Any concerns or areas needing attention (or 'None' if all good)",
  "recommendations": "Specific recommendations for next week (2-3 actionable items)"
}

Guidelines:
- Be specific and reference actual workout details
- Highlight trainer observations and progress
- Be encouraging but honest about concerns
- Make recommendations practical and achievable
- Use a warm, professional tone
- Keep it concise (total 150-200 words)

IMPORTANT: Return ONLY the JSON object, no other text."""

    user_message = f"""Generate a weekly summary for {patient_name}.

WEEKLY METRICS:
- Total Sessions: {total_sessions}
- Total Training Time: {total_minutes} minutes
- Average Session Duration: {avg_duration:.1f} minutes

WORKOUT SESSIONS:
{''.join(workout_details)}

Please provide the summary in JSON format as specified."""

    # Call Groq API
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # or "mixtral-8x7b-32768" or "llama3-70b-8192"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1500,
            response_format={"type": "json_object"}  # Force JSON output
        )

        response_text = response.choices[0].message.content

        # Try to extract JSON from response
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
            summary_data = json.loads(json_str)
        else:
            # Try to parse as direct JSON
            summary_data = json.loads(response_text)

        return summary_data

    except Exception as e:
        print(f"Error generating summary with Groq: {e}")
        # Fallback summary
        return {
            "summary": f"{patient_name} completed {total_sessions} sessions this week ({total_minutes} minutes total).",
            "improvements": "See individual workout logs for details.",
            "concerns": "Unable to generate AI summary",
            "recommendations": "Continue with current program"
        }


def save_weekly_report_to_notion(
    patient_id: str,
    patient_name: str,
    week_start: datetime,
    week_end: datetime,
    workouts: List[Dict[str, Any]],
    summary_data: Dict[str, str]
) -> str:
    """
    Save the weekly report to Notion Weekly Logs database

    Args:
        patient_id: Notion page ID of the patient
        patient_name: Name of the patient
        week_start: Start date of the week
        week_end: End date of the week
        workouts: List of workout dictionaries
        summary_data: AI-generated summary data

    Returns:
        Notion page ID of the created weekly log
    """
    # Calculate metrics
    total_sessions = len(workouts)
    total_minutes = sum([w['duration'] for w in workouts if w['duration']])

    # Calculate average rating (if available)
    ratings_map = {"Excellent": 5, "Good": 4, "Average": 3, "Below Average": 2, "Poor": 1}
    valid_ratings = [ratings_map.get(w['rating'], 0) for w in workouts if w.get('rating')]
    avg_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0

    # Calculate attendance rate (assuming 3 sessions per week as target)
    target_sessions = 3
    attendance_rate = min((total_sessions / target_sessions) * 100, 100)

    # Generate week ID
    week_number = week_start.isocalendar()[1]
    year = week_start.year
    week_id = f"WEEKLY-{patient_name.replace(' ', '')}-W{week_number:02d}-{year}"

    # Create properties for Notion
    properties = {
        "Week ID": {
            "title": [{"text": {"content": week_id}}]
        },
        "patient": {
            "relation": [{"id": patient_id}]
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
            "number": total_sessions
        },
        "Total Minutes": {
            "number": total_minutes
        },
        "Average Rating": {
            "number": round(avg_rating, 1)
        },
        "Attendance Rate": {
            "number": round(attendance_rate, 1)
        },
        "Weekly Summary": {
            "rich_text": [{"text": {"content": summary_data.get("summary", "")}}]
        },
        "Key Improvements": {
            "rich_text": [{"text": {"content": summary_data.get("improvements", "")}}]
        },
        "Concerns Noted": {
            "rich_text": [{"text": {"content": summary_data.get("concerns", "")}}]
        },
        "Recommendations": {
            "rich_text": [{"text": {"content": summary_data.get("recommendations", "")}}]
        }
    }

    # Create the page in Notion
    page = notion.pages.create(
        parent={"database_id": DB_WEEKLY},
        properties=properties
    )

    return page["id"]


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Stairs Gym - Weekly Reports API",
        "version": "1.0.0"
    }


@app.get("/api/patients")
async def get_all_patients():
    """Get all active patients"""
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
            patients.append({
                "id": page.get("id"),
                "name": get_title_from_title_array(props.get("Name", {}).get("title", [])),
                "patient_id": props.get("Patient ID", {}).get("unique_id", {}).get("number"),
                "email": props.get("Email", {}).get("email"),
                "phone": props.get("Phone", {}).get("phone_number")
            })

        return {"patients": patients, "count": len(patients)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients: {str(e)}")


@app.get("/api/patients/{patient_id}/workouts")
async def get_patient_workouts(patient_id: str, days: int = 7):
    """Get workout logs for a specific patient"""
    try:
        workouts = fetch_patient_workout_logs(patient_id, days)
        return {
            "patient_id": patient_id,
            "days": days,
            "workouts": workouts,
            "count": len(workouts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching workouts: {str(e)}")


@app.post("/api/weekly-report/{patient_id}")
async def generate_weekly_report(patient_id: str, days: int = 7):
    """
    Generate and save weekly report for a specific patient

    Args:
        patient_id: Notion page ID of the patient
        days: Number of days to include in the report (default: 7)
    """
    try:
        # Get patient details
        patient_page = notion.pages.retrieve(page_id=patient_id)
        patient_props = patient_page.get("properties", {})
        patient_name = get_title_from_title_array(patient_props.get("Name", {}).get("title", []))

        if not patient_name:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Fetch workout logs
        workouts = fetch_patient_workout_logs(patient_id, days)

        if not workouts:
            return {
                "status": "no_workouts",
                "message": f"No workout sessions found for {patient_name} in the past {days} days",
                "patient_name": patient_name
            }

        # Generate AI summary
        summary_data = generate_weekly_summary_with_groq(patient_name, workouts)

        # Calculate week range
        week_end = datetime.now()
        week_start = week_end - timedelta(days=days)

        # Save to Notion
        weekly_log_id = save_weekly_report_to_notion(
            patient_id,
            patient_name,
            week_start,
            week_end,
            workouts,
            summary_data
        )

        return {
            "status": "success",
            "message": f"Weekly report generated for {patient_name}",
            "patient_name": patient_name,
            "workout_count": len(workouts),
            "week_start": week_start.strftime("%Y-%m-%d"),
            "week_end": week_end.strftime("%Y-%m-%d"),
            "weekly_log_id": weekly_log_id,
            "summary": summary_data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating weekly report: {str(e)}")


@app.post("/api/weekly-reports/all")
async def generate_all_weekly_reports(days: int = 7):
    """
    Generate weekly reports for all active patients

    This endpoint processes all active patients and generates their weekly reports
    """
    try:
        # Get all active patients
        patients_response = await get_all_patients()
        patients = patients_response.get("patients", [])

        if not patients:
            return {
                "status": "no_patients",
                "message": "No active patients found"
            }

        results = []
        for patient in patients:
            try:
                report = await generate_weekly_report(patient["id"], days)
                results.append({
                    "patient_id": patient["id"],
                    "patient_name": patient["name"],
                    "status": report.get("status"),
                    "workout_count": report.get("workout_count", 0)
                })
            except Exception as e:
                results.append({
                    "patient_id": patient["id"],
                    "patient_name": patient["name"],
                    "status": "error",
                    "error": str(e)
                })

        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "error"]
        no_workouts = [r for r in results if r["status"] == "no_workouts"]

        return {
            "status": "completed",
            "total_patients": len(patients),
            "successful": len(successful),
            "failed": len(failed),
            "no_workouts": len(no_workouts),
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating reports: {str(e)}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
