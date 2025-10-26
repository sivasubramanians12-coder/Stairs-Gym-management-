# Workout Log Conversation Checklist - Stairs Gym

**Version:** 2.0
**Date:** October 26, 2025
**Purpose:** Simple checklist for trainers to fill workout logs via conversation with Claude

---

## 💬 HOW THIS WORKS

**Instead of filling forms, you chat with Claude:**
- Tell Claude what happened in the session
- Claude asks follow-up questions if needed
- Claude fills the Notion workout log with factual data only
- Takes 2-3 minutes per session

---

## ✅ CONVERSATION CHECKLIST

### Before You Start Talking to Claude:
Say: *"I need to log a workout session for [Patient Name]"*

Then cover these points (Claude will prompt you if you forget):

---

### 📋 SECTION 1: Basic Info (Claude will ask if missing)
- [ ] Patient name
- [ ] Date & time
- [ ] Session duration

---

### 💪 SECTION 2: What Did You Do? (Just tell Claude)
- [ ] **Exercises done** - list them with sets/reps/weight
  - Example: "We did 3 sets of squats at 50kg, 8 reps each"
  - Example: "Plank holds - 3 sets of 45 seconds"
  - Example: "Balance work - single leg stands, 30 seconds each leg"

**Just speak naturally - Claude will organize it into:**
- Strength exercises
- Mobility/flexibility exercises
- Balance exercises
- Cardio (if any)

---

### 📊 SECTION 3: How Did It Go? (Facts only)
- [ ] **Form/technique observations** - what you saw
  - Good: "Form was good on squats, knees tracked well"
  - Good: "Lost balance twice on single leg deadlifts"
  - Bad: "Patient seemed unmotivated" ❌ (speculation)

- [ ] **Comparisons to last session** (if you remember)
  - "Squat weight increased from 45kg to 50kg"
  - "Plank time up from 40 seconds to 45 seconds"
  - If you don't remember, that's fine - say "don't know"

---

### 🩹 SECTION 4: Any Pain or Issues? (Important!)
- [ ] **Did patient report any pain/discomfort?**
  - If YES: Where? How much (0-10)? During which exercise?
  - Use patient's exact words: "Patient said: 'My right knee hurt during lunges'"

- [ ] **Did you modify any exercises?**
  - If YES: Which exercise? Changed to what? Why?
  - Example: "Changed full lunges to half depth because of knee pain"

- [ ] **Any incidents or safety concerns?**
  - Loss of balance, form breakdown, equipment issues, stopped early?

---

### 💬 SECTION 5: Patient Feedback (30 seconds)
- [ ] **What did patient say about the session?**
  - Quote them: "Patient said: 'Felt strong today'"

- [ ] **How did patient rate themselves?** (quick ask)
  - Energy level: ___/10
  - How hard was it: ___/10
  - Did they enjoy it: ___/10

---

### 🎯 SECTION 6: Next Session Plan (Quick note)
- [ ] **Any changes for next time?**
  - "Increase bench press to 42.5kg next time"
  - "Continue monitoring right knee"
  - "No changes, keep current program"

---

## 🗣️ EXAMPLE CONVERSATION

**Trainer:** "I need to log a workout for John Doe from today's session."

**Claude:** "Got it! Tell me what exercises you did."

**Trainer:** "We did squats - 3 sets of 8 reps at 55kg. Then bench press, 3 sets of 10 at 40kg. Finished with plank holds, 3 sets of 45 seconds each."

**Claude:** "Great. How was his form?"

**Trainer:** "Form was good on everything. Squats were much better than last week - knees stayed aligned."

**Claude:** "Did he report any pain or discomfort?"

**Trainer:** "Nope, no pain today."

**Claude:** "Any changes needed for next session?"

**Trainer:** "Yeah, increase squat weight to 57.5kg next time. He's ready."

**Claude:** "Perfect. How did he rate the session - energy and difficulty?"

**Trainer:** "He said he felt strong today. Energy was 8 out of 10, difficulty was about 6."

**Claude:** "Got it. I'll log all that now. Session duration?"

**Trainer:** "45 minutes."

**Claude:** ✅ "Workout logged: WO-001-T001-20251026-001. All done!"

---

## 🚫 WHAT TO AVOID

### DON'T Say:
- ❌ "Patient seems tired" (how do you know? ask them)
- ❌ "Patient is making great progress" (unless you have measurements)
- ❌ "Patient wasn't motivated today" (speculation)

### DO Say:
- ✅ "Patient rated energy 4/10"
- ✅ "Squat weight increased from 50kg to 55kg"
- ✅ "Patient said: 'I'm feeling tired today'"

---

## 📱 QUICK MOBILE VERSION

**Absolute minimum to tell Claude:**
1. Patient name & date
2. Exercises with sets/reps/weight
3. Any pain (yes/no, where, how much)
4. Any modifications made
5. Session duration

Claude will ask for more if needed!

---

## 🎯 CLAUDE'S JOB

When you tell Claude about the workout, Claude will:
1. ✅ Ask clarifying questions if info is missing
2. ✅ Organize exercises into categories (strength/mobility/balance)
3. ✅ Record ONLY what you said - no filler text
4. ✅ Use your exact words for observations and patient quotes
5. ✅ Create the Notion workout log with proper ID format
6. ❌ NOT add motivational language you didn't say
7. ❌ NOT invent progress you didn't mention
8. ❌ NOT speculate about patient's feelings

---

## 💡 TIPS FOR FAST LOGGING

### During the Session:
- Mental note of key numbers (weights, reps, times)
- If patient mentions pain, jot it down immediately
- Ask patient for quick ratings at the end (energy/difficulty/enjoyment)

### After the Session (2-3 minutes):
- Open chat with Claude
- Tell the story of the session naturally
- Claude organizes it into proper format
- Done!

---

## 🔄 WHAT HAPPENS NEXT

Your conversation with Claude → Workout log in Notion → Weekly report (factual summary)

**Weekly Report Will Include:**
- Exercises you logged (with weights/reps)
- Your observations about form/technique
- Patient quotes you provided
- Pain/modifications you noted
- Comparisons you mentioned

**Weekly Report Will NOT Include:**
- Motivational filler
- Invented progress
- Speculation about patient motivation
- Generic "great job" statements (unless YOU said them)

---

## ✅ PRE-FLIGHT CHECKLIST

**Before ending conversation with Claude, verify:**
- [ ] Patient name correct
- [ ] All exercises logged
- [ ] Pain/modifications captured (if any)
- [ ] Patient feedback recorded
- [ ] Next session plan noted
- [ ] Claude confirms workout log ID (WO-XXX-TXXX-YYYYMMDD-XXX)

**That's it! You're done.**

---

**Template Version:** 2.0 (Conversational)
**Time Required:** 2-3 minutes per session
**Best For:** Quick, accurate workout logging via chat with Claude
