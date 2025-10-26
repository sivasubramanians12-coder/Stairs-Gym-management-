# Notion Database Setup Guide - Stairs Gym

**Version:** 1.0
**Date:** October 26, 2025
**Purpose:** Complete guide to add standardized fields to Notion databases

---

## 📋 OVERVIEW

This guide shows how to add new fields to your Notion databases to support the standardized templates:
- STANDARDIZED_ASSESSMENT_TEMPLATE.md (Detailed assessment protocols)
- WORKOUT_LOG_CONVERSATION_CHECKLIST.md (Simple conversational checklist for workout logs)
- MEDICAL_HISTORY_REHAB_TEMPLATE.md (Medical tracking framework)

**Databases to Update:**
1. PATIENTS (Patient Database)
2. ASSESSMENT LOGS
3. WORKOUT LOGS
4. WEEKLY LOGS
5. MONTHLY LOGS

---

## 🏥 DATABASE 1: PATIENTS

### Section 1: Medical History Fields

#### Current Medical Conditions
**Field Name:** `Current Medical Conditions`
- **Type:** Multi-select
- **Options:**
  - None
  - Type 1 Diabetes
  - Type 2 Diabetes
  - Hypertension (High BP)
  - Hypotension (Low BP)
  - Heart Disease
  - Asthma
  - COPD
  - Osteoarthritis
  - Rheumatoid Arthritis
  - Osteoporosis
  - Chronic Back Pain
  - Chronic Neck Pain
  - Fibromyalgia
  - Thyroid Disorder
  - Epilepsy
  - Multiple Sclerosis
  - Parkinson's Disease
  - Anxiety Disorder
  - Depression
  - Other

#### Current Medications
**Field Name:** `Current Medications`
- **Type:** Text (long text)
- **Description:** List all medications with dosage (one per line)

#### Past Surgeries
**Field Name:** `Past Surgeries`
- **Type:** Text (long text)
- **Description:** List surgeries with dates and body parts

#### Injury History
**Field Name:** `Injury History (Past 5 Years)`
- **Type:** Text (long text)
- **Description:** List injuries with dates, body parts, and current status

#### Family Medical History
**Field Name:** `Family Medical History`
- **Type:** Text
- **Description:** Relevant family conditions

### Section 2: Current Pain & Discomfort

#### Current Pain Level
**Field Name:** `Current Pain Level`
- **Type:** Number (0-10 scale)
- **Format:** Number

#### Pain Locations
**Field Name:** `Pain Locations`
- **Type:** Multi-select
- **Options:**
  - No Pain
  - Lower Back
  - Upper Back
  - Neck
  - Left Shoulder
  - Right Shoulder
  - Left Elbow
  - Right Elbow
  - Left Wrist
  - Right Wrist
  - Left Hip
  - Right Hip
  - Left Knee
  - Right Knee
  - Left Ankle
  - Right Ankle
  - Other

#### Pain Details
**Field Name:** `Pain Details`
- **Type:** Text (long text)
- **Description:** Type, frequency, triggers

### Section 3: Movement Restrictions

#### Exercise Restrictions
**Field Name:** `Exercise Restrictions`
- **Type:** Multi-select
- **Options:**
  - None
  - Overhead Pressing
  - Deep Squats
  - Deadlifts
  - Jump/Plyometric
  - Running
  - Twisting/Rotation
  - Prone Exercises
  - Supine Exercises
  - Inversions
  - Heavy Loading (>50% 1RM)
  - Valsalva Maneuver
  - Other

#### Modified Exercises
**Field Name:** `Modified Exercises`
- **Type:** Text (long text)
- **Description:** List of exercise modifications (original → modified, reason)

### Section 4: Medical Clearance

#### Clearance Status
**Field Name:** `Medical Clearance Status`
- **Type:** Select
- **Options:**
  - Full Clearance
  - Partial Clearance
  - Clearance Pending
  - No Clearance Obtained
  - Requires Medical Review

#### Doctor's Clearance Notes
**Field Name:** `Doctor Clearance Notes`
- **Type:** Text (long text)

#### PT Clearance Notes
**Field Name:** `PT Clearance Notes`
- **Type:** Text (long text)

#### Last Medical Review Date
**Field Name:** `Last Medical Review Date`
- **Type:** Date

### Section 5: Rehabilitation Status

#### Currently in Rehab
**Field Name:** `Currently in Rehab`
- **Type:** Checkbox

#### Rehab Focus
**Field Name:** `Rehab Focus`
- **Type:** Text
- **Description:** Primary rehabilitation focus area

