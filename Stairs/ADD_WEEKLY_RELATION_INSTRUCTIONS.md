# How to Add Weekly Reports to PATIENTS Database

## The Issue
The WEEKLY LOGS database has a "patient" relation, but it's not showing up in the PATIENTS database because it's a **one-way relation**.

## Solution (2 minutes)

### Option A: Enable Two-Way Relation (Easiest)

1. **Open Notion** and go to your **WEEKLY LOGS** database
2. **Click on the "patient" column header** (at the top of the table)
3. **Click "Edit property"** (or the 3-dot menu → Edit property)
4. In the relation settings, you should see:
   - "Related to: PATIENTS"
   - A checkbox or toggle for **"Show on PATIENTS"**
5. **Enable "Show on PATIENTS"**
6. **Name the reverse property**: Type "Weekly Reports" or "weekly Logs"
7. **Click "Done"** or "Save"

✅ The "Weekly Reports" column should now appear in your PATIENTS database automatically!

---

### Option B: Create New Two-Way Relation (If Option A doesn't work)

1. **Open your PATIENTS database** in Notion
2. **Click "+ New property"** (or just click to the right of the last column)
3. **Property name**: `Weekly Reports`
4. **Property type**: Select **"Relation"**
5. **Related database**: Select **"WEEKLY LOGS"**
6. **Two-way relation**: Make sure this is ENABLED ✓
7. **Property name in WEEKLY LOGS**: Should auto-fill with "patient" or you can name it
8. **Click "Done"**

---

## Verification

After completing either option:

1. **Go to PATIENTS database**
2. **Click on any patient** (like Robert Wilson)
3. **Look for the "Weekly Reports" property**
4. **You should see 1 weekly report** listed there
5. **Click on it** to view the full weekly report

---

## If It's Still Not Working

Run this Python script to verify:

```bash
python fix_weekly_relations.py
```

It will tell you if the relation is properly set up.

---

**After this is done**, all new weekly reports will automatically appear in the PATIENTS database! 🎉
