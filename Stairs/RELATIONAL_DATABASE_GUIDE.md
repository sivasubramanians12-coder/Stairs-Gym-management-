# Relational Database Guide - Stairs Gym System

**Date:** 2025-10-26
**Purpose:** Manual setup guide for creating relationships between all 6 databases

---

## DATABASE STRUCTURE OVERVIEW

### Current Databases with IDs

1. **PATIENTS** - ID: `298d97e8-c876-81b0-a954-f1db89bda5d7`
   - Has auto-generated Patient ID (unique_id field: "Id")
   - 10 patient records

2. **TRAINERS** - ID: `298d97e8-c876-817d-8d02-db5c3a64ba6d`
   - Has auto-generated Trainer ID (unique_id field: "id")
   - 10 trainer records

3. **ASSESSMENT LOGS** - ID: `298d97e8-c876-814a-81f9-fd691a0c9270`
4. **WORKOUT LOGS** - ID: `298d97e8-c876-8179-be21-fea272d651a5`
5. **WEEKLY LOGS** - ID: `298d97e8-c876-81a4-aef8-c4e8c80cf26f`
6. **MONTHLY LOGS** - ID: `298d97e8-c876-811d-acfe-cf3b630fcd7e`

---

## RELATIONAL MODEL

```
TRAINERS (1) ────────< (Many) PATIENTS
    │                      │
    │                      ├──────< ASSESSMENT LOGS (Many)
    │                      ├──────< WORKOUT LOGS (Many)
    │                      ├──────< WEEKLY LOGS (Many)
    │                      └──────< MONTHLY LOGS (Many)
    └──────────────────────────< ASSESSMENT LOGS (Many)
    └──────────────────────────< WORKOUT LOGS (Many)
```

### Relationships Explained:

1. **One Trainer → Many Patients**
   - Each patient has ONE assigned trainer
   - Each trainer can have MULTIPLE patients

2. **One Patient → Many Assessment Logs**
   - Each assessment belongs to ONE patient
   - Each patient can have MULTIPLE assessments over time

3. **One Patient → Many Workout Logs**
   - Each workout belongs to ONE patient
   - Each patient can have MULTIPLE workout sessions

4. **One Trainer → Many Assessment Logs**
   - Each assessment is conducted by ONE trainer
   - Each trainer can conduct MULTIPLE assessments

5. **One Trainer → Many Workout Logs**
   - Each workout is supervised by ONE trainer
   - Each trainer can supervise MULTIPLE workouts

6. **One Patient → Many Weekly/Monthly Logs**
   - Each log belongs to ONE patient
   - Each patient can have MULTIPLE weekly/monthly reports

---

## PART 1: ADD RELATIONS TO DATABASES (10 minutes)

### STEP 1.1: Add Relations to ASSESSMENT LOGS

1. Open **ASSESSMENT LOGS** database in Notion
2. Click **"+ Add a property"** (top right)

**Relation 1: Patient**
- Property name: `Patient`
- Type: `Relation`
- Related database: `PATIENTS`
- Click "Done"

3. Click **"+ Add a property"** again

**Relation 2: Assessed By**
- Property name: `Assessed By`
- Type: `Relation`
- Related database: `TRAINERS`
- Click "Done"

✅ **ASSESSMENT LOGS now has 2 relations**

---

### STEP 1.2: Add Relations to WORKOUT LOGS

1. Open **WORKOUT LOGS** database in Notion
2. Click **"+ Add a property"**

**Relation 1: Patient**
- Property name: `Patient`
- Type: `Relation`
- Related database: `PATIENTS`
- Click "Done"

3. Click **"+ Add a property"** again

**Relation 2: Trainer**
- Property name: `Trainer`
- Type: `Relation`
- Related database: `TRAINERS`
- Click "Done"

✅ **WORKOUT LOGS now has 2 relations**

---

### STEP 1.3: Add Relations to WEEKLY LOGS

1. Open **WEEKLY LOGS** database in Notion
2. Click **"+ Add a property"**

**Relation: Patient**
- Property name: `Patient`
- Type: `Relation`
- Related database: `PATIENTS`
- Click "Done"

✅ **WEEKLY LOGS now has 1 relation**

---

### STEP 1.4: Add Relations to MONTHLY LOGS

