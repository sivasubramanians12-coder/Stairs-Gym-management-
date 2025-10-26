# Stairs Gym Management System

**AI-Powered Gym Management & Reporting System**

A comprehensive gym management system that uses Notion as the database and AI (Groq/Llama) to generate factual, hallucination-free workout reports.

---

## 🎯 Features

### Core Functionality
- **Patient Management** - Complete medical history, restrictions, and rehabilitation tracking
- **Workout Logging** - Conversational logging via Claude (2-3 minutes per session)
- **Assessment System** - Standardized tests with measurable scores (0-100 scale)
- **Automated Reports** - Weekly and monthly reports with ZERO AI hallucinations
- **Medical Tracking** - Comprehensive pain, injury, and incident tracking

### Key Differentiators
✅ **100% Fact-Based Reports** - AI summarizes only recorded data, no speculation
✅ **Conversational Logging** - Trainers chat with Claude to log workouts
✅ **Standardized Assessments** - Consistent, measurable tests across all patients
✅ **Legal Compliance** - Proper medical documentation for liability protection
✅ **Scalable** - Works for any number of trainers and patients

---

## 📁 Project Structure

### Core Templates
- **`STANDARDIZED_ASSESSMENT_TEMPLATE.md`** - Detailed assessment protocols with scoring rubrics
- **`WORKOUT_LOG_CONVERSATION_CHECKLIST.md`** - Simple conversational checklist for workout logging
- **`MEDICAL_HISTORY_REHAB_TEMPLATE.md`** - Comprehensive medical tracking framework

### Documentation
- **`SIMPLIFIED_APPROACH_SUMMARY.md`** - Overview of the conversational logging approach
- **`STANDARDIZATION_COMPLETE_SUMMARY.md`** - Complete system documentation
- **`NOTION_DATABASE_SETUP_GUIDE.md`** - Step-by-step database configuration
- **`RELATIONAL_DATABASE_GUIDE.md`** - Database structure and naming conventions
- **`NAMING_CONVENTION_UPDATE_SUMMARY.md`** - Log naming standards
- **`ASSESSMENT_INTEGRATION_SUMMARY.md`** - Assessment integration details

### Python Scripts

#### Report Generation (AI-Powered)
- **`generate_all_weekly_reports.py`** - Generate weekly reports for all active patients
- **`generate_all_monthly_reports.py`** - Generate monthly reports for all active patients
- **`generate_all_reports_with_assessments.py`** - Generate reports with assessment integration

#### Utilities
- **`fix_workout_log_names.py`** - Fix workout log naming to standard format
- **`fix_weekly_monthly_log_names.py`** - Fix weekly/monthly log naming
- **`verify_all_naming_conventions.py`** - Verify all logs follow naming standards
- **`verify_patient_assessment_updates.py`** - Verify patient assessment scores updated
- **`check_patient_ids.py`** - Verify patient ID structure
- **`check_assessment_structure.py`** - Verify assessment database structure

