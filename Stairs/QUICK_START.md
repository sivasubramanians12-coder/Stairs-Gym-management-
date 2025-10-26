# Quick Start - Weekly Reports System

**Get up and running in 15 minutes**

---

## 1. Install Dependencies (2 min)

```bash
cd "C:\Users\siva.s\AI Experiments\Stairs"

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install packages
pip install -r requirements.txt
```

---

## 2. Configure Environment (3 min)

Create a `.env` file:

```env
# Get from https://www.notion.so/my-integrations
NOTION_API_KEY=secret_your_key_here

# Already set (from your databases)
NOTION_DATABASE_ID_PATIENTS=298d97e8-c876-81b0-a954-f1db89bda5d7
NOTION_DATABASE_ID_WORKOUTS=298d97e8-c876-8179-be21-fea272d651a5
NOTION_DATABASE_ID_WEEKLY=298d97e8-c876-81a4-aef8-c4e8c80cf26f

# Get from https://console.groq.com/ (FREE - using Llama 3.3 70B)
GROQ_API_KEY=gsk_your_groq_key_here
```

---

## 3. Start the API Server (1 min)

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 4. Test It (5 min)

Open browser: http://localhost:8000/docs

### Test 1: Get Patients
- Click `GET /api/patients`
- Click "Try it out"
- Click "Execute"
- ✅ You should see your 10 patients

### Test 2: Generate One Report
- Click `POST /api/weekly-report/{patient_id}`
- Click "Try it out"
- Enter any patient ID from step above
- Click "Execute"
- ✅ Check your Notion WEEKLY LOGS database

### Test 3: Generate All Reports
- Click `POST /api/weekly-reports/all`
- Click "Try it out"
- Click "Execute"
- ✅ Wait ~30 seconds for all reports to generate

---

## 5. Check Results in Notion (2 min)

1. Open Notion → **WEEKLY LOGS** database
2. You should see new entries for each patient
3. Each entry has:
   - Week ID
   - Patient (linked)
   - Weekly Summary (AI-generated)
   - Key Improvements
   - Concerns Noted
   - Recommendations
   - Metrics (sessions, minutes, attendance)

---

## 6. Automate It (Optional - 5 min)

### Option A: Python Scheduler (Recommended)

```bash
# Run this to generate reports every Sunday at 8 PM
python scheduler.py
```

Keep it running in background or set up as Windows Task.

### Option B: Manual Cron Job

```bash
# Edit crontab (Linux/Mac)
crontab -e

# Add: Run every Sunday at 8 PM
0 20 * * 0 cd /path/to/Stairs && python scheduler.py --now
```

---

## 7. Enable Notifications (Optional - 10 min)

### Email Setup:

1. Get Gmail App Password:
   - Google Account → Security → 2FA → App passwords
   - Generate new password

2. Add to `.env`:
   ```env
   GMAIL_USER=your.email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ```

### WhatsApp Setup:

1. Sign up: https://www.twilio.com/try-twilio
2. Get credentials from console
3. Add to `.env`:
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxx
   TWILIO_AUTH_TOKEN=xxxxx
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   ```

4. Test with sandbox: https://www.twilio.com/console/sms/whatsapp/sandbox

---

## That's It! 🎉

You now have:
- ✅ Automated weekly report generation
- ✅ AI-powered summaries using Groq (Llama 3.3 70B) - FREE!
- ✅ All trainer comments aggregated
- ✅ Reports saved to Notion
- ✅ (Optional) WhatsApp & Email delivery

---

## Common Commands

```bash
# Start API server
python main.py

# Run scheduler (auto mode)
python scheduler.py

# Generate reports now (manual)
python scheduler.py --now

# Test notifications
python notifications.py
```

---

## Troubleshooting

**Can't connect to Notion:**
- Check `NOTION_API_KEY` in `.env`
- Verify integration has access to databases

**Groq API error:**
- Check `GROQ_API_KEY` in `.env`
- Verify your key is valid: https://console.groq.com/
- Groq has a generous free tier!

**No workouts found:**
- This is normal if patient had no sessions this week
- Add test workout logs to test with real data

**Port 8000 already in use:**
```bash
# Change port in .env
PORT=8001
```

---

## Next Steps

1. Add real workout logs to WORKOUT LOGS database
2. Generate reports and review AI summaries
3. Adjust Groq prompts in `main.py` if needed (see generate_weekly_summary_with_groq function)
4. Enable WhatsApp/Email delivery
5. Deploy to cloud (Railway/Heroku) for 24/7 operation

---

**Need help?** Check `WEEKLY_REPORTS_SETUP.md` for detailed guide.