1. Open **MONTHLY LOGS** database in Notion
2. Click **"+ Add a property"**

**Relation: Patient**
- Property name: `Patient`
- Type: `Relation`
- Related database: `PATIENTS`
- Click "Done"

✅ **MONTHLY LOGS now has 1 relation**

---

### STEP 1.5: Add Relations to PATIENTS

1. Open **PATIENTS** database in Notion
2. Click **"+ Add a property"**

**Relation 1: Assigned Trainer**
- Property name: `Assigned Trainer`
- Type: `Relation`
- Related database: `TRAINERS`
- Click "Done"

3. Click **"+ Add a property"**

**Relation 2: Assessment Logs**
- Property name: `Assessment Logs`
- Type: `Relation`
- Related database: `ASSESSMENT LOGS`
- Click "Done"

4. Click **"+ Add a property"**

**Relation 3: Workout Logs**
- Property name: `Workout Logs`
- Type: `Relation`
- Related database: `WORKOUT LOGS`
- Click "Done"

5. Click **"+ Add a property"**

**Relation 4: Weekly Logs**
- Property name: `Weekly Logs`
- Type: `Relation`
- Related database: `WEEKLY LOGS`
- Click "Done"

6. Click **"+ Add a property"**

**Relation 5: Monthly Logs**
- Property name: `Monthly Logs`
- Type: `Relation`
- Related database: `MONTHLY LOGS`
- Click "Done"

✅ **PATIENTS now has 5 relations**

---

## PART 2: NAMING CONVENTIONS FOR LOGS

### Assessment Log Naming Format:
```
ASSESS-[PatientID]-[TrainerID]-[Date]

Examples:
- ASSESS-001-T003-20251026
- ASSESS-002-T001-20251024
```

### Workout Log Naming Format:
```
WO-[PatientID]-[TrainerID]-[Date]-[SessionNumber]

Examples:
- WO-001-T003-20251026-001
- WO-002-T001-20251024-002
```

### Weekly Log Naming Format:
```
WEEKLY-[PatientID]-W[WeekNumber]-[Year]

Examples:
- WEEKLY-001-W43-2025
- WEEKLY-002-W42-2025
```

### Monthly Log Naming Format:
```
MONTHLY-[PatientID]-[MonthYear]

Examples:
- MONTHLY-001-OCT2025
- MONTHLY-002-SEP2025
```

---

## PART 3: EXAMPLE DATA RELATIONSHIPS

### Example 1: Patient John Doe (ID: 1)

**Patient Record:**
- Name: John Doe
- Patient ID: 1
- Assigned Trainer: Alex Johnson (Trainer ID: 1)

**Assessment Log:**
- Assessment ID: `ASSESS-001-T001-20251026`
- Patient: John Doe (relation)
- Assessed By: Alex Johnson (relation)
- Date: 2025-10-26

**Workout Log:**
- Log ID: `WO-001-T001-20251026-001`
- Patient: John Doe (relation)
- Trainer: Alex Johnson (relation)
- Date: 2025-10-26

**Weekly Log:**
- Log ID: `WEEKLY-001-W43-2025`
- Patient: John Doe (relation)
- Week: 43, Year: 2025

**Monthly Log:**
- Log ID: `MONTHLY-001-OCT2025`
- Patient: John Doe (relation)
- Month: October 2025

---

## PART 4: CURRENT DATABASE STATUS

### PATIENTS Database (10 records)
```
ID | Name               | Assigned Trainer (To Add)
---|--------------------|--------------------------
1  | John Doe          | Alex Johnson (T1)
2  | Jane Smith        | Sarah Smith (T2)
3  | Michael Brown     | Marcus Chen (T3)
4  | Emily Davis       | Jessica Lee (T4)
5  | Robert Wilson     | Rachel Martinez (T6)
6  | Lisa Anderson     | Nina Patel (T8)
7  | David Martinez    | Tom Anderson (T9)
8  | Sarah Johnson     | Kevin Wright (T7)
9  | James Thompson    | Emily Roberts (T10)
10 | Patricia Garcia   | David Park (T5)
```

