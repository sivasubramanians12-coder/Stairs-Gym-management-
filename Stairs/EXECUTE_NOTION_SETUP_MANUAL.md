# Execute Notion Setup - Manual Checklist (Copy & Paste Ready)

**Status:** Ready to execute in Notion UI
**Time Required:** 25 minutes
**Difficulty:** Easy (copy-paste and click)

---

## ⚠️ Important Note

The Notion MCP API has limitations for relations and bulk data. Instead, I'm providing you with a **copy-paste ready checklist** that you can execute directly in your Notion workspace in 25 minutes.

---

## PART A: ORGANIZE COLUMNS (Manual - 5 minutes)

### Instructions
1. Go to your Notion workspace
2. Open **PATIENTS** database
3. Drag columns in this order (use the 6-dot handle next to each column name)

**SECTION 1 - CONTACT INFO:**
- Name
- Email
- Phone
- Date of Birth
- Gender

**SECTION 2 - REGISTRATION:**
- Status
- Registration Date
- Primary Goal
- Target Weight
- Goal Notes
- Suggested Program

**SECTION 3 - PHYSICAL:**
- Height (cm)
- Weight (kg)
- Chest (cm)
- Waist (cm)
- Hips (cm)
- Thigh (cm)
- Arm (cm)

**SECTION 4 - HEALTH:**
- Key Injuries
- Current Pain/Discomfort
- Medical Notes
- Restrictions

**SECTION 5 - ASSESSMENT:**
- Last Assessment Date
- Current Overall Score
- Current Strength Score
- Current Mobility Score
- Current Balance Score
- Current Flexibility Score

✅ **Done with Part A**

---

## PART B: ADD RELATIONS (Manual - 10 minutes)

### B1: ASSESSMENT LOGS - Add 2 Relations

1. Open **ASSESSMENT LOGS** database
2. Click **"+ Add a property"** (top right corner)
3. **Create: "Patient"**
   - Type: `Relation`
   - Related database: `PATIENTS`
   - Confirm
4. Click **"+ Add a property"** again
5. **Create: "Assessed By"**
   - Type: `Relation`
   - Related database: `TRAINERS`
   - Confirm

✅ **ASSESSMENT LOGS: 2 relations added**

---

### B2: WORKOUT LOGS - Add 2 Relations

1. Open **WORKOUT LOGS** database
2. Click **"+ Add a property"**
3. **Create: "Patient"**
   - Type: `Relation`
   - Related database: `PATIENTS`
   - Confirm
4. Click **"+ Add a property"** again
5. **Create: "Trainer"**
   - Type: `Relation`
   - Related database: `TRAINERS`
   - Confirm

✅ **WORKOUT LOGS: 2 relations added**

---

### B3: WEEKLY LOGS - Add 1 Relation

1. Open **WEEKLY LOGS** database
2. Click **"+ Add a property"**
3. **Create: "Patient"**
   - Type: `Relation`
   - Related database: `PATIENTS`
   - Confirm

✅ **WEEKLY LOGS: 1 relation added**

---

### B4: MONTHLY LOGS - Add 1 Relation

1. Open **MONTHLY LOGS** database
2. Click **"+ Add a property"**
3. **Create: "Patient"**
   - Type: `Relation`
   - Related database: `PATIENTS`
   - Confirm

✅ **MONTHLY LOGS: 1 relation added**

---

### B5: PATIENTS - Add 5 Relations

1. Open **PATIENTS** database
2. Click **"+ Add a property"**
3. **Create: "Assigned Trainer"**
   - Type: `Relation`
   - Related database: `TRAINERS`
   - Confirm
4. Click **"+ Add a property"**
5. **Create: "Assessment Logs"**
   - Type: `Relation`
   - Related database: `ASSESSMENT LOGS`
   - Confirm
6. Click **"+ Add a property"**
7. **Create: "Workout Logs"**
   - Type: `Relation`
   - Related database: `WORKOUT LOGS`
   - Confirm
8. Click **"+ Add a property"**
9. **Create: "Weekly Logs"**
   - Type: `Relation`
   - Related database: `WEEKLY LOGS`
   - Confirm
10. Click **"+ Add a property"**
11. **Create: "Monthly Logs"**
    - Type: `Relation`
    - Related database: `MONTHLY LOGS`
    - Confirm

✅ **PATIENTS: 5 relations added**

---

## PART C: ADD SAMPLE DATA (Manual - 10 minutes)

### C1: Add Trainers

**Open TRAINERS database**

#### Trainer 1 - Alex Johnson
```
Name: Alex Johnson
Email: alex@gym.com
Phone: +1-555-0001
Active Status: ✓ (checked)
Specialization: Strength, Cardio
```

Click "+" to add new row, fill in the above, press Enter.

#### Trainer 2 - Sarah Smith
```
Name: Sarah Smith
Email: sarah@gym.com
Phone: +1-555-0002
Active Status: ✓ (checked)
Specialization: Flexibility, Rehabilitation
```

Click "+" to add new row, fill in the above, press Enter.

✅ **2 Trainers added**

---

### C2: Add Patients

**Open PATIENTS database**

#### Patient 1 - John Doe
```
CONTACT:
Name: John Doe
Email: john@email.com
Phone: +1-555-1001
Date of Birth: 1990-05-15
Gender: Male

REGISTRATION:
Status: Active
Registration Date: 2025-10-26
Primary Goal: Muscle Gain
Target Weight: 85
Goal Notes: Increase muscle mass and strength
Suggested Program: 4x/week strength training

PHYSICAL:
Height (cm): 180
Weight (kg): 75
Chest (cm): 100
Waist (cm): 85
Hips (cm): 95
Thigh (cm): 55
Arm (cm): 35

HEALTH:
Key Injuries: None
Current Pain/Discomfort: None
Medical Notes: Healthy
Restrictions: (leave empty)

ASSESSMENT:
Last Assessment Date: 2025-10-26
Current Overall Score: 72
Current Strength Score: 75
Current Mobility Score: 70
Current Balance Score: 68
Current Flexibility Score: 72

RELATIONS:
Assigned Trainer: Alex Johnson
```

