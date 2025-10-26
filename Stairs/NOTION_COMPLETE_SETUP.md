# Complete Notion Setup - All Steps in One

**Total Time: 30 minutes**
**Status: Ready to execute step-by-step**

---

## PART A: ORGANIZE PATIENTS DATABASE COLUMNS (5 minutes)

Your PATIENTS database has all properties but they need organizing into visual sections.

### How to Reorder Columns in Notion

1. Open **PATIENTS** database in your Stairs workspace
2. For each section below, drag columns to group them together
3. Drag using the **6-dot menu** next to the column header

### SECTION 1: PATIENT CONTACT INFORMATION
Drag these to the left side first:
- Name (already first)
- Email
- Phone
- Date of Birth
- Gender

### SECTION 2: REGISTRATION INFORMATION
- Status
- Registration Date
- Primary Goal
- Target Weight
- Goal Notes
- Suggested Program

### SECTION 3: PHYSICAL INFORMATION (Body Measurements)
- Height (cm)
- Weight (kg)
- Chest (cm)
- Waist (cm)
- Hips (cm)
- Thigh (cm)
- Arm (cm)

### SECTION 4: HEALTH & INJURY INFORMATION
- Key Injuries
- Current Pain/Discomfort
- Medical Notes
- Restrictions

### SECTION 5: FIRST ASSESSMENT INFORMATION
- Last Assessment Date
- Current Overall Score ⭐ (Main KPI - 0-100)
- Current Strength Score
- Current Mobility Score
- Current Balance Score
- Current Flexibility Score

---

## PART B: ADD RELATIONS TO ALL DATABASES (10 minutes)

Relations connect databases together. Add manually in Notion.

### STEP B1: Add Relations to ASSESSMENT LOGS

1. Open **ASSESSMENT LOGS** database
2. Click **"+ Add a property"** (top right)
3. **Add: Patient**
   - Name: Patient
   - Type: Relation
   - Select database: PATIENTS
   - Click Done

4. Click **"+ Add a property"** again
5. **Add: Assessed By**
   - Name: Assessed By
   - Type: Relation
   - Select database: TRAINERS
   - Click Done

✅ ASSESSMENT LOGS now has 2 relations

---

### STEP B2: Add Relations to WORKOUT LOGS

1. Open **WORKOUT LOGS** database
2. Click **"+ Add a property"**
3. **Add: Patient**
   - Name: Patient
   - Type: Relation
   - Select database: PATIENTS
   - Click Done

4. Click **"+ Add a property"**
5. **Add: Trainer**
   - Name: Trainer
   - Type: Relation
   - Select database: TRAINERS
   - Click Done

✅ WORKOUT LOGS now has 2 relations

---

### STEP B3: Add Relations to WEEKLY LOGS

1. Open **WEEKLY LOGS** database
2. Click **"+ Add a property"**
3. **Add: Patient**
   - Name: Patient
   - Type: Relation
   - Select database: PATIENTS
   - Click Done

✅ WEEKLY LOGS now has 1 relation

---

### STEP B4: Add Relations to MONTHLY LOGS

1. Open **MONTHLY LOGS** database
2. Click **"+ Add a property"**
3. **Add: Patient**
   - Name: Patient
   - Type: Relation
   - Select database: PATIENTS
   - Click Done

✅ MONTHLY LOGS now has 1 relation

---

### STEP B5: Add Relations Back to PATIENTS

1. Open **PATIENTS** database
2. Click **"+ Add a property"**
3. **Add: Assigned Trainer**
   - Name: Assigned Trainer
   - Type: Relation
   - Select database: TRAINERS
   - Click Done

4. Click **"+ Add a property"**
5. **Add: Assessment Logs**
   - Name: Assessment Logs
   - Type: Relation
   - Select database: ASSESSMENT LOGS
   - Click Done

6. Click **"+ Add a property"**
7. **Add: Workout Logs**
   - Name: Workout Logs
   - Type: Relation
   - Select database: WORKOUT LOGS
   - Click Done

8. Click **"+ Add a property"**
9. **Add: Weekly Logs**
   - Name: Weekly Logs
   - Type: Relation
   - Select database: WEEKLY LOGS
   - Click Done

10. Click **"+ Add a property"**
11. **Add: Monthly Logs**
    - Name: Monthly Logs
    - Type: Relation
    - Select database: MONTHLY LOGS
    - Click Done

✅ PATIENTS now has 5 relations

---

## PART C: ADD SAMPLE TEST DATA (15 minutes)