#### Rehab Start Date
**Field Name:** `Rehab Start Date`
- **Type:** Date

#### Rehab Expected Completion
**Field Name:** `Rehab Expected Completion`
- **Type:** Date

#### Rehab Current Phase
**Field Name:** `Rehab Current Phase`
- **Type:** Text
- **Description:** e.g., "Phase 2 of 4"

### Section 6: Emergency Information

#### Emergency Contact Name
**Field Name:** `Emergency Contact Name`
- **Type:** Text

#### Emergency Contact Phone
**Field Name:** `Emergency Contact Phone`
- **Type:** Phone

#### Emergency Contact Relationship
**Field Name:** `Emergency Contact Relationship`
- **Type:** Text

#### Blood Type
**Field Name:** `Blood Type`
- **Type:** Select
- **Options:**
  - Unknown
  - A+
  - A-
  - B+
  - B-
  - AB+
  - AB-
  - O+
  - O-

---

## 📊 DATABASE 2: ASSESSMENT LOGS

### Section 1: Body Measurements (Already Exists - Verify These)

- ✅ Weight (kg) - Number
- ✅ Height (cm) - Number
- ✅ Chest (cm) - Number
- ✅ Waist (cm) - Number
- ✅ Hips (cm) - Number
- ✅ Thigh (cm) - Number
- ✅ Arm (cm) - Number

### Section 2: Strength Test Scores

#### Squat Form Score
**Field Name:** `Squat Form Score`
- **Type:** Number (0-40)
- **Description:** Bodyweight squat assessment

#### Plank Hold Score
**Field Name:** `Plank Hold Score`
- **Type:** Number (0-30)
- **Description:** Plank duration test

#### Plank Hold Time (seconds)
**Field Name:** `Plank Hold Time`
- **Type:** Number
- **Description:** Actual time held in seconds

#### Push-up Score
**Field Name:** `Push-up Score`
- **Type:** Number (0-30)
- **Description:** Push-up rep test

#### Push-up Reps
**Field Name:** `Push-up Reps`
- **Type:** Number
- **Description:** Number of reps completed

#### Push-up Type
**Field Name:** `Push-up Type`
- **Type:** Select
- **Options:**
  - Standard
  - Modified (on knees)

### Section 3: Mobility Test Scores

#### Overhead Squat Mobility Score
**Field Name:** `Overhead Squat Mobility Score`
- **Type:** Number (0-30)

#### Sit and Reach Score
**Field Name:** `Sit and Reach Score`
- **Type:** Number (0-35)

#### Sit and Reach Distance (cm)
**Field Name:** `Sit and Reach Distance`
- **Type:** Number
- **Description:** Distance beyond toes (positive) or before toes (negative)

#### Shoulder Mobility Score
**Field Name:** `Shoulder Mobility Score`
- **Type:** Number (0-35)

### Section 4: Balance Test Scores

#### Single Leg Balance Eyes Open Score
**Field Name:** `Balance Eyes Open Score`
- **Type:** Number (0-30)

#### Balance Eyes Open Time - Right Leg (seconds)
**Field Name:** `Balance Eyes Open Right`
- **Type:** Number

#### Balance Eyes Open Time - Left Leg (seconds)
**Field Name:** `Balance Eyes Open Left`
- **Type:** Number

#### Single Leg Balance Eyes Closed Score
**Field Name:** `Balance Eyes Closed Score`
- **Type:** Number (0-30)

#### Balance Eyes Closed Time - Right Leg (seconds)
**Field Name:** `Balance Eyes Closed Right`
- **Type:** Number

#### Balance Eyes Closed Time - Left Leg (seconds)
**Field Name:** `Balance Eyes Closed Left`
- **Type:** Number

#### Y-Balance Test Score
**Field Name:** `Y-Balance Score`
- **Type:** Number (0-40)

#### Y-Balance Right Leg Composite (%)
**Field Name:** `Y-Balance Right Composite`
- **Type:** Number

#### Y-Balance Left Leg Composite (%)
**Field Name:** `Y-Balance Left Composite`
- **Type:** Number

### Section 5: Flexibility Test Scores

#### Hip Flexor Flexibility Score
**Field Name:** `Hip Flexor Flexibility Score`
- **Type:** Number (0-25)

#### Shoulder Internal Rotation Score
**Field Name:** `Shoulder IR Score`
- **Type:** Number (0-25)

