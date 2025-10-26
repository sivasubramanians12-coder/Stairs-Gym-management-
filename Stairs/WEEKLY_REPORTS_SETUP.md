# Weekly Reports System - Setup Guide

**Stairs Gym - Automated Weekly Patient Reports**

This guide will help you set up the automated weekly reporting system that:
- ✅ Fetches all workout logs for each patient
- ✅ Aggregates trainer comments and observations
- ✅ Generates AI-powered summaries using Claude
- ✅ Saves reports to Notion Weekly Logs database
- ✅ Sends reports via WhatsApp and Email (optional)

---

## Prerequisites

Before you begin, make sure you have:

1. ✅ **Notion databases set up** (from RELATIONAL_DATABASE_GUIDE.md)
   - PATIENTS database
   - TRAINERS database
   - WORKOUT LOGS database
   - WEEKLY LOGS database

2. ✅ **Notion Integration created** with access to all databases

3. ✅ **Groq API key** (from Groq - FREE tier available!)

4. ✅ **Python 3.11+** installed

5. ⚠️ **Optional:** Twilio account (for WhatsApp)
6. ⚠️ **Optional:** Gmail account (for Email)

---

## Part 1: Environment Setup (10 minutes)

### Step 1.1: Install Python Dependencies

```bash
# Navigate to project folder
cd "C:\Users\siva.s\AI Experiments\Stairs"

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 1.2: Create Environment Configuration

1. Copy the `.env.example` file to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` file and fill in your credentials:

```env
# REQUIRED: Notion API
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxx

# REQUIRED: Database IDs (already filled from RELATIONAL_DATABASE_GUIDE.md)
NOTION_DATABASE_ID_PATIENTS=298d97e8-c876-81b0-a954-f1db89bda5d7
NOTION_DATABASE_ID_TRAINERS=298d97e8-c876-817d-8d02-db5c3a64ba6d
NOTION_DATABASE_ID_ASSESSMENTS=298d97e8-c876-814a-81f9-fd691a0c9270
NOTION_DATABASE_ID_WORKOUTS=298d97e8-c876-8179-be21-fea272d651a5
NOTION_DATABASE_ID_WEEKLY=298d97e8-c876-81a4-aef8-c4e8c80cf26f
NOTION_DATABASE_ID_MONTHLY=298d97e8-c876-811d-acfe-cf3b630fcd7e

# REQUIRED: Groq AI (FREE - using Llama 3.3 70B)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx

# OPTIONAL: Server Configuration
HOST=0.0.0.0
PORT=8000

# OPTIONAL: For WhatsApp (via Twilio)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# OPTIONAL: For Email (via Gmail)
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

### How to Get API Keys:

**Notion API Key:**
1. Go to https://www.notion.so/my-integrations
2. Find your "Gym System" integration
3. Copy the "Internal Integration Token"

**Groq API Key:**
1. Go to https://console.groq.com/
2. Sign up (free tier available - very generous!)
3. Go to "API Keys" in the left menu
4. Create a new API key
5. Copy the key (starts with `gsk_`)

**Twilio (Optional - for WhatsApp):**
1. Go to https://www.twilio.com/console
2. Sign up for free trial
3. Copy Account SID and Auth Token
4. For WhatsApp, use Twilio Sandbox: https://www.twilio.com/console/sms/whatsapp/sandbox

**Gmail App Password (Optional - for Email):**
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Go to Security → App passwords
4. Generate new app password
5. Copy the 16-character password

---

## Part 2: Testing the System (15 minutes)

### Step 2.1: Start the API Server

```bash
# Make sure you're in the project folder with virtual environment activated
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2.2: Test Basic Endpoints

Open a new terminal and test:

```bash
# Test health check
curl http://localhost:8000/

# Expected response:
# {"status":"ok","service":"Stairs Gym - Weekly Reports API","version":"1.0.0"}

# Get all active patients
curl http://localhost:8000/api/patients

# You should see your 10 patients listed
```

### Step 2.3: Generate Test Weekly Report

**Option A: Using curl**
```bash
# Replace PATIENT_ID with actual Notion page ID from your PATIENTS database
curl -X POST "http://localhost:8000/api/weekly-report/PATIENT_ID?days=7"
```

**Option B: Using a browser**
Open your browser and go to:
```
http://localhost:8000/docs
```

This opens the FastAPI interactive documentation where you can:
1. Click on `/api/weekly-report/{patient_id}`
2. Click "Try it out"
3. Enter a patient ID
4. Click "Execute"

### Step 2.4: Verify in Notion

