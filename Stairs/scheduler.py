"""
Weekly Report Scheduler for Stairs Gym

This script runs continuously and generates weekly reports for all patients
at a scheduled time (default: Sunday 8:00 PM)
"""

import schedule
import time
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
SCHEDULE_DAY = os.getenv("SCHEDULE_DAY", "sunday")  # monday, tuesday, etc.
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "20:00")  # 24-hour format


def generate_weekly_reports():
    """
    Trigger weekly report generation for all patients
    """
    print(f"\n{'='*60}")
    print(f"Starting weekly report generation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        # Call the API endpoint to generate all weekly reports
        response = requests.post(
            f"{API_BASE_URL}/api/weekly-reports/all",
            params={"days": 7},
            timeout=300  # 5 minute timeout for all reports
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Report Generation Complete!")
            print(f"   - Total Patients: {data.get('total_patients', 0)}")
            print(f"   - Successful: {data.get('successful', 0)}")
            print(f"   - No Workouts: {data.get('no_workouts', 0)}")
            print(f"   - Failed: {data.get('failed', 0)}")

            # Show details
            if data.get('results'):
                print(f"\nDetailed Results:")
                for result in data['results']:
                    status_icon = "✅" if result['status'] == 'success' else "⚠️" if result['status'] == 'no_workouts' else "❌"
                    print(f"   {status_icon} {result['patient_name']}: {result['status']} ({result.get('workout_count', 0)} workouts)")

        else:
            print(f"❌ Error: API returned status code {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: Could not connect to API")
        print(f"   Error: {str(e)}")
        print(f"   Make sure the API server is running at {API_BASE_URL}")

    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")

    print(f"\n{'='*60}")
    print(f"Next report scheduled for: {SCHEDULE_DAY.capitalize()} at {SCHEDULE_TIME}")
    print(f"{'='*60}\n")


def manual_trigger():
    """
    Manually trigger report generation (for testing)
    """
    print("Manual trigger activated...")
    generate_weekly_reports()


def main():
    """
    Main scheduler loop
    """
    print(f"""
╔══════════════════════════════════════════════════════════╗
║         STAIRS GYM - Weekly Report Scheduler             ║
╠══════════════════════════════════════════════════════════╣
║  API Endpoint: {API_BASE_URL:<38} ║
║  Schedule: {SCHEDULE_DAY.capitalize()} at {SCHEDULE_TIME:<34} ║
╚══════════════════════════════════════════════════════════╝
""")

    # Schedule the job
    if SCHEDULE_DAY.lower() == "monday":
        schedule.every().monday.at(SCHEDULE_TIME).do(generate_weekly_reports)
    elif SCHEDULE_DAY.lower() == "tuesday":
        schedule.every().tuesday.at(SCHEDULE_TIME).do(generate_weekly_reports)
    elif SCHEDULE_DAY.lower() == "wednesday":
        schedule.every().wednesday.at(SCHEDULE_TIME).do(generate_weekly_reports)
    elif SCHEDULE_DAY.lower() == "thursday":
        schedule.every().thursday.at(SCHEDULE_TIME).do(generate_weekly_reports)
    elif SCHEDULE_DAY.lower() == "friday":
        schedule.every().friday.at(SCHEDULE_TIME).do(generate_weekly_reports)
    elif SCHEDULE_DAY.lower() == "saturday":
        schedule.every().saturday.at(SCHEDULE_TIME).do(generate_weekly_reports)
    elif SCHEDULE_DAY.lower() == "sunday":
        schedule.every().sunday.at(SCHEDULE_TIME).do(generate_weekly_reports)
    else:
        print(f"❌ Invalid schedule day: {SCHEDULE_DAY}")
        print("   Valid options: monday, tuesday, wednesday, thursday, friday, saturday, sunday")
        return

    print(f"✅ Scheduler started successfully!")
    print(f"⏰ Next report will run on {SCHEDULE_DAY.capitalize()} at {SCHEDULE_TIME}")
    print(f"\nPress Ctrl+C to stop the scheduler\n")

    # Check if API is accessible
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print(f"✅ API is accessible at {API_BASE_URL}\n")
        else:
            print(f"⚠️  Warning: API returned status {response.status_code}\n")
    except:
        print(f"⚠️  Warning: Could not connect to API at {API_BASE_URL}")
        print(f"   Make sure the API server is running\n")

    # Run scheduler loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n✋ Scheduler stopped by user")
        print("Goodbye! 👋\n")


if __name__ == "__main__":
    import sys

    # Check for manual trigger flag
    if len(sys.argv) > 1 and sys.argv[1] == "--now":
        manual_trigger()
    else:
        main()