#### Ankle Dorsiflexion Score
**Field Name:** `Ankle Dorsiflexion Score`
- **Type:** Number (0-25)

#### General Flexibility Score
**Field Name:** `General Flexibility Score`
- **Type:** Number (0-25)

### Section 6: Medical Assessment Fields

#### Movement Restrictions Identified
**Field Name:** `Movement Restrictions`
- **Type:** Multi-select
- **Options:** (Same as PATIENTS Exercise Restrictions)

#### Exercises to Avoid
**Field Name:** `Exercises to Avoid`
- **Type:** Text (long text)

#### Modified Exercises Recommended
**Field Name:** `Modified Exercises Recommended`
- **Type:** Text (long text)

#### Clearance Status at Assessment
**Field Name:** `Clearance Status`
- **Type:** Select
- **Options:**
  - Full Clearance
  - Partial Clearance
  - Medical Review Required

---

## 💪 DATABASE 3: WORKOUT LOGS

### Section 1: Exercise Checklists (Use Formula or Text Fields)

#### Strength Exercises Completed
**Field Name:** `Strength Exercises`
- **Type:** Text (long text)
- **Format:** Checklist format (one exercise per line with sets/reps/weight)
- **Example:**
  ```
  ✓ Push-ups - 3 sets × 10 reps @ bodyweight
  ✓ Bench Press - 3 sets × 8 reps @ 40kg
  ✓ Squats - 4 sets × 10 reps @ 50kg
  ```

#### Mobility Exercises Completed
**Field Name:** `Mobility Exercises`
- **Type:** Text (long text)
- **Format:** Same as above

#### Balance Exercises Completed
**Field Name:** `Balance Exercises`
- **Type:** Text (long text)
- **Format:** Same as above

### Section 2: Medical & Safety Notes

#### Pre-Workout Health Check
**Field Name:** `Pre-Workout Health Check`
- **Type:** Multi-select
- **Options:**
  - Feeling Normal/Healthy
  - New Pain Since Last Session
  - Increased Pain in Existing Condition
  - Illness (Cold/Flu/Infection)
  - Dizziness or Lightheadedness
  - Unusual Fatigue
  - Difficulty Breathing
  - Chest Pain or Pressure
  - Heart Palpitations
  - Nausea
  - Headache
  - Took Pain Medication Today
  - Skipped Regular Medication
  - Poor Sleep (<5 hours)
  - Dehydrated
  - Fasting (>6 hours)
  - Recent Alcohol (<24hrs)
  - High Stress Level

#### Pain During Session
**Field Name:** `Pain During Session`
- **Type:** Checkbox

#### Pain Details During Session
**Field Name:** `Pain Details`
- **Type:** Text (long text)
- **Format:** Body part, severity (0-10), during which exercise, action taken

#### Modifications Made
**Field Name:** `Modifications Made This Session`
- **Type:** Text (long text)
- **Format:** Original exercise → Modified to, Reason

#### Safety Incidents
**Field Name:** `Safety Incidents`
- **Type:** Multi-select
- **Options:**
  - None
  - Pain/Discomfort During Exercise
  - Form Breakdown
  - Loss of Balance
  - Equipment Issue
  - Session Ended Early
  - Other

#### Incident Details
**Field Name:** `Incident Details`
- **Type:** Text (long text)

### Section 3: Performance Metrics

#### Session Intensity (RPE)
**Field Name:** `Session Intensity (RPE)`
- **Type:** Select
- **Options:**
  - Light (RPE 1-3)
  - Moderate (RPE 4-6)
  - Hard (RPE 7-8)
  - Very Hard (RPE 9-10)

#### Total Exercises Completed
**Field Name:** `Total Exercises`
- **Type:** Number

#### Total Sets Completed
**Field Name:** `Total Sets`
- **Type:** Number

#### Total Reps Completed
**Field Name:** `Total Reps`
- **Type:** Number

#### Total Weight Lifted (kg)
**Field Name:** `Total Weight Lifted`
- **Type:** Number
- **Description:** Sum of all sets

#### Post-Workout Energy Level
**Field Name:** `Post-Workout Energy`
- **Type:** Number (1-10 scale)

#### Patient Self-Reported Difficulty
**Field Name:** `Patient Difficulty Rating`
- **Type:** Number (1-10 scale)

#### Patient Self-Reported Enjoyment
**Field Name:** `Patient Enjoyment Rating`
- **Type:** Number (1-10 scale)

---

## 📅 DATABASE 4: WEEKLY LOGS

### Section 1: Pain Tracking