Now populate with test data to verify everything works.

### STEP C1: Add Test Trainers to TRAINERS Database

1. Open **TRAINERS** database
2. Click **"+ Add a row"** at the bottom
3. **Fill in Trainer 1:**
   - Name: Alex Johnson
   - Email: alex@gym.com
   - Phone: +1-555-0001
   - Active Status: ✓ (check the box)
   - Specialization: Select "Strength" and "Cardio"

4. Click **"+ Add a row"** again
5. **Fill in Trainer 2:**
   - Name: Sarah Smith
   - Email: sarah@gym.com
   - Phone: +1-555-0002
   - Active Status: ✓ (check the box)
   - Specialization: Select "Flexibility" and "Rehabilitation"

✅ TRAINERS database now has 2 test trainers

---

### STEP C2: Add Test Patients to PATIENTS Database

1. Open **PATIENTS** database
2. Click **"+ Add a row"** at the bottom
3. **Fill in Patient 1: John Doe**

**CONTACT INFORMATION:**
- Name: John Doe
- Email: john@email.com
- Phone: +1-555-1001
- Date of Birth: 1990-05-15
- Gender: Male

**REGISTRATION INFORMATION:**
- Status: Active
- Registration Date: 2025-10-26
- Primary Goal: Muscle Gain
- Target Weight: 85
- Goal Notes: Increase muscle mass and strength
- Suggested Program: 4x/week strength training

**PHYSICAL INFORMATION:**
- Height (cm): 180
- Weight (kg): 75
- Chest (cm): 100
- Waist (cm): 85
- Hips (cm): 95
- Thigh (cm): 55
- Arm (cm): 35

**HEALTH & INJURY:**
- Key Injuries: None
- Current Pain/Discomfort: None
- Medical Notes: Healthy
- Restrictions: (leave empty)

**ASSESSMENT INFORMATION:**
- Last Assessment Date: 2025-10-26
- Current Overall Score: 72
- Current Strength Score: 75
- Current Mobility Score: 70
- Current Balance Score: 68
- Current Flexibility Score: 72

**RELATIONS:**
- Assigned Trainer: Click and select "Alex Johnson"

---

4. Click **"+ Add a row"** again
5. **Fill in Patient 2: Jane Smith**

**CONTACT INFORMATION:**
- Name: Jane Smith
- Email: jane@email.com
- Phone: +1-555-1002
- Date of Birth: 1992-08-22
- Gender: Female

**REGISTRATION INFORMATION:**
- Status: Active
- Registration Date: 2025-10-24
- Primary Goal: Weight Loss
- Target Weight: 60
- Goal Notes: Lose 5kg in 3 months
- Suggested Program: 3x/week cardio + 2x/week strength

**PHYSICAL INFORMATION:**
- Height (cm): 165
- Weight (kg): 68
- Chest (cm): 92
- Waist (cm): 78
- Hips (cm): 102
- Thigh (cm): 58
- Arm (cm): 28

**HEALTH & INJURY:**
- Key Injuries: Mild lower back issue (2022)
- Current Pain/Discomfort: Occasional lower back tightness
- Medical Notes: No major restrictions, monitor lower back
- Restrictions: Click and select "No Heavy Lifting"

**ASSESSMENT INFORMATION:**
- Last Assessment Date: 2025-10-24
- Current Overall Score: 65
- Current Strength Score: 62
- Current Mobility Score: 60
- Current Balance Score: 68
- Current Flexibility Score: 68

**RELATIONS:**
- Assigned Trainer: Click and select "Sarah Smith"

✅ PATIENTS database now has 2 test patients

---

### STEP C3: Add Sample Workout Log (Optional but Recommended)

1. Open **WORKOUT LOGS** database
2. Click **"+ Add a row"**
3. **Fill in Sample Workout:**

**BASIC INFO:**
- Log ID: WO-2025-10-26-001
- Date: 2025-10-26
- Duration (min): 60

**WORKOUT DETAILS:**
- Exercises & Sets:
  ```
  Bench Press: 4x8 @ 80kg
  Squats: 4x8 @ 100kg
  Deadlifts: 3x5 @ 120kg
  ```
- Focus Areas: Select "Strength"

**TRAINER COMMENTARY:**
- What I Noticed: Great form on all exercises, very focused today
- What's Improving: Strength improving week over week, especially in deadlifts
- Concerns/Issues: None
- Overall Session Rating: Excellent

**PATIENT FEEDBACK:**
- Patient Self-Rating: 4-Easy
- Patient Comments: Felt strong today

