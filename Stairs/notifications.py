"""
Notification Module for Stairs Gym
Handles WhatsApp and Email delivery of weekly reports
"""

import os
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Optional: Twilio for WhatsApp
try:
    from twilio.rest import Client as TwilioClient
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("⚠️  Twilio not installed. WhatsApp functionality disabled.")
    print("   Install with: pip install twilio")


# ============================================================================
# WHATSAPP NOTIFICATIONS (via Twilio)
# ============================================================================

def send_whatsapp_message(
    to_phone: str,
    message: str,
    patient_name: Optional[str] = None
) -> dict:
    """
    Send WhatsApp message using Twilio

    Args:
        to_phone: Recipient phone number (format: +919876543210)
        message: Message content
        patient_name: Optional patient name for logging

    Returns:
        Dictionary with status and details
    """
    if not TWILIO_AVAILABLE:
        return {
            "status": "error",
            "message": "Twilio not installed"
        }

    # Check credentials
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

    if not account_sid or not auth_token:
        return {
            "status": "error",
            "message": "Twilio credentials not configured"
        }

    try:
        # Initialize Twilio client
        client = TwilioClient(account_sid, auth_token)

        # Format phone number
        if not to_phone.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_phone}"
        else:
            to_number = to_phone

        # Send message
        message_obj = client.messages.create(
            from_=from_number,
            to=to_number,
            body=message
        )

        return {
            "status": "success",
            "message_sid": message_obj.sid,
            "to": to_phone,
            "patient_name": patient_name
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "to": to_phone,
            "patient_name": patient_name
        }


# ============================================================================
# EMAIL NOTIFICATIONS (via Gmail SMTP)
# ============================================================================

def send_email(
    to_email: str,
    subject: str,
    body: str,
    patient_name: Optional[str] = None,
    html: bool = False
) -> dict:
    """
    Send email using Gmail SMTP

    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body content
        patient_name: Optional patient name for logging
        html: Whether to send as HTML (default: plain text)

    Returns:
        Dictionary with status and details
    """
    # Get Gmail credentials from environment
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_password:
        return {
            "status": "error",
            "message": "Gmail credentials not configured",
            "to": to_email
        }

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach body
        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)

        return {
            "status": "success",
            "to": to_email,
            "patient_name": patient_name
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "to": to_email,
            "patient_name": patient_name
        }


# ============================================================================
# WEEKLY REPORT FORMATTING
# ============================================================================

def format_weekly_report_message(
    patient_name: str,
    summary_data: dict,
    workout_count: int,
    total_minutes: int,
    week_start: str,
    week_end: str
) -> str:
    """
    Format weekly report summary as a WhatsApp/SMS message

    Args:
        patient_name: Name of the patient
        summary_data: Dictionary with summary, improvements, concerns, recommendations
        workout_count: Number of workouts completed
        total_minutes: Total training minutes
        week_start: Start date of the week
        week_end: End date of the week

    Returns:
        Formatted message string
    """
    message = f"""🏋️ STAIRS GYM - Weekly Progress Report

Hi {patient_name}! 👋

📅 Week: {week_start} to {week_end}

📊 YOUR STATS:
• Sessions Completed: {workout_count}
• Total Training Time: {total_minutes} minutes

{summary_data.get('summary', '')}

💪 IMPROVEMENTS NOTED:
{summary_data.get('improvements', 'Keep up the great work!')}

⚠️ AREAS TO FOCUS:
{summary_data.get('concerns', 'None - you\'re doing great!')}

🎯 NEXT WEEK RECOMMENDATIONS:
{summary_data.get('recommendations', 'Continue with your current program.')}

Keep pushing forward! 💪
- Your Stairs Gym Team
"""
    return message


