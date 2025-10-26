"""
Verify all log naming conventions follow RELATIONAL_DATABASE_GUIDE.md standards
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
DB_WORKOUTS = os.getenv("NOTION_DATABASE_ID_WORKOUTS")
DB_WEEKLY = os.getenv("NOTION_DATABASE_ID_WEEKLY")
DB_MONTHLY = os.getenv("NOTION_DATABASE_ID_MONTHLY")
DB_ASSESSMENTS = os.getenv("NOTION_DATABASE_ID_ASSESSMENTS")


def get_text_from_rich_text(rich_text_array):
    """Extract plain text from Notion rich text array"""
    if not rich_text_array:
        return ""
    return "".join([item.get("plain_text", "") for item in rich_text_array])


print("="*85)
print(" " * 25 + "NAMING CONVENTION VERIFICATION")
print("="*85)

print("\nExpected Formats (per RELATIONAL_DATABASE_GUIDE.md):")
print("  - Assessment: ASSESS-[PatientID]-[TrainerID]-[Date]")
print("  - Workout:    WO-[PatientID]-[TrainerID]-[Date]-[SessionNumber]")
print("  - Weekly:     WEEKLY-[PatientID]-W[WeekNumber]-[Year]")
print("  - Monthly:    MONTHLY-[PatientID]-[MonthYear]")

# ========== CHECK ASSESSMENTS ==========
print("\n" + "="*85)
print("[1/4] ASSESSMENT LOGS")
print("="*85)

assessments_response = notion.databases.query(
    database_id=DB_ASSESSMENTS,
    page_size=10
)

assessments = assessments_response.get("results", [])
print(f"\nTotal Assessment Logs: {len(assessments)}")
print(f"\n{'Assessment ID':<40} | {'Format Check'}")
print("-" * 85)

assessment_correct = 0
for assessment in assessments[:10]:
    props = assessment.get("properties", {})
    assessment_id = get_text_from_rich_text(props.get("Assessment ID", {}).get("title", []))

    # Check format: ASSESS-XXX-TXXX-YYYYMMDD
    parts = assessment_id.split("-")
    is_correct = (
        len(parts) == 4 and
        parts[0] == "ASSESS" and
        len(parts[1]) == 3 and parts[1].isdigit() and
        len(parts[2]) == 4 and parts[2].startswith("T") and
        len(parts[3]) == 8 and parts[3].isdigit()
    )

    status = "✅" if is_correct else "❌"
    if is_correct:
        assessment_correct += 1

    print(f"{status} {assessment_id:<38} | {'Correct' if is_correct else 'INVALID FORMAT'}")

print(f"\n✅ Correct: {assessment_correct}/{len(assessments[:10])}")

# ========== CHECK WORKOUTS ==========
print("\n" + "="*85)
print("[2/4] WORKOUT LOGS")
print("="*85)

workouts_response = notion.databases.query(
    database_id=DB_WORKOUTS,
    page_size=10
)

workouts = workouts_response.get("results", [])
print(f"\nTotal Workout Logs: {len(workouts)}")
print(f"\n{'Workout Log ID':<40} | {'Format Check'}")
print("-" * 85)

workout_correct = 0
for workout in workouts[:10]:
    props = workout.get("properties", {})
    log_id = get_text_from_rich_text(props.get("Log ID", {}).get("title", []))

    # Check format: WO-XXX-TXXX-YYYYMMDD-XXX
    parts = log_id.split("-")
    is_correct = (
        len(parts) == 5 and
        parts[0] == "WO" and
        len(parts[1]) == 3 and parts[1].isdigit() and
        len(parts[2]) == 4 and parts[2].startswith("T") and
        len(parts[3]) == 8 and parts[3].isdigit() and
        len(parts[4]) == 3 and parts[4].isdigit()
    )

    status = "✅" if is_correct else "❌"
    if is_correct:
        workout_correct += 1

    print(f"{status} {log_id:<38} | {'Correct' if is_correct else 'INVALID FORMAT'}")

print(f"\n✅ Correct: {workout_correct}/{len(workouts[:10])}")

# ========== CHECK WEEKLY LOGS ==========
print("\n" + "="*85)
print("[3/4] WEEKLY LOGS")
print("="*85)

weekly_response = notion.databases.query(
    database_id=DB_WEEKLY,
    page_size=10
)

weekly_logs = weekly_response.get("results", [])
print(f"\nTotal Weekly Logs: {len(weekly_logs)}")
print(f"\n{'Week ID':<30} | {'Format Check'}")
print("-" * 85)

weekly_correct = 0
for log in weekly_logs[:10]:
    props = log.get("properties", {})
    week_id = get_text_from_rich_text(props.get("Week ID", {}).get("title", []))

    # Check format: WEEKLY-XXX-WXX-YYYY
    parts = week_id.split("-")
    is_correct = (
        len(parts) == 4 and
        parts[0] == "WEEKLY" and
        len(parts[1]) == 3 and parts[1].isdigit() and
        len(parts[2]) == 3 and parts[2].startswith("W") and parts[2][1:].isdigit() and
        len(parts[3]) == 4 and parts[3].isdigit()
    )

    status = "✅" if is_correct else "❌"
    if is_correct:
        weekly_correct += 1

    print(f"{status} {week_id:<28} | {'Correct' if is_correct else 'INVALID FORMAT'}")

print(f"\n✅ Correct: {weekly_correct}/{len(weekly_logs[:10])}")

# ========== CHECK MONTHLY LOGS ==========
print("\n" + "="*85)
print("[4/4] MONTHLY LOGS")
print("="*85)

monthly_response = notion.databases.query(
    database_id=DB_MONTHLY,
    page_size=10
)

monthly_logs = monthly_response.get("results", [])
print(f"\nTotal Monthly Logs: {len(monthly_logs)}")
print(f"\n{'Month ID':<30} | {'Format Check'}")
print("-" * 85)

monthly_correct = 0
for log in monthly_logs[:10]:
    props = log.get("properties", {})
    month_id = get_text_from_rich_text(props.get("Month ID", {}).get("title", []))

    # Check format: MONTHLY-XXX-MMMYYYY (e.g., MONTHLY-001-OCT2025)
    parts = month_id.split("-")
    is_correct = (
        len(parts) == 3 and
        parts[0] == "MONTHLY" and
        len(parts[1]) == 3 and parts[1].isdigit() and
        len(parts[2]) >= 7  # At least 3 chars for month + 4 for year
    )

    status = "✅" if is_correct else "❌"
    if is_correct:
        monthly_correct += 1

    print(f"{status} {month_id:<28} | {'Correct' if is_correct else 'INVALID FORMAT'}")

print(f"\n✅ Correct: {monthly_correct}/{len(monthly_logs[:10])}")

# ========== SUMMARY ==========
print("\n" + "="*85)
print(" " * 35 + "SUMMARY")
print("="*85)

total_logs = len(assessments) + len(workouts) + len(weekly_logs) + len(monthly_logs)
total_checked = min(len(assessments), 10) + min(len(workouts), 10) + min(len(weekly_logs), 10) + min(len(monthly_logs), 10)
total_correct = assessment_correct + workout_correct + weekly_correct + monthly_correct

print(f"\n📊 Overall Results:")
print(f"   Total Logs in System: {total_logs}")
print(f"   Logs Checked (sample): {total_checked}")
print(f"   Correct Format: {total_correct}/{total_checked} ({(total_correct/total_checked*100) if total_checked > 0 else 0:.1f}%)")

print(f"\n📋 By Category:")
print(f"   Assessment Logs: {assessment_correct}/{min(len(assessments), 10)} correct")
print(f"   Workout Logs:    {workout_correct}/{min(len(workouts), 10)} correct")
print(f"   Weekly Logs:     {weekly_correct}/{min(len(weekly_logs), 10)} correct")
print(f"   Monthly Logs:    {monthly_correct}/{min(len(monthly_logs), 10)} correct")

if total_correct == total_checked:
    print(f"\n✅ ALL NAMING CONVENTIONS ARE CORRECT!")
    print(f"   Your system follows the RELATIONAL_DATABASE_GUIDE.md standards.")
else:
    print(f"\n⚠️  Some logs have incorrect naming conventions")
    print(f"   Run fix scripts to correct naming.")

print("\n" + "="*85)