### TRAINERS Database (10 records)
```
ID | Name               | Specialization
---|--------------------|---------------------------------
1  | Alex Johnson      | Strength, Cardio
2  | Sarah Smith       | Flexibility, Rehabilitation
3  | Marcus Chen       | Strength, Athletic Performance
4  | Jessica Lee       | Cardio, Endurance
5  | David Park        | Flexibility, Mobility
6  | Rachel Martinez   | Rehabilitation, Strength
7  | Kevin Wright      | Cardio, Weight Loss
8  | Nina Patel        | Flexibility, Balance
9  | Tom Anderson      | Strength, Bodybuilding
10 | Emily Roberts     | Rehabilitation (Inactive)
```

---

## PART 5: STEP-BY-STEP SETUP EXAMPLE

### Example: Link John Doe to Alex Johnson

1. **Open PATIENTS database**
2. **Click on "John Doe" row**
3. **Find "Assigned Trainer" property**
4. **Click the empty field**
5. **Search for "Alex Johnson"**
6. **Select "Alex Johnson"**
7. **Close the record**

✅ Now John Doe is linked to Alex Johnson!

### Create an Assessment Log for John Doe

1. **Open ASSESSMENT LOGS database**
2. **Click "+ New"** to create new record
3. **Fill in:**
   - Assessment ID: `ASSESS-001-T001-20251026`
   - Assessment Date: 2025-10-26
   - Strength Score: 75
   - Mobility Score: 70
   - Balance Score: 68
   - Flexibility Score: 72
   - **Patient:** Click and select "John Doe"
   - **Assessed By:** Click and select "Alex Johnson"
4. **Save**

✅ Now the assessment is linked to both John Doe and Alex Johnson!

---

## PART 6: VERIFICATION CHECKLIST

After setting up relations, verify:

- [ ] **PATIENTS database:**
  - [ ] Open any patient record
  - [ ] "Assigned Trainer" field shows a trainer
  - [ ] Can click trainer to see their full profile

- [ ] **ASSESSMENT LOGS:**
  - [ ] Create sample assessment
  - [ ] Link to patient and trainer
  - [ ] Verify patient's record shows this assessment in "Assessment Logs"

- [ ] **WORKOUT LOGS:**
  - [ ] Create sample workout
  - [ ] Link to patient and trainer
  - [ ] Verify patient's record shows this workout in "Workout Logs"

- [ ] **Bidirectional Relations Work:**
  - [ ] Open a patient → See all their assessments/workouts
  - [ ] Open an assessment → See which patient and trainer
  - [ ] Open a trainer → See all their patients (if relation is two-way)

---

## PART 7: BACKEND INTEGRATION

### Database IDs for .env File

```env
# Notion API
NOTION_API_KEY=[Your integration token]

# Database IDs
NOTION_DATABASE_ID_PATIENTS=298d97e8-c876-81b0-a954-f1db89bda5d7
NOTION_DATABASE_ID_TRAINERS=298d97e8-c876-817d-8d02-db5c3a64ba6d
NOTION_DATABASE_ID_ASSESSMENTS=298d97e8-c876-814a-81f9-fd691a0c9270
NOTION_DATABASE_ID_WORKOUTS=298d97e8-c876-8179-be21-fea272d651a5
NOTION_DATABASE_ID_WEEKLY=298d97e8-c876-81a4-aef8-c4e8c80cf26f
NOTION_DATABASE_ID_MONTHLY=298d97e8-c876-811d-acfe-cf3b630fcd7e
```

### ID Field Names in Databases

```python
# For API queries
PATIENT_ID_FIELD = "Id"  # Auto-generated unique ID
TRAINER_ID_FIELD = "id"  # Auto-generated unique ID
```

---

## SUMMARY

**What You'll Do Manually (15 minutes):**
1. Add 11 relation properties across 5 databases
2. Assign each of the 10 patients to one of the 10 trainers
3. Create sample assessment and workout logs with proper naming

**What You'll Get:**
- Fully relational database structure
- Proper patient → trainer assignments
- Ability to track all logs per patient
- Searchable by Patient ID and Trainer ID
- Ready for backend API integration

---

## NEXT STEPS

1. ✅ Complete Part 1: Add all relations (10 min)
2. ✅ Complete Part 2: Assign trainers to patients (5 min)
3. ✅ Create 2-3 sample logs with proper naming (5 min)
4. ✅ Verify all relations work bidirectionally
5. 🚀 Move to Part 2: Backend Development

**Time Required:** 20 minutes total

Good luck! 🎯