def format_weekly_report_email(
    patient_name: str,
    summary_data: dict,
    workout_count: int,
    total_minutes: int,
    week_start: str,
    week_end: str,
    workouts: list
) -> str:
    """
    Format weekly report as HTML email

    Returns:
        HTML formatted email string
    """
    # Create workout details table
    workout_rows = ""
    for i, workout in enumerate(workouts, 1):
        workout_rows += f"""
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{i}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{workout.get('date', 'N/A')}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{workout.get('duration', 0)} min</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{', '.join(workout.get('focus_areas', [])) or 'General'}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{workout.get('rating', 'N/A')}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Weekly Progress Report</title>
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
            <h1 style="margin: 0;">🏋️ STAIRS GYM</h1>
            <p style="margin: 10px 0 0 0; font-size: 18px;">Weekly Progress Report</p>
        </div>

        <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
            <p style="font-size: 16px;">Hi <strong>{patient_name}</strong>! 👋</p>

            <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea;">
                <p style="margin: 0; color: #666;">📅 Week: <strong>{week_start}</strong> to <strong>{week_end}</strong></p>
            </div>

            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">📊 Your Stats</h2>
            <div style="display: flex; gap: 20px; margin: 20px 0;">
                <div style="flex: 1; background: white; padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 32px; font-weight: bold; color: #667eea;">{workout_count}</div>
                    <div style="color: #666;">Sessions</div>
                </div>
                <div style="flex: 1; background: white; padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 32px; font-weight: bold; color: #764ba2;">{total_minutes}</div>
                    <div style="color: #666;">Minutes</div>
                </div>
            </div>

            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">📝 Summary</h2>
            <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p>{summary_data.get('summary', '')}</p>
            </div>

            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">💪 Key Improvements</h2>
            <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p style="white-space: pre-line;">{summary_data.get('improvements', 'Keep up the great work!')}</p>
            </div>

            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">⚠️ Focus Areas</h2>
            <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p style="white-space: pre-line;">{summary_data.get('concerns', 'None - you\'re doing great!')}</p>
            </div>

            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">🎯 Next Week</h2>
            <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p style="white-space: pre-line;">{summary_data.get('recommendations', 'Continue with your current program.')}</p>
            </div>

            <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">📋 Workout Details</h2>
            <table style="width: 100%; background: white; border-radius: 8px; overflow: hidden; margin: 20px 0; border-collapse: collapse;">
                <thead>
                    <tr style="background: #667eea; color: white;">
                        <th style="padding: 12px; text-align: left;">#</th>
                        <th style="padding: 12px; text-align: left;">Date</th>
                        <th style="padding: 12px; text-align: left;">Duration</th>
                        <th style="padding: 12px; text-align: left;">Focus</th>
                        <th style="padding: 12px; text-align: left;">Rating</th>
                    </tr>
                </thead>
                <tbody>
                    {workout_rows}
                </tbody>
            </table>

            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 30px 0;">
                <p style="margin: 0; font-size: 18px; font-weight: bold;">Keep pushing forward! 💪</p>
                <p style="margin: 10px 0 0 0;">- Your Stairs Gym Team</p>
            </div>

            <p style="text-align: center; color: #999; font-size: 12px; margin-top: 30px;">
                This is an automated weekly report. If you have questions, please contact your trainer.
            </p>
        </div>
    </body>
    </html>
    """
    return html


# ============================================================================
# COMBINED DELIVERY FUNCTIONS
# ============================================================================

def send_weekly_report(
    patient_name: str,
    patient_email: Optional[str],
    patient_phone: Optional[str],
    summary_data: dict,
    workout_count: int,
    total_minutes: int,
    week_start: str,
    week_end: str,
    workouts: list,
    send_email_flag: bool = True,
    send_whatsapp_flag: bool = True
) -> dict:
    """
    Send weekly report via both email and WhatsApp

    Returns:
        Dictionary with delivery status
    """
    results = {
        "patient_name": patient_name,
        "email": {"sent": False, "status": "skipped"},
        "whatsapp": {"sent": False, "status": "skipped"}
    }

    # Send Email
    if send_email_flag and patient_email:
        email_html = format_weekly_report_email(
            patient_name, summary_data, workout_count,
            total_minutes, week_start, week_end, workouts
        )
        email_result = send_email(
            to_email=patient_email,
            subject=f"Your Weekly Progress Report - {week_start} to {week_end}",
            body=email_html,
            patient_name=patient_name,
            html=True
        )
        results["email"] = email_result
        results["email"]["sent"] = email_result.get("status") == "success"

    # Send WhatsApp
    if send_whatsapp_flag and patient_phone:
        whatsapp_message = format_weekly_report_message(
            patient_name, summary_data, workout_count,
            total_minutes, week_start, week_end
        )
        whatsapp_result = send_whatsapp_message(
            to_phone=patient_phone,
            message=whatsapp_message,
            patient_name=patient_name
        )
        results["whatsapp"] = whatsapp_result
        results["whatsapp"]["sent"] = whatsapp_result.get("status") == "success"

    return results


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("Testing Notification Module\n")

    # Test data
    test_summary = {
        "summary": "Great week! Completed 3 solid training sessions with consistent effort.",
        "improvements": "• Strength in bench press increasing\n• Better form on squats\n• Improved endurance",
        "concerns": "Slight lower back tightness - focus on stretching",
        "recommendations": "• Add 10 min warm-up\n• Continue current program\n• Focus on mobility work"
    }

    # Test WhatsApp message formatting
    print("=" * 60)
    print("WhatsApp Message Format:")
    print("=" * 60)
    msg = format_weekly_report_message(
        patient_name="Test Patient",
        summary_data=test_summary,
        workout_count=3,
        total_minutes=150,
        week_start="2025-10-20",
        week_end="2025-10-26"
    )
    print(msg)

    print("\n" + "=" * 60)
    print("Email HTML generated successfully!")
    print("=" * 60)