After generating a report:
1. Open your Notion **WEEKLY LOGS** database
2. You should see a new entry with:
   - Week ID (e.g., `WEEKLY-JohnDoe-W43-2025`)
   - Patient relation
   - Weekly Summary (AI-generated)
   - Key Improvements
   - Concerns Noted
   - Recommendations
   - Metrics (sessions, minutes, etc.)

---

## Part 3: Generate Reports for All Patients

### Manual Trigger (One-Time)

```bash
# Generate weekly reports for all active patients
curl -X POST "http://localhost:8000/api/weekly-reports/all?days=7"
```

This will:
- Fetch all active patients
- Generate weekly report for each
- Save to Notion Weekly Logs
- Return summary of results

Expected output:
```json
{
  "status": "completed",
  "total_patients": 10,
  "successful": 8,
  "failed": 0,
  "no_workouts": 2,
  "results": [...]
}
```

---

## Part 4: Automated Scheduling (Optional)

### Option A: Use Built-in Python Scheduler

The `scheduler.py` script will automatically generate reports every week.

**Configuration:**

Edit `.env` to set schedule:
```env
SCHEDULE_DAY=sunday
SCHEDULE_TIME=20:00
```

**Run the scheduler:**
```bash
python scheduler.py
```

The scheduler will:
- ✅ Run continuously in background
- ✅ Generate reports every Sunday at 8:00 PM
- ✅ Log all activities to console

**Manual trigger (for testing):**
```bash
python scheduler.py --now
```

**Keep it running:**
```bash
# Option 1: Use nohup (Linux/Mac)
nohup python scheduler.py > scheduler.log 2>&1 &

# Option 2: Use Windows Task Scheduler (Windows)
# - Open Task Scheduler
# - Create Basic Task
# - Trigger: Weekly, Sunday 8:00 PM
# - Action: Start a program
# - Program: C:\path\to\venv\Scripts\python.exe
# - Arguments: scheduler.py
# - Start in: C:\Users\siva.s\AI Experiments\Stairs

# Option 3: Use systemd (Linux)
# Create a systemd service file
```

### Option B: Use Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday at 8:00 PM)
0 20 * * 0 cd /path/to/Stairs && /path/to/venv/bin/python scheduler.py --now

# Save and exit
```

### Option C: Use Windows Task Scheduler

1. Open **Task Scheduler**
2. Create Task → General tab:
   - Name: "Stairs Gym Weekly Reports"
   - Description: "Generate weekly patient reports"
3. Triggers tab → New:
   - Weekly
   - Day: Sunday
   - Time: 8:00 PM
4. Actions tab → New:
   - Action: Start a program
   - Program: `C:\Users\siva.s\AI Experiments\Stairs\venv\Scripts\python.exe`
   - Arguments: `scheduler.py --now`
   - Start in: `C:\Users\siva.s\AI Experiments\Stairs`
5. Save

---

## Part 5: Enable WhatsApp & Email Notifications (Optional)

### Step 5.1: Update main.py to Include Notifications

The notification system is already set up in `notifications.py`. To enable it, you need to call it from `main.py`.

Add this to the `generate_weekly_report` function in `main.py`:

```python
# After saving to Notion, add this:
from notifications import send_weekly_report

# Get patient contact info
patient_email = patient_props.get("Email", {}).get("email")
patient_phone = patient_props.get("Phone", {}).get("phone_number")

# Send notifications
if patient_email or patient_phone:
    notification_result = send_weekly_report(
        patient_name=patient_name,
        patient_email=patient_email,
        patient_phone=patient_phone,
        summary_data=summary_data,
        workout_count=len(workouts),
        total_minutes=total_minutes,
        week_start=week_start.strftime("%Y-%m-%d"),
        week_end=week_end.strftime("%Y-%m-%d"),
        workouts=workouts,
        send_email_flag=True,  # Set to False to disable email
        send_whatsapp_flag=True  # Set to False to disable WhatsApp
    )

    # Update Notion with delivery status
    notion.pages.update(
        page_id=weekly_log_id,
        properties={
            "Email Sent": {"checkbox": notification_result["email"]["sent"]},
            "WhatsApp Sent": {"checkbox": notification_result["whatsapp"]["sent"]},
            "Sent Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
        }
    )
```

### Step 5.2: Test Notifications

```bash
# Test email formatting
python notifications.py

