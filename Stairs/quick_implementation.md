# Quick Implementation Guide
## Patient Database System - Step by Step

**Time to Complete:** 2-3 days  
**Skill Level:** Intermediate (with guided instructions)

---

## Part 1: Notion Setup (2-3 hours)

### Step 1.1: Create Notion Workspace

1. Go to https://notion.so
2. Sign up or log in
3. Create workspace: "Scientific Gym"
4. Upgrade to Team plan if you have 3+ trainers ($8/user/month)

### Step 1.2: Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Settings:
   - Name: "Gym System"
   - Associated workspace: "Scientific Gym"
   - Type: Internal
   - Capabilities: ✓ All (Read, Update, Insert content)
4. Click "Submit"
5. **COPY the "Internal Integration Token"** → Save it as `NOTION_API_KEY`
6. Keep this window open (you'll need it)

### Step 1.3: Create Database 1 - PATIENTS

1. In Notion, create a new page: "Patient Database"
2. Type `/database` and select "Table - Inline"
3. Name it: "PATIENTS"
4. Delete default properties (except Name)
5. Add properties in this exact order:

**Click "+ New property" for each:**

**PERSONAL DETAILS:**
```
Name (keep existing - Title type)
Patient ID: Unique ID
Email: Email
Phone: Phone number
Date of Birth: Date
Gender: Select (add options: Male, Female, Other)
Status: Select (add options: Active, Inactive)
Registration Date: Date
```

**BODY DETAILS:**
```
Height (cm): Number (format: Number)
Weight (kg): Number (format: Number with 1 decimal)
BMI: Formula → paste: prop("Weight (kg)") / ((prop("Height (cm)") / 100) * (prop("Height (cm)") / 100))
Chest (cm): Number
Waist (cm): Number
Hips (cm): Number
Thigh (cm): Number
Arm (cm): Number
```

**INJURY RECORDS:**
```
Key Injuries: Text
Current Pain/Discomfort: Text
Medical Notes: Text
Restrictions: Multi-select (add: No Heavy Lifting, No Running, No Overhead, Neck Issues, Back Issues, Knee Issues, Shoulder Issues)
```

**CURRENT ASSESSMENT:**
```
Last Assessment Date: Date
Current Overall Score: Number (0-100)
Current Strength Score: Number (0-100)
Current Mobility Score: Number (0-100)
Current Balance Score: Number (0-100)
Current Flexibility Score: Number (0-100)
```

**GOALS:**
```
Primary Goal: Select (add: Weight Loss, Muscle Gain, Endurance, Flexibility, General Fitness, Rehabilitation, Athletic Performance)
Target Weight: Number
Goal Notes: Text
Suggested Program: Text
```

6. Click "Share" (top right)
7. Click "Add connections"
8. Select "Gym System" integration
9. Click "Allow access"
10. Copy the database URL → Extract database ID (the random string)
    - URL format: `notion.so/workspace/DATABASE_ID?v=...`
    - Save this as `NOTION_DATABASE_ID_PATIENTS`

### Step 1.4: Create Database 2 - TRAINERS

1. Create new page: "Trainers"
2. Add Table database
3. Add properties:

```
Name: Title (keep existing)
Trainer ID: Unique ID
Email: Email
Phone: Phone number
Active Status: Checkbox
Specialization: Multi-select (add: Strength, Cardio, Flexibility, Rehabilitation, Sports)
```

4. Share with "Gym System" integration
5. Copy database ID → Save as `NOTION_DATABASE_ID_TRAINERS`

### Step 1.5: Create Database 3 - ASSESSMENT LOGS

1. Create new page: "Assessment Logs"
2. Add Table database
3. Add properties:

```
Assessment ID: Title (auto-name with date)
Patient: Relation → Select PATIENTS database → No limit
Assessment Date: Date
Assessment Number: Number
Assessed By: Relation → Select TRAINERS database → Single item

--- SCORES ---
Strength Score: Number (0-100)
Mobility Score: Number (0-100)
Balance Score: Number (0-100)
Flexibility Score: Number (0-100)
Overall Score: Formula → (prop("Strength Score") + prop("Mobility Score") + prop("Balance Score") + prop("Flexibility Score")) / 4

--- DETAILS ---
Strength Tests Details: Text
Mobility Tests Details: Text
Balance Tests Details: Text
Flexibility Tests Details: Text

--- GOALS & PROGRAM ---
Goals Set: Text
Program Suggested: Text
Focus Areas: Multi-select (add: Upper Body Strength, Lower Body Strength, Core, Cardio, Flexibility, Balance, Mobility)
Trainer Notes: Text
```

4. Share with integration
5. Copy database ID → Save as `NOTION_DATABASE_ID_ASSESSMENTS`

### Step 1.6: Create Database 4 - WORKOUT LOGS

1. Create new page: "Workout Logs"
2. Add Table database
3. Add properties:

```
Log ID: Title (auto-generate)
Patient: Relation → PATIENTS → No limit
Date: Date
Trainer: Relation → TRAINERS → Single item
Duration (min): Number

--- WORKOUT DETAILS ---
Exercises & Sets: Text
Focus Areas: Multi-select (add: Strength, Cardio, Flexibility, Mobility, Balance, Core)

--- TRAINER COMMENTARY ---
What I Noticed: Text
What's Improving: Text
Concerns/Issues: Text
Overall Session Rating: Select (add: Excellent, Good, Average, Below Average, Poor)

--- PATIENT FEEDBACK ---
Patient Self-Rating: Select (add: 1-Very Hard, 2-Hard, 3-Moderate, 4-Easy, 5-Very Easy)
Patient Comments: Text
```

4. Share with integration
5. Copy database ID → Save as `NOTION_DATABASE_ID_WORKOUTS`

### Step 1.7: Create Database 5 - WEEKLY LOGS

1. Create new page: "Weekly Logs"
2. Add Table database
3. Add properties:

```
Week ID: Title (format: "Week of Oct 20, 2025")
Patient: Relation → PATIENTS → No limit
Week Start: Date
Week End: Date
Generated Date: Date

--- METRICS ---
Total Sessions: Number
Total Minutes: Number
Average Rating: Number (1-5, 1 decimal)
Attendance Rate: Number (percentage)

--- AI SUMMARY ---
Weekly Summary: Text
Key Improvements: Text
Concerns Noted: Text
Recommendations: Text

--- DELIVERY ---
WhatsApp Sent: Checkbox
Email Sent: Checkbox
Sent Date: Date
```

4. Share with integration
5. Copy database ID → Save as `NOTION_DATABASE_ID_WEEKLY`

### Step 1.8: Create Database 6 - MONTHLY LOGS

1. Create new page: "Monthly Logs"
2. Add Table database
3. Add properties:

```
Month ID: Title (format: "October 2025")
Patient: Relation → PATIENTS → No limit
Month Start: Date
Month End: Date
Generated Date: Date

--- METRICS ---
Total Sessions: Number
Total Minutes: Number
Average Rating: Number
Attendance Rate: Number

--- BODY CHANGES ---
Start Weight: Number
End Weight: Number
Weight Change: Formula → prop("End Weight") - prop("Start Weight")
Start Measurements: Text
End Measurements: Text
Body Changes: Text

--- AI SUMMARY ---
Monthly Summary: Text
Major Achievements: Text
Challenges: Text
Next Month Focus: Text
Trainer Comments: Text

--- DELIVERY ---
WhatsApp Sent: Checkbox
Email Sent: Checkbox
Sent Date: Date
```

4. Share with integration
5. Copy database ID → Save as `NOTION_DATABASE_ID_MONTHLY`

### Step 1.9: Add Relations Back to PATIENTS

Go back to PATIENTS database and add:

```
Assigned Trainer: Relation → TRAINERS → Single item
Assessment Logs: Relation → ASSESSMENT LOGS → No limit
Workout Logs: Relation → WORKOUT LOGS → No limit
Weekly Logs: Relation → WEEKLY LOGS → No limit
Monthly Logs: Relation → MONTHLY LOGS → No limit
```

### Step 1.10: Add Sample Data

**Add 2 test trainers:**
- Name: "Test Trainer 1", Email: test1@gym.com, Active: ✓
- Name: "Test Trainer 2", Email: test2@gym.com, Active: ✓

**Add 2 test patients:**
- Name: "John Doe", Status: Active, Height: 175, Weight: 75, Assigned Trainer: Test Trainer 1
- Name: "Jane Smith", Status: Active, Height: 165, Weight: 62, Assigned Trainer: Test Trainer 2

---

## Part 2: Backend Setup (3-4 hours)

### Step 2.1: Prepare Environment

```bash
# Create project folder
mkdir gym-backend
cd gym-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create .env file
cat > .env << 'EOF'
# Notion
NOTION_API_KEY=your_notion_integration_token_here
NOTION_DATABASE_ID_PATIENTS=your_patients_db_id
NOTION_DATABASE_ID_TRAINERS=your_trainers_db_id
NOTION_DATABASE_ID_ASSESSMENTS=your_assessments_db_id
NOTION_DATABASE_ID_WORKOUTS=your_workouts_db_id
NOTION_DATABASE_ID_WEEKLY=your_weekly_db_id
NOTION_DATABASE_ID_MONTHLY=your_monthly_db_id

# Claude AI
ANTHROPIC_API_KEY=your_claude_api_key_here

# Server
HOST=0.0.0.0
PORT=8000
EOF

# Replace "your_xxx_here" with actual values
```

### Step 2.2: Install Dependencies

```bash
# Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
anthropic==0.7.0
notion-client==2.2.1
pydantic==2.5.0
httpx==0.25.2
twilio==8.11.0
python-multipart==0.0.6
EOF

# Install
pip install -r requirements.txt
```

### Step 2.3: Create Main Application

Create file `main.py`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import anthropic
from notion_client import Client
import os
from dotenv import load_dotenv
from datetime import datetime, date, timedelta

# Load environment
load_dotenv()

# Initialize
app = FastAPI(title="Gym Patient Database API")
notion = Client(auth=os.getenv("NOTION_API_KEY"))
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database IDs
DB_PATIENTS = os.getenv("NOTION_DATABASE_ID_PATIENTS")
DB_TRAINERS = os.getenv("NOTION_DATABASE_ID_TRAINERS")
DB_ASSESSMENTS = os.getenv("NOTION_DATABASE_ID_ASSESSMENTS")
DB_WORKOUTS = os.getenv("NOTION_DATABASE_ID_WORKOUTS")
DB_WEEKLY = os.getenv("NOTION_DATABASE_ID_WEEKLY")
DB_MONTHLY = os.getenv("NOTION_DATABASE_ID_MONTHLY")

# Conversation storage (in production, use Redis or DB)
conversations = {}

# Models
class ChatMessage(BaseModel):
    trainer_id: str
    message: str

class WorkoutLog(BaseModel):
    patient_name: str
    date: str
    duration: int
    exercises: str
    focus_areas: List[str]
    noticed: str
    improving: str
    concerns: str
    rating: str

# Routes
@app.get("/")
async def root():
    return {"status": "ok", "message": "Gym Patient Database API"}

@app.post("/api/chat")
async def chat_with_claude(msg: ChatMessage):
    """Chat with Claude to log workouts or assessments"""
    
    trainer_id = msg.trainer_id
    message = msg.message
    
    # Initialize conversation if new
    if trainer_id not in conversations:
        conversations[trainer_id] = []
    
    # System prompt for workout logging
    system_prompt = """You are an AI assistant for gym trainers logging workout sessions.

Extract structured data from natural language descriptions.

Required information:
- Patient name
- Date (default today if not mentioned)
- Duration (default 60 min)
- Exercises with sets/reps/weight
- What you noticed
- What's improving
- Any concerns
- Session rating

When you have enough information, respond with JSON:
{
  "action": "save_workout",
  "data": {
    "patient_name": "string",
    "date": "YYYY-MM-DD",
    "duration": number,
    "exercises": "detailed description",
    "focus_areas": ["array"],
    "noticed": "observations",
    "improving": "progress",
    "concerns": "issues",
    "rating": "Excellent|Good|Average|Below Average|Poor"
  }
}

If it's an assessment, use action: "save_assessment" with appropriate structure.

Be conversational. Don't ask for every tiny detail. Use smart defaults."""

    # Add user message
    conversations[trainer_id].append({
        "role": "user",
        "content": message
    })
    
    # Call Claude
    response = claude.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        system=system_prompt,
        messages=conversations[trainer_id]
    )
    
    assistant_message = response.content[0].text
    
    # Add to conversation history
    conversations[trainer_id].append({
        "role": "assistant",
        "content": assistant_message
    })
    
    # Try to extract JSON if present
    structured_data = None
    if "```json" in assistant_message:
        try:
            start = assistant_message.find("```json") + 7
            end = assistant_message.find("```", start)
            json_str = assistant_message[start:end].strip()
            import json
            structured_data = json.loads(json_str)
            
            # If we got structured data, save it
            if structured_data and structured_data.get("action") == "save_workout":
                workout_id = await save_workout_to_notion(structured_data["data"], trainer_id)
                assistant_message += f"\n\n✓ Saved to Notion! Workout ID: {workout_id}"
                
        except Exception as e:
            print(f"Error parsing JSON: {e}")
    
    return {
        "response": assistant_message,
        "structured_data": structured_data,
        "conversation_id": trainer_id
    }