#### Average Pain Level This Week
**Field Name:** `Average Pain Level`
- **Type:** Number (0-10)
- **Description:** Average across all sessions

#### Pain Trend
**Field Name:** `Pain Trend`
- **Type:** Select
- **Options:**
  - Improving (Decreasing)
  - Stable (No Change)
  - Worsening (Increasing)
  - Variable

### Section 2: Medical Summary

#### New Issues This Week
**Field Name:** `New Issues This Week`
- **Type:** Text (long text)
- **Description:** New pain, injuries, or concerns

#### Medication Changes
**Field Name:** `Medication Changes`
- **Type:** Text
- **Description:** New, stopped, or dosage changed

#### Medical Appointments This Week
**Field Name:** `Medical Appointments`
- **Type:** Text (long text)
- **Description:** Doctor visits, PT sessions, specialist visits

### Section 3: Incident Summary

#### Total Incidents This Week
**Field Name:** `Total Incidents`
- **Type:** Number

#### Incident Severity
**Field Name:** `Incident Severity`
- **Type:** Select
- **Options:**
  - None
  - Minor
  - Moderate
  - Severe

---

## 📊 DATABASE 5: MONTHLY LOGS

### Section 1: Pain Tracking

#### Monthly Average Pain Level
**Field Name:** `Monthly Average Pain`
- **Type:** Number (0-10)

#### Pain Trend
**Field Name:** `Pain Trend`
- **Type:** Select
- **Options:**
  - Improving
  - Stable
  - Declining
  - Mixed

### Section 2: Medical Changes Summary

#### Medical Changes This Month
**Field Name:** `Medical Changes`
- **Type:** Text (long text)
- **Format:**
  ```
  - New diagnosis: [if any]
  - New medication: [if any]
  - Surgery scheduled: [if any]
  - PT started/completed: [if any]
  ```

#### Program Modifications Made
**Field Name:** `Program Modifications`
- **Type:** Text (long text)
- **Format:** Date, Reason, Modification, Outcome

### Section 3: Incident Summary

#### Total Incidents This Month
**Field Name:** `Total Incidents`
- **Type:** Number

#### Minor Incidents Count
**Field Name:** `Minor Incidents`
- **Type:** Number

#### Moderate Incidents Count
**Field Name:** `Moderate Incidents`
- **Type:** Number

#### Severe Incidents Count
**Field Name:** `Severe Incidents`
- **Type:** Number

---

## ✅ IMPLEMENTATION CHECKLIST

### Phase 1: PATIENTS Database (Priority: HIGH)
- [ ] Add medical history fields (conditions, medications, surgeries, injuries)
- [ ] Add current pain tracking fields
- [ ] Add movement restrictions fields
- [ ] Add medical clearance fields
- [ ] Add rehabilitation status fields
- [ ] Add emergency information fields
- [ ] Test with one patient record

### Phase 2: ASSESSMENT LOGS Database (Priority: HIGH)
- [ ] Verify body measurement fields exist
- [ ] Add strength test score fields (squat, plank, push-up)
- [ ] Add mobility test score fields (overhead squat, sit & reach, shoulder)
- [ ] Add balance test score fields (eyes open, eyes closed, Y-balance)
- [ ] Add flexibility test score fields
- [ ] Add medical assessment fields
- [ ] Test with one assessment record

### Phase 3: WORKOUT LOGS Database (Priority: MEDIUM)
- [ ] Add exercise checklist fields (strength, mobility, balance)
- [ ] Add pre-workout health check field
- [ ] Add pain during session fields
- [ ] Add modifications tracking fields
- [ ] Add safety incident fields
- [ ] Add performance metrics fields
- [ ] Add patient self-report fields
- [ ] Test with one workout record

### Phase 4: WEEKLY LOGS Database (Priority: MEDIUM)
- [ ] Add pain tracking fields
- [ ] Add pain trend field
- [ ] Add medical summary fields
- [ ] Add incident summary fields
- [ ] Test with one weekly report

### Phase 5: MONTHLY LOGS Database (Priority: LOW)
- [ ] Add monthly pain tracking fields
- [ ] Add medical changes summary fields
- [ ] Add program modifications field
- [ ] Add incident breakdown fields
- [ ] Test with one monthly report

### Phase 6: Testing & Validation
- [ ] Create one complete patient record with all fields
- [ ] Create one complete assessment with all fields
- [ ] Create one complete workout log with all fields
- [ ] Generate one weekly report with new fields
- [ ] Generate one monthly report with new fields
- [ ] Verify all relations work correctly
- [ ] Update report generation scripts if needed