# This will print a sample WhatsApp message to console
```

---

## Part 6: Troubleshooting

### Issue: "Patient not found"

**Solution:**
- Verify patient ID is correct
- Check patient exists in PATIENTS database
- Ensure patient Status is "Active"

### Issue: "No workout sessions found"

**Solution:**
- This is normal if patient hasn't worked out this week
- The report will still be generated with "no activity" message
- Check WORKOUT LOGS database has entries for this patient

### Issue: Groq API error

**Solution:**
- Verify `GROQ_API_KEY` is correct in `.env`
- Check API key is valid: https://console.groq.com/
- Groq has generous free tier limits
- Check internet connection

### Issue: Notion API error

**Solution:**
- Verify `NOTION_API_KEY` is correct
- Check integration has access to all databases
- Verify database IDs are correct

### Issue: Email not sending

**Solution:**
- Verify Gmail credentials in `.env`
- Make sure you're using App Password, not regular password
- Check 2FA is enabled on Google account
- Check Gmail hasn't blocked "less secure app" access

### Issue: WhatsApp not sending

**Solution:**
- Verify Twilio credentials
- Check phone number format: `+919876543210` (with country code)
- For testing, use Twilio Sandbox
- For production, request WhatsApp Business API approval

---

## Part 7: Understanding the Workflow

Here's what happens when you run weekly reports:

```
1. API receives request
   ↓
2. Fetch all active patients from Notion
   ↓
3. For each patient:
   a. Fetch workout logs from past 7 days
   b. Extract trainer comments, ratings, observations
   c. Send to Groq AI (Llama 3.3 70B) for summary generation
   d. Receive structured summary (improvements, concerns, recommendations)
   e. Save to WEEKLY LOGS database in Notion
   f. (Optional) Send WhatsApp message
   g. (Optional) Send HTML email
   ↓
4. Return summary of all results
```

---

## Part 8: API Endpoints Reference

### `GET /`
Health check

### `GET /api/patients`
Get all active patients

**Response:**
```json
{
  "patients": [
    {
      "id": "page_id",
      "name": "John Doe",
      "patient_id": 1,
      "email": "john@example.com",
      "phone": "+919876543210"
    }
  ],
  "count": 10
}
```

### `GET /api/patients/{patient_id}/workouts?days=7`
Get workout logs for a patient

**Parameters:**
- `patient_id` (path): Notion page ID
- `days` (query): Number of days to look back (default: 7)

### `POST /api/weekly-report/{patient_id}?days=7`
Generate weekly report for one patient

**Parameters:**
- `patient_id` (path): Notion page ID
- `days` (query): Number of days to include (default: 7)

**Response:**
```json
{
  "status": "success",
  "patient_name": "John Doe",
  "workout_count": 3,
  "week_start": "2025-10-20",
  "week_end": "2025-10-26",
  "weekly_log_id": "notion_page_id",
  "summary": {
    "summary": "...",
    "improvements": "...",
    "concerns": "...",
    "recommendations": "..."
  }
}
```

### `POST /api/weekly-reports/all?days=7`
Generate weekly reports for ALL active patients

**Response:**
```json
{
  "status": "completed",
  "total_patients": 10,
  "successful": 8,
  "failed": 0,
  "no_workouts": 2,
  "results": [...]
}
```

---

## Part 9: Costs

**Estimated monthly costs:**

- **Groq API:** FREE! 🎉
  - Free tier includes generous limits
  - Llama 3.3 70B model is completely free
  - Perfect for small to medium gyms

- **Twilio (WhatsApp):** $20-40
  - $0.005 per message
  - 40 patients × 4 reports = 160 messages = ~$0.80
  - Plus monthly fee: $20

- **Email (Gmail):** Free (up to 500/day)

- **Server (Railway/Heroku):** $5-20/month
  - Or run on local server: Free

**Total: ~$25-60/month** (or FREE if you skip WhatsApp and host locally!)

---

## Part 10: Next Steps

1. ✅ **Test with real data:**
   - Add real workout logs for patients
   - Generate reports and review quality
   - Adjust Claude prompts if needed

2. ✅ **Enable notifications:**
   - Set up Twilio for WhatsApp
   - Configure Gmail for email
   - Test delivery to one patient first

3. ✅ **Deploy to production:**
   - Use Railway, Heroku, or your own server
   - Set up automated scheduling
   - Monitor logs for errors

4. ✅ **Train your team:**
   - Show trainers how to log workouts
   - Demonstrate weekly reports
   - Collect feedback

---

## Support

For issues or questions:
- Check troubleshooting section above
- Review Notion API docs: https://developers.notion.com/
- Review Groq API docs: https://console.groq.com/docs/
- Email: support@stairsgym.com

---

**You're all set! 🚀**

Start by testing with a single patient, verify the report quality, then scale to all patients.