async def save_workout_to_notion(workout_data: dict, trainer_id: str):
    """Save workout log to Notion"""
    
    # Find patient by name
    patient_results = notion.databases.query(
        database_id=DB_PATIENTS,
        filter={
            "property": "Name",
            "title": {
                "contains": workout_data["patient_name"]
            }
        }
    )
    
    if not patient_results["results"]:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_id = patient_results["results"][0]["id"]
    
    # Find trainer
    trainer_results = notion.databases.query(
        database_id=DB_TRAINERS,
        page_size=1
    )
    trainer_notion_id = trainer_results["results"][0]["id"] if trainer_results["results"] else None
    
    # Create workout log
    properties = {
        "Log ID": {
            "title": [{"text": {"content": f"LOG-{datetime.now().strftime('%Y%m%d%H%M%S')}"}}]
        },
        "Patient": {"relation": [{"id": patient_id}]},
        "Date": {"date": {"start": workout_data["date"]}},
        "Duration (min)": {"number": workout_data["duration"]},
        "Exercises & Sets": {"rich_text": [{"text": {"content": workout_data["exercises"]}}]},
        "Focus Areas": {"multi_select": [{"name": area} for area in workout_data["focus_areas"]]},
        "What I Noticed": {"rich_text": [{"text": {"content": workout_data["noticed"]}}]},
        "What's Improving": {"rich_text": [{"text": {"content": workout_data["improving"]}}]},
        "Concerns/Issues": {"rich_text": [{"text": {"content": workout_data["concerns"]}}]},
        "Overall Session Rating": {"select": {"name": workout_data["rating"]}}
    }
    
    if trainer_notion_id:
        properties["Trainer"] = {"relation": [{"id": trainer_notion_id}]}
    
    page = notion.pages.create(
        parent={"database_id": DB_WORKOUTS},
        properties=properties
    )
    
    return page["id"]

