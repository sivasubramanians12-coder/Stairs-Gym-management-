# Adding Relations Between Databases - Manual Steps

Since the API has strict requirements for relations, we'll add them manually in Notion (takes 5 minutes).

---

## What are Relations?

Relations connect data across databases. For example:
- A PATIENT can have many WORKOUT LOGS
- A WORKOUT LOG belongs to one PATIENT
- This creates a link so data is interconnected

---

## STEP 1: Add Relations to ASSESSMENT LOGS

1. Open **ASSESSMENT LOGS** database
2. Click **"+ Add a property"** (right side)
3. **Create Property #1: Patient**
   - Property name: `Patient`
   - Type: `Relation` (select from dropdown)
   - Database to connect: `PATIENTS`
   - Click "Done"

4. **Create Property #2: Assessed By**
   - Property name: `Assessed By`
   - Type: `Relation`
   - Database to connect: `TRAINERS`
   - Click "Done"

---

## STEP 2: Add Relations to WORKOUT LOGS

1. Open **WORKOUT LOGS** database
2. Click **"+ Add a property"**
3. **Create Property #1: Patient**
   - Property name: `Patient`
   - Type: `Relation`
   - Database to connect: `PATIENTS`
   - Click "Done"

4. **Create Property #2: Trainer**
   - Property name: `Trainer`
   - Type: `Relation`
   - Database to connect: `TRAINERS`
   - Click "Done"

---

## STEP 3: Add Relations to WEEKLY LOGS

1. Open **WEEKLY LOGS** database
2. Click **"+ Add a property"**
3. **Create Property: Patient**
   - Property name: `Patient`
   - Type: `Relation`
   - Database to connect: `PATIENTS`
   - Click "Done"

---

## STEP 4: Add Relations to MONTHLY LOGS

1. Open **MONTHLY LOGS** database
2. Click **"+ Add a property"**
3. **Create Property: Patient**
   - Property name: `Patient`
   - Type: `Relation`
   - Database to connect: `PATIENTS`
   - Click "Done"

---

## STEP 5: Add Relations Back to PATIENTS

1. Open **PATIENTS** database
2. Click **"+ Add a property"** multiple times:

3. **Property #1: Assigned Trainer**
   - Property name: `Assigned Trainer`
   - Type: `Relation`
   - Database: `TRAINERS`
   - Click "Done"

4. **Property #2: Assessment Logs**
   - Property name: `Assessment Logs`
   - Type: `Relation`
   - Database: `ASSESSMENT LOGS`
   - Click "Done"

5. **Property #3: Workout Logs**
   - Property name: `Workout Logs`
   - Type: `Relation`
   - Database: `WORKOUT LOGS`
   - Click "Done"

6. **Property #4: Weekly Logs**
   - Property name: `Weekly Logs`
   - Type: `Relation`
   - Database: `WEEKLY LOGS`
   - Click "Done"

7. **Property #5: Monthly Logs**
   - Property name: `Monthly Logs`
   - Type: `Relation`
   - Database: `MONTHLY LOGS`
   - Click "Done"

---

## How Relations Will Work

Once you add relations, you'll be able to:

**Example: PATIENT "John Doe"**
- Click on `Assigned Trainer` → Select "Trainer A"
- Click on `Workout Logs` → It will auto-show all workouts linked to John
- Click on `Assessment Logs` → Shows all assessments

**Example: WORKOUT LOG entry**
- Click on `Patient` → Select "John Doe"
- Now this workout is linked to John's record
- It auto-appears in John's "Workout Logs" relation

---

## Visual Summary

```
PATIENTS (Master Database)
├── Name (Title)
├── Contact Info (Email, Phone, DOB, Gender)
├── Registration Info (Status, Date, Goal)
├── Physical Info (Height, Weight, Measurements)
├── Health Info (Injuries, Pain, Restrictions)
├── Assessment Info (Scores)
└── Relations:
    ├── Assigned Trainer → TRAINERS
    ├── Assessment Logs → ASSESSMENT LOGS
    ├── Workout Logs → WORKOUT LOGS
    ├── Weekly Logs → WEEKLY LOGS
    └── Monthly Logs → MONTHLY LOGS

TRAINERS → Links to PATIENTS (Assigned Patients)
ASSESSMENT LOGS → Links to PATIENTS (Patient) + TRAINERS (Assessed By)
WORKOUT LOGS → Links to PATIENTS (Patient) + TRAINERS (Trainer)
WEEKLY LOGS → Links to PATIENTS (Patient)
MONTHLY LOGS → Links to PATIENTS (Patient)
```

---

## Checklist

- [ ] Added Patient + Assessed By relations to ASSESSMENT LOGS
- [ ] Added Patient + Trainer relations to WORKOUT LOGS
- [ ] Added Patient relation to WEEKLY LOGS
- [ ] Added Patient relation to MONTHLY LOGS
- [ ] Added 5 relations back to PATIENTS database

**Total time: 5-10 minutes**

Once done, you're ready for sample data! 🚀