#### Test Data
- **`test_notion.py`** - Test Notion API connection
- **`create_sample_data.py`** - Create sample workout data for testing

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Notion account with API access
- Groq API account (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Stairs
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file with:
   ```
   NOTION_API_KEY=your_notion_api_key
   NOTION_DATABASE_ID_PATIENTS=your_patients_db_id
   NOTION_DATABASE_ID_TRAINERS=your_trainers_db_id
   NOTION_DATABASE_ID_WORKOUTS=your_workouts_db_id
   NOTION_DATABASE_ID_WEEKLY=your_weekly_db_id
   NOTION_DATABASE_ID_MONTHLY=your_monthly_db_id
   NOTION_DATABASE_ID_ASSESSMENTS=your_assessments_db_id
   GROQ_API_KEY=your_groq_api_key
   ```

4. **Set up Notion databases**

   Follow the guide in `NOTION_DATABASE_SETUP_GUIDE.md` to create and configure your Notion databases.

5. **Test the connection**
   ```bash
   python test_notion.py
   ```

---

## 📊 Usage

### For Trainers: Logging Workouts

**Simple conversational approach (2-3 minutes):**

1. After a workout session, chat with Claude:
   ```
   "I need to log a workout for John Doe"
   ```

2. Tell Claude what happened:
   - Exercises done (sets/reps/weight)
   - Form observations
   - Any pain reported
   - Patient feedback

3. Claude fills the Notion log automatically!

See `WORKOUT_LOG_CONVERSATION_CHECKLIST.md` for complete guide.

### For Assessors: Conducting Assessments

1. Follow the detailed protocols in `STANDARDIZED_ASSESSMENT_TEMPLATE.md`
2. Conduct measurable tests:
   - Strength Tests (Squat Form, Plank, Push-ups)
   - Mobility Tests (Overhead Squat, Sit & Reach, Shoulder Mobility)
   - Balance Tests (Single Leg, Y-Balance)
   - Flexibility Tests
3. Record scores (0-100 scale)
4. Assessment data automatically updates patient records

### For Admins: Generating Reports

**Weekly Reports:**
```bash
python generate_all_weekly_reports.py
```

**Monthly Reports:**
```bash
python generate_all_monthly_reports.py
```

**Reports with Assessments:**
```bash
python generate_all_reports_with_assessments.py
```

**Verify Naming Conventions:**
```bash
python verify_all_naming_conventions.py
```

---

## 🏗️ Architecture

### Data Flow
```
TRAINER LOGS WORKOUT (via chat with Claude)
    ↓
NOTION WORKOUT LOGS DATABASE
    ↓
AI REPORT GENERATION (Weekly/Monthly)
(Temperature: 0.3 - factual only)
(Explicit instructions: NO hallucinations)
    ↓
100% FACT-BASED REPORTS
(Sent to patients)
```

### Naming Conventions

All logs follow standardized format:

- **Assessments:** `ASSESS-[PatientID]-[TrainerID]-[Date]`
  - Example: `ASSESS-001-T003-20251026`

- **Workouts:** `WO-[PatientID]-[TrainerID]-[Date]-[SessionNumber]`
  - Example: `WO-001-T001-20251026-001`

- **Weekly Logs:** `WEEKLY-[PatientID]-W[WeekNumber]-[Year]`
  - Example: `WEEKLY-001-W43-2025`

- **Monthly Logs:** `MONTHLY-[PatientID]-[MonthYear]`
  - Example: `MONTHLY-001-OCT2025`

---

## 🔧 Configuration

### AI Settings

**Temperature:** 0.3 (factual, not creative)
**Model:** Llama 3.3 70B Versatile (via Groq)
**System Role:** "Fitness data analyst" (not "fitness coach")

**Key Prompt Instructions:**
- Use ONLY provided data
- DO NOT speculate or add filler text
- DO NOT invent progress
- Reference specific exercises, weights, reps
- If data missing, write "Not recorded"

### Notion Database Structure

Six interconnected databases:
1. **PATIENTS** - Patient information, medical history, current scores
2. **TRAINERS** - Trainer information
3. **WORKOUT LOGS** - Individual workout sessions
4. **WEEKLY LOGS** - Weekly summary reports
5. **MONTHLY LOGS** - Monthly summary reports
6. **ASSESSMENT LOGS** - Comprehensive assessments

See `RELATIONAL_DATABASE_GUIDE.md` for complete structure.

---

## 📖 Documentation

### Getting Started
- `README.md` (this file) - Project overview
- `SIMPLIFIED_APPROACH_SUMMARY.md` - Understanding the system approach
- `NOTION_DATABASE_SETUP_GUIDE.md` - Database setup instructions

### For Trainers
- `WORKOUT_LOG_CONVERSATION_CHECKLIST.md` - How to log workouts (5 min read)
- `STANDARDIZED_ASSESSMENT_TEMPLATE.md` - How to conduct assessments

### For Developers
- `RELATIONAL_DATABASE_GUIDE.md` - Database architecture
- `NAMING_CONVENTION_UPDATE_SUMMARY.md` - Naming standards
- `STANDARDIZATION_COMPLETE_SUMMARY.md` - Complete system documentation

### For Admins
- `MEDICAL_HISTORY_REHAB_TEMPLATE.md` - Medical tracking reference
- `ASSESSMENT_INTEGRATION_SUMMARY.md` - How assessments integrate with reports

---

## 🛡️ AI Hallucination Prevention

### The Problem
Traditional AI fitness reports often include:
- Motivational filler text not based on data
- Speculation about patient motivation
- Invented progress not recorded by trainers
- Generic "great job" statements

### Our Solution
1. **Temperature: 0.3** (not 0.7) - Less creative, more factual
2. **System Role:** "Data analyst" (not "motivational coach")
3. **Explicit Instructions:** "Use ONLY provided data, NO filler"
4. **Verification:** Compare AI output to source trainer notes

### Result
✅ Reports contain ONLY factual data from trainer observations
✅ Zero motivational language not stated by trainer
✅ Zero invented progress
✅ Legal protection through factual documentation

---

## 📈 Benefits

### Time Savings
- **Trainers:** 7-12 minutes saved per session (2-3 min logging vs 10-15 min forms)
- **Admins:** Automated report generation vs manual compilation
- **Patients:** Immediate access to factual progress reports

### Quality Improvements
- **Consistency:** Standardized assessments across all trainers
- **Accuracy:** Conversational logging captures details immediately
- **Compliance:** Proper medical documentation and incident tracking
- **Transparency:** 100% fact-based reports, no speculation

### Scalability
- Add unlimited trainers (no retraining needed - just chat with Claude)
- Add unlimited patients (automated report generation)
- Consistent quality regardless of team size

---

## 🔒 Security & Privacy

### Data Protection
- `.env` file excluded from git (contains API keys)
- HIPAA-sensitive medical information tracked
- Access controls recommended on Notion workspace
- Separate database option for detailed medical records

### Best Practices
- Only authorized trainers access medical fields
- Regular backup of Notion databases
- Secure API key storage
- Audit trail through Notion version history

---

## 🤝 Contributing

### Reporting Issues
If you find bugs or have suggestions, please open an issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

### Making Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add AmazingFeature'`)
6. Push to branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

---

## 📝 License

This project is intended for use by Stairs Gym and authorized partners. Please contact the repository owner for licensing information.

---

## 🙏 Acknowledgments

- **Notion API** - Database infrastructure
- **Groq** - AI inference (Llama 3.3 70B)
- **Claude Code** - Development assistance and conversational logging interface

---

## 📞 Support

For questions or support:
- Review the documentation in the `/docs` folder (all .md files)
- Check `SIMPLIFIED_APPROACH_SUMMARY.md` for system overview
- See `TROUBLESHOOTING.md` for common issues (if available)

---

## 🗺️ Roadmap

### Completed ✅
- [x] Notion database integration
- [x] AI-powered report generation (no hallucinations)
- [x] Conversational workout logging
- [x] Standardized assessment framework
- [x] Medical history and rehab tracking
- [x] Automated naming conventions
- [x] Assessment integration with patient records

### Future Enhancements 🔮
- [ ] WhatsApp/Email integration for report delivery
- [ ] Mobile app for trainers
- [ ] Photo/video capture for form analysis
- [ ] Progress charts and visualizations
- [ ] Multi-language support
- [ ] Client portal for self-service access

---

**Version:** 2.0 (Simplified Conversational Approach)
**Last Updated:** October 26, 2025
**Status:** Production Ready ✅