Click "+" to add new row, fill in all fields above.

#### Patient 2 - Jane Smith
```
CONTACT:
Name: Jane Smith
Email: jane@email.com
Phone: +1-555-1002
Date of Birth: 1992-08-22
Gender: Female

REGISTRATION:
Status: Active
Registration Date: 2025-10-24
Primary Goal: Weight Loss
Target Weight: 60
Goal Notes: Lose 5kg in 3 months
Suggested Program: 3x/week cardio + 2x/week strength

PHYSICAL:
Height (cm): 165
Weight (kg): 68
Chest (cm): 92
Waist (cm): 78
Hips (cm): 102
Thigh (cm): 58
Arm (cm): 28

HEALTH:
Key Injuries: Mild lower back issue (2022)
Current Pain/Discomfort: Occasional lower back tightness
Medical Notes: No major restrictions, monitor lower back
Restrictions: No Heavy Lifting

ASSESSMENT:
Last Assessment Date: 2025-10-24
Current Overall Score: 65
Current Strength Score: 62
Current Mobility Score: 60
Current Balance Score: 68
Current Flexibility Score: 68

RELATIONS:
Assigned Trainer: Sarah Smith
```

Click "+" to add new row, fill in all fields above.

✅ **2 Patients added**

---

### C3: Add Sample Workout Log (Optional)

**Open WORKOUT LOGS database**

```
Log ID: WO-2025-10-26-001
Date: 2025-10-26
Duration (min): 60
Exercises & Sets: Bench Press: 4x8 @ 80kg, Squats: 4x8 @ 100kg, Deadlifts: 3x5 @ 120kg
Focus Areas: Strength
What I Noticed: Great form on all exercises, very focused today
What's Improving: Strength improving week over week, especially in deadlifts
Concerns/Issues: None
Overall Session Rating: Excellent
Patient Self-Rating: 4-Easy
Patient Comments: Felt strong today
Patient: John Doe
Trainer: Alex Johnson
```

Click "+" to add new row, fill in fields.

✅ **Sample workout added**

---

### C4: Add Sample Assessment Log (Optional)

**Open ASSESSMENT LOGS database**

```
Assessment ID: ASSESS-JOHN-001
Assessment Date: 2025-10-26
Assessment Number: 1
Strength Score: 75
Mobility Score: 70
Balance Score: 68
Flexibility Score: 72
Strength Tests Details: Upper push 75, lower squat 78, deadlift 72
Mobility Tests Details: Shoulder 68, hip 72, ankle 70, spine 68
Balance Tests Details: Single leg 70, dynamic 66
Flexibility Tests Details: Hamstring 70, hip flexor 72, shoulder 72, lower back 74
Goals Set: Improve overall score to 80+ in 6 months
Program Suggested: 4x/week strength, 2x/week mobility/flexibility
Focus Areas: Strength, Mobility
Trainer Notes: Good baseline fitness, needs more mobility work
Patient: John Doe
Assessed By: Alex Johnson
```

Click "+" to add new row, fill in fields.

✅ **Sample assessment added**

---

## PART D: VERIFICATION (5 minutes)

### Checklist - Verify All Complete

- [ ] **Part A Done:** PATIENTS columns organized into 5 sections
- [ ] **Part B Done:** All 6 databases have relations added
  - [ ] ASSESSMENT LOGS: Patient + Assessed By
  - [ ] WORKOUT LOGS: Patient + Trainer
  - [ ] WEEKLY LOGS: Patient
  - [ ] MONTHLY LOGS: Patient
  - [ ] PATIENTS: Assigned Trainer + Assessment Logs + Workout Logs + Weekly Logs + Monthly Logs

- [ ] **Part C Done:** Sample data added
  - [ ] 2 Trainers (Alex Johnson, Sarah Smith)
  - [ ] 2 Patients (John Doe, Jane Smith)
  - [ ] 1 Workout log
  - [ ] 1 Assessment log

### Quick Verification Test

1. Open **PATIENTS** database
2. Click on "John Doe"
3. Verify you can see:
   - Contact info filled in
   - Assessment scores showing
   - "Assigned Trainer" shows "Alex Johnson"

If all ✓, you're ready for backend!

---

## ✅ COMPLETE!

Your Notion setup is now ready for backend development.

**Database IDs (Save for backend):**
```
NOTION_DATABASE_ID_PATIENTS=298d97e8-c876-8155-91a6-f4a4a816c1f1
NOTION_DATABASE_ID_TRAINERS=298d97e8-c876-817d-8d02-db5c3a64ba6d
NOTION_DATABASE_ID_ASSESSMENTS=298d97e8-c876-814a-81f9-fd691a0c9270
NOTION_DATABASE_ID_WORKOUTS=298d97e8-c876-8179-be21-fea272d651a5
NOTION_DATABASE_ID_WEEKLY=298d97e8-c876-81a4-aef8-c4e8c80cf26f
NOTION_DATABASE_ID_MONTHLY=298d97e8-c876-811d-acfe-cf3b630fcd7e
```

---

## Next: Backend Setup

Once complete, I'll help you set up:
1. Python + FastAPI backend
2. Deploy to Railway
3. Zapier automation
4. End-to-end testing

**Let me know when done! 🚀**