**RELATIONS:**
- Patient: Select "John Doe"
- Trainer: Select "Alex Johnson"

✅ Optional workout log added for testing

---

### STEP C4: Add Sample Assessment Log (Optional)

1. Open **ASSESSMENT LOGS** database
2. Click **"+ Add a row"**
3. **Fill in Assessment:**

**BASIC INFO:**
- Assessment ID: ASSESS-JOHN-001
- Assessment Date: 2025-10-26
- Assessment Number: 1

**SCORES:**
- Strength Score: 75
- Mobility Score: 70
- Balance Score: 68
- Flexibility Score: 72

**DETAILS:**
- Strength Tests Details: Upper push 75, lower squat 78, deadlift 72
- Mobility Tests Details: Shoulder 68, hip 72, ankle 70, spine 68
- Balance Tests Details: Single leg 70, dynamic 66
- Flexibility Tests Details: Hamstring 70, hip flexor 72, shoulder 72, lower back 74

**GOALS & PROGRAM:**
- Goals Set: Improve overall score to 80+ in 6 months
- Program Suggested: 4x/week strength, 2x/week mobility/flexibility
- Focus Areas: Select "Strength" and "Mobility"
- Trainer Notes: Good baseline fitness, needs more mobility work

**RELATIONS:**
- Patient: Select "John Doe"
- Assessed By: Select "Alex Johnson"

✅ Sample assessment added

---

## PART D: VERIFICATION CHECKLIST (Final verification)

Before moving to backend, verify everything:

**DATABASES CREATED:**
- [ ] PATIENTS (with all properties organized into 5 sections)
- [ ] TRAINERS (with properties)
- [ ] ASSESSMENT LOGS (with relations)
- [ ] WORKOUT LOGS (with relations)
- [ ] WEEKLY LOGS (with relations)
- [ ] MONTHLY LOGS (with relations)

**RELATIONS WORKING:**
- [ ] Open PATIENTS > John Doe > "Assigned Trainer" shows "Alex Johnson"
- [ ] Open PATIENTS > Jane Smith > "Assigned Trainer" shows "Sarah Smith"
- [ ] Open WORKOUT LOGS > Click the relation cells and verify data shows up
- [ ] Open ASSESSMENT LOGS > Relations link to PATIENTS and TRAINERS

**DATA POPULATED:**
- [ ] 2 trainers in TRAINERS database
- [ ] 2 patients in PATIENTS database with full contact, registration, physical, health, and assessment info
- [ ] Sample workout log (optional but recommended)
- [ ] Sample assessment log (optional but recommended)

**VISUAL ORGANIZATION:**
- [ ] PATIENTS columns are organized into 5 clear sections
- [ ] Database is easy to read when scrolling right

---

## SUCCESS! 🎉

Your Notion setup is now complete:
- ✅ 6 databases created
- ✅ Columns organized logically
- ✅ Relations set up between databases
- ✅ Sample data added for testing
- ✅ Ready for backend development

---

## NEXT STEPS

Once you confirm this is complete, I'll help you with:

1. **Part 2: Backend Setup (Python + FastAPI)**
   - Create project structure
   - Set up environment variables
   - Write the API code
   - Deploy to Railway

2. **Part 3: Zapier Automation**
   - Set up weekly reports
   - Set up monthly reports
   - Configure email and WhatsApp

3. **Part 4: Testing & Launch**
   - Test the complete system
   - Train trainers
   - Go live!

---

## Database IDs (Save These)

Keep these IDs - you'll need them for the backend:

```
NOTION_API_KEY = [Your integration token from Step 1.1]

NOTION_DATABASE_ID_PATIENTS = 298d97e8-c876-8155-91a6-f4a4a816c1f1
NOTION_DATABASE_ID_TRAINERS = 298d97e8-c876-817d-8d02-db5c3a64ba6d
NOTION_DATABASE_ID_ASSESSMENTS = 298d97e8-c876-814a-81f9-fd691a0c9270
NOTION_DATABASE_ID_WORKOUTS = 298d97e8-c876-8179-be21-fea272d651a5
NOTION_DATABASE_ID_WEEKLY = 298d97e8-c876-81a4-aef8-c4e8c80cf26f
NOTION_DATABASE_ID_MONTHLY = 298d97e8-c876-811d-acfe-cf3b630fcd7e
```

---

## Support

Questions while setting up?
- Check Notion help: notion.so/help
- All instructions are step-by-step
- Take your time - no rush!

**Good luck! Let me know when complete! 🚀**