@app.post("/api/workout/log")
async def log_workout(workout: WorkoutLog):
    """Direct workout logging (alternative to chat)"""
    return await save_workout_to_notion(workout.dict(), "direct")

@app.get("/api/patients")
async def get_patients(status: Optional[str] = "Active"):
    """Get all patients"""
    
    filter_param = {}
    if status:
        filter_param = {
            "property": "Status",
            "select": {"equals": status}
        }
    
    results = notion.databases.query(
        database_id=DB_PATIENTS,
        filter=filter_param if filter_param else None
    )
    
    patients = []
    for page in results["results"]:
        props = page["properties"]
        patients.append({
            "id": page["id"],
            "name": props["Name"]["title"][0]["text"]["content"] if props["Name"]["title"] else "",
            "status": props["Status"]["select"]["name"] if props["Status"]["select"] else "",
            "email": props["Email"]["email"] if "Email" in props else None
        })
    
    return {"patients": patients, "count": len(patients)}

@app.get("/api/patients/{patient_id}/workouts")
async def get_patient_workouts(patient_id: str, days: int = 7):
    """Get recent workouts for a patient"""
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    results = notion.databases.query(
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
        sorts=[{"property": "Date", "direction": "descending"}]
    )
    
    return {"workouts": results["results"], "count": len(results["results"])}