---

## 🔧 FIELD NAMING CONVENTIONS

**Best Practices:**
1. Use clear, descriptive names
2. Use consistent capitalization (Title Case recommended)
3. Avoid abbreviations unless commonly understood
4. Group related fields with prefixes when helpful
   - Example: `Balance Eyes Open Score`, `Balance Eyes Closed Score`

**Field Type Recommendations:**
- **Checklists:** Multi-select
- **Free text notes:** Text (long text)
- **Scores (0-100):** Number
- **Yes/No:** Checkbox
- **Categories:** Select (single choice) or Multi-select (multiple choices)
- **Dates:** Date
- **Phone numbers:** Phone
- **Pain levels:** Number (0-10 scale)

---

## 📝 MIGRATION STRATEGY

### Option 1: Gradual Migration (Recommended)
1. Add fields to PATIENTS database first
2. Update 2-3 patient records manually to test
3. Add fields to ASSESSMENT LOGS
4. Create one complete assessment using new template
5. Add fields to WORKOUT LOGS
6. Have trainers use new fields for 1 week
7. Add fields to WEEKLY and MONTHLY logs
8. Generate reports with new data

**Timeline:** 2-3 weeks
**Risk:** Low
**Benefit:** Can catch issues early

### Option 2: Full Migration
1. Add all fields to all databases at once
2. Update all existing records
3. Train all trainers on new fields
4. Switch to new system immediately

**Timeline:** 1 week intensive
**Risk:** Medium-High
**Benefit:** Quick deployment

### Option 3: Parallel System (Safest)
1. Create duplicate databases with new fields
2. Run both old and new systems for 2 weeks
3. Compare outputs
4. Switch to new system when confident

**Timeline:** 3-4 weeks
**Risk:** Very Low
**Benefit:** No data loss risk, can revert if needed

---

## 🚨 IMPORTANT NOTES

### Data Privacy & Security
- Medical information is HIPAA-sensitive
- Ensure proper access controls on Notion workspace
- Only authorized trainers should access medical fields
- Consider separate database for detailed medical records

### Required vs Optional Fields
**Required (Cannot be blank):**
- Assessment ID
- Patient relation
- Assessment Date
- Workout Date
- Log IDs

**Optional but Recommended:**
- All medical fields (may not apply to all patients)
- Pain tracking (only if patient has pain)
- Incident tracking (only if incidents occur)

### Field Updates After Setup
Once trainers start using fields:
1. Avoid renaming fields (breaks formulas)
2. Avoid changing field types (causes data loss)
3. You can safely add new multi-select options
4. You can add new fields without affecting existing data

---

## 💡 TIPS FOR TRAINERS

### Using New Fields Efficiently
1. **Pre-fill common options:** Create templates with most-used selections
2. **Use keyboard shortcuts:** Tab through fields quickly
3. **Copy previous records:** Duplicate last session and update only changes
4. **Focus on facts:** Only fill what applies, leave blanks if no data

### Prioritize These Fields
**Every Session Must Have:**
- Exercise checklists (what was done)
- Duration
- Trainer observations (factual only)
- Patient pain (if any)

**Fill When Applicable:**
- Pre-workout health check (if issues reported)
- Modifications (if made)
- Incidents (if occurred)
- Patient self-reports (quick 30-second survey)

---

## 📚 RELATED DOCUMENTATION

- **STANDARDIZED_ASSESSMENT_TEMPLATE.md** - Full assessment protocol
- **STANDARDIZED_WORKOUT_TEMPLATE.md** - Workout tracking guide
- **MEDICAL_HISTORY_REHAB_TEMPLATE.md** - Medical tracking guide
- **TRAINER_NOTES_TEMPLATE.md** - Quick trainer notes
- **RELATIONAL_DATABASE_GUIDE.md** - Database structure overview

---

## 🎯 EXPECTED OUTCOMES

### After Full Implementation:
✅ **100% factual reports** - No AI hallucinations, only recorded data
✅ **Complete medical tracking** - Full patient health history accessible
✅ **Standardized assessments** - Consistent, measurable tests across all patients
✅ **Incident prevention** - Better safety tracking and pattern recognition
✅ **Legal compliance** - Proper medical documentation for liability protection
✅ **Better patient care** - Trainers have full context for each session

---

**Document Version:** 1.0
**Last Updated:** October 26, 2025
**Status:** Ready for Implementation
**Estimated Setup Time:** 3-5 hours (gradual migration)
