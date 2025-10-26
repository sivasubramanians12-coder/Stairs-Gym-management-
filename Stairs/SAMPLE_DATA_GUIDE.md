# Adding Sample Test Data - Quick Guide

After organizing columns and adding relations, add test data to verify everything works.

---

## STEP 1: Add Test Trainers

Open **TRAINERS** database and add 2 test trainers:

### Trainer 1:
- **Name:** Alex Johnson
- **Email:** alex@gym.com
- **Phone:** +1-555-0001
- **Active Status:** ✓ (checked)
- **Specialization:** Strength, Cardio

### Trainer 2:
- **Name:** Sarah Smith
- **Email:** sarah@gym.com
- **Phone:** +1-555-0002
- **Active Status:** ✓ (checked)
- **Specialization:** Flexibility, Rehabilitation

---

## STEP 2: Add Test Patients

Open **PATIENTS** database and add 2 test patients:

### Patient 1: John Doe

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
- Assigned Trainer: Alex Johnson

---

### Patient 2: Jane Smith

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
- Restrictions: No Heavy Lifting (select this one)

**ASSESSMENT INFORMATION:**
- Last Assessment Date: 2025-10-24
- Current Overall Score: 65
- Current Strength Score: 62
- Current Mobility Score: 60
- Current Balance Score: 68
- Current Flexibility Score: 68

**RELATIONS:**
- Assigned Trainer: Sarah Smith

---

## Verification Checklist

After adding data, verify:

- [ ] **TRAINERS database:** 2 trainers added
- [ ] **PATIENTS database:** 2 patients added
- [ ] **Relations working:**
  - Open John Doe → "Assigned Trainer" shows "Alex Johnson" ✓
  - Open Jane Smith → "Assigned Trainer" shows "Sarah Smith" ✓
- [ ] **All contact info filled in:** Emails, phones, DOB
- [ ] **Physical measurements:** Height, weight, and body measurements
- [ ] **Assessment scores:** Overall score and component scores visible

---

## Next: Add Test Workouts (Optional)

To fully test the system, you can add a sample workout:

Open **WORKOUT LOGS** database and add:

### Sample Workout:
- **Log ID:** WO-2025-10-26-001
- **Patient:** John Doe (select from relation)
- **Date:** 2025-10-26
- **Duration (min):** 60
- **Exercises & Sets:**
  ```
  Bench Press: 4x8 @ 80kg
  Squats: 4x8 @ 100kg
  Deadlifts: 3x5 @ 120kg
  ```
- **Focus Areas:** Strength (select)
- **What I Noticed:** Great form on all exercises, very focused today
- **What's Improving:** Strength improving week over week, especially in deadlifts
- **Concerns/Issues:** None
- **Overall Session Rating:** Excellent
- **Patient Self-Rating:** 4-Easy
- **Trainer:** Alex Johnson (relation)

---

## Time Required

- Adding trainers: 2 minutes
- Adding patients: 5 minutes
- Adding sample workout: 2 minutes
- **Total: ~10 minutes**

---

## Success Indicators

✅ You're ready for backend when:
1. All test data is added
2. Relations are working (you can click between databases)
3. You can see linked records showing up correctly
4. Database structure is organized

**Congratulations! Your Notion setup is complete! 🎉**

Next step: Backend setup with Python + FastAPI