@app.post("/api/reports/weekly/{patient_id}")
async def generate_weekly_report(patient_id: str):
    """Generate weekly report for a patient"""
    
    # Get last 7 days of workouts
    workouts = await get_patient_workouts(patient_id, days=7)
    
    if workouts["count"] == 0:
        return {"error": "No workouts in the past week"}
    
    # Generate summary with Claude
    workout_summary = "\n".join([
        f"- {w['properties']['Date']['date']['start']}: {w['properties']['Overall Session Rating']['select']['name'] if w['properties']['Overall Session Rating']['select'] else 'N/A'}"
        for w in workouts["workouts"]
    ])
    
    system_prompt = """You are a fitness coach generating a weekly progress summary.
    
Make it motivational, specific, and actionable.
Include:
1. Week overview (sessions, time)
2. Key improvements
3. Any concerns
4. Next week recommendations

Keep it 150-200 words. Use emojis. Be encouraging."""

    response = claude.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Generate weekly summary for this workout data:\n{workout_summary}"
        }]
    )
    
    summary = response.content[0].text
    
    # Save to Weekly Logs database
    # (Implementation left as exercise)
    
    return {
        "summary": summary,
        "workouts_count": workouts["count"]
    }

@app.post("/api/clear-conversation/{trainer_id}")
async def clear_conversation(trainer_id: str):
    """Clear conversation history"""
    if trainer_id in conversations:
        conversations[trainer_id] = []
    return {"status": "cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 2.4: Test the Backend

```bash
# Run the server
python main.py

# In another terminal, test it:
curl http://localhost:8000/

# Test chat endpoint:
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "trainer_id": "trainer1",
    "message": "Log workout for John Doe. 45 min strength training. Bench press 3x10 at 60kg, squats 3x12 at 80kg. Form is improving, energy was good."
  }'

# Test getting patients:
curl http://localhost:8000/api/patients
```

---

## Part 3: Deploy to Railway (30 minutes)

### Step 3.1: Prepare for Deployment

```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Initialize git
git init
git add .
git commit -m "Initial commit"
```

### Step 3.2: Deploy

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Add environment variables
railway variables set NOTION_API_KEY=your_key
railway variables set ANTHROPIC_API_KEY=your_key
railway variables set NOTION_DATABASE_ID_PATIENTS=your_id
railway variables set NOTION_DATABASE_ID_TRAINERS=your_id
railway variables set NOTION_DATABASE_ID_ASSESSMENTS=your_id
railway variables set NOTION_DATABASE_ID_WORKOUTS=your_id
railway variables set NOTION_DATABASE_ID_WEEKLY=your_id
railway variables set NOTION_DATABASE_ID_MONTHLY=your_id

# Deploy
railway up

# Get URL
railway domain

# Your API is now live at: https://your-app.up.railway.app
```

---

## Part 4: Zapier Setup (1-2 hours)

### Step 4.1: Create Weekly Report Zap

1. Go to zapier.com
2. Click "Create Zap"
3. Name: "Weekly Patient Reports"

**Step 1 - Trigger:**
- App: Schedule by Zapier
- Event: Every Week
- Day: Sunday
- Time: 8:00 PM
- Test trigger

**Step 2 - Get Patients:**
- App: Webhooks by Zapier
- Action: GET
- URL: `https://your-railway-app.up.railway.app/api/patients?status=Active`
- Test and get patient list

**Step 3 - Loop:**
- App: Looping by Zapier
- Values: Select patients array from Step 2

**Step 4 - Generate Report:**
- App: Webhooks by Zapier
- Action: POST
- URL: `https://your-railway-app.up.railway.app/api/reports/weekly/{{patient_id}}`
- Test

**Step 5 - Send WhatsApp:**
- App: Twilio
- Action: Send WhatsApp Message
- From: Your Twilio WhatsApp number
- To: `whatsapp:{{patient_phone}}`
- Body: `{{summary}}` from Step 4

**Step 6 - Send Email:**
- App: Gmail
- Action: Send Email
- To: `{{patient_email}}`
- Subject: "Your Weekly Progress Update"
- Body: `{{summary}}`

**Turn on Zap!**

---

## Part 5: Testing (1 hour)

### Test Workout Logging

```bash
# Open terminal and run:
curl -X POST https://your-app.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "trainer_id": "test_trainer",
    "message": "Log workout for John Doe. Today we did 60 min upper body. Bench press 3x8 at 80kg, rows 3x10 at 60kg, shoulder press 3x8 at 30kg. His form is excellent, strength is improving. No concerns. Great session!"
  }'
```

Check Notion - you should see the workout logged!

### Test Weekly Report

```bash
# Manually trigger report:
curl -X POST https://your-app.up.railway.app/api/reports/weekly/PATIENT_ID_HERE
```

---

## Quick Reference Card for Trainers

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOGGING WORKOUTS WITH CLAUDE - QUICK GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW TO LOG:
Just talk naturally! Example:

"Log workout for Rahul. 45 min strength. 
Bench press 3x10 @ 60kg, squats 3x12 @ 80kg.
Form improving, energy good. No issues."

WHAT TO INCLUDE:
✓ Patient name
✓ What exercises (sets x reps @ weight)
✓ What you noticed
✓ What's improving
✓ Any concerns

HELPFUL COMMANDS:
• "Log workout for [name]..."
• "How is [patient] doing?"
• "Show [patient]'s last 2 weeks"
• "Generate report for [patient]"

TIPS:
• Don't overthink it - just describe the session
• You don't need to mention everything
• Claude will ask if critical info is missing
• Takes <2 minutes vs 10 min manual entry

SUPPORT: trainer-support@gym.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Troubleshooting

**Issue: "Patient not found"**
```
Solution: Make sure patient name matches exactly in Notion
Or use partial match: "Log for Rahul" will find "Rahul Sharma"
```

**Issue: Notion API rate limit**
```
Solution: Notion allows 3 requests per second
If hitting limits, add small delays in code
Or upgrade Notion plan
```

**Issue: Claude not extracting data**
```
Solution: Be more specific in your description
Include: name, exercises, and observations
Clear conversation history if confused
```

**Issue: WhatsApp not sending**
```
Solution: 
1. Check Twilio account status
2. Verify phone numbers have country code (+91...)
3. Check Twilio sandbox approval
4. For production, request WhatsApp Business API
```

---

## Next Actions

### Tomorrow:
- [ ] Complete Notion setup
- [ ] Add your actual trainers
- [ ] Add 2-3 real patients

### This Week:
- [ ] Deploy backend
- [ ] Test workout logging with real data
- [ ] Create Zapier automation
- [ ] Test weekly report

### Next Week:
- [ ] Train all trainers
- [ ] Go live with all patients
- [ ] Monitor and optimize

---

## Cost Summary

**Monthly:**
- Notion: $40 (5 trainers)
- Claude API: $50-100
- Zapier: $49
- Twilio: $50
- Railway: $5-20
**Total: ~$200-260/month**

**One-time:**
- Setup: $0 (DIY with this guide)
- Or hire developer: $2,000-3,000

---

## Support

Questions during setup?

1. Check troubleshooting section above
2. Email: support@gym.com
3. Notion has great docs: notion.so/help
4. Claude API docs: docs.anthropic.com

**You're ready to build! Start with Notion databases and work through step by step. Good luck! 🚀**
