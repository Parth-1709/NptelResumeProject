# AI-Assisted Resume Evaluator (ATS-Style Scoring System)

A web-based **ATS-style resume evaluation system** that analyzes a candidate’s resume against a given job description and generates a **transparent, explainable compatibility score** with actionable improvement suggestions.

This project was developed as part of an **NPTEL Internship** and focuses on **deterministic scoring logic** rather than black-box decision making.

---

## 🌐 Live Application

🔗 **App Link:** https://nptel-resume-project.vercel.app/

---

## 🚀 Features

- Upload resumes in **PDF format**
- Paste or enter a **job description**
- Automatic extraction of:
  - Skills
  - Keywords
  - Experience indicators
- **ATS compatibility score (out of 100)**
- Section-wise score breakdown
- Identification of **missing or weak skills**
- Clear, actionable resume improvement suggestions
- Input validation for invalid or irrelevant job descriptions

---

## 🏗️ System Overview

The system follows a modular architecture:
- **Frontend:** Resume upload, job description input, result visualization  
- **Backend:** FastAPI-based APIs for processing and evaluation  
- **NLP Engine:** Rule-based and NLP-assisted skill and keyword extraction  
- **Scoring Engine:** Deterministic ATS-style scoring logic

---

## 🧠 Scoring Logic (High Level)

The final ATS score is computed using weighted components:
- Skill Match
- Keyword Relevance
- Experience Alignment
- Resume Structure

This ensures **consistency, transparency, and explainability** in evaluation.

---

## 🛠️ Technologies Used

- **Backend:** Python, FastAPI  
- **NLP:** spaCy, Regular Expressions  
- **Frontend:** React / Next.js  
- **Database:** PostgreSQL / SQLite (optional)  
- **Deployment:** Vercel, Render  

---

## 📸 Screenshots

> Add screenshots inside the `screenshots/` folder and update the links below.

### Resume Upload and Job Description Input
<!-- Replace upload.png with your actual screenshot -->
![Resume Upload Interface](<img width="1365" height="858" alt="Screenshot 2026-01-28 123906" src="https://github.com/user-attachments/assets/e6724a41-1936-4f71-9223-68ae4e6fa749" />
)

---

### ATS Score and Section-wise Breakdown
<!-- Replace score.png with your actual screenshot -->
![ATS Score Output](<img width="1145" height="879" alt="Screenshot 2026-01-28 124532" src="https://github.com/user-attachments/assets/36b05cf7-b097-488c-aa8a-ed5691721596" />
)

---

### Administrative Dashboard
<!-- Include only if admin dashboard shows aggregate insights -->
![Admin Dashboard](<img width="817" height="274" alt="image" src="https://github.com/user-attachments/assets/f6a347c6-b16c-45ef-b08b-4de6fd32cfe8" />
)

---

## 🧪 Testing

The application was tested using multiple resumes and job descriptions with different formats and skill sets.  
Edge cases such as missing resume sections and invalid job descriptions were handled gracefully.

---

## 📌 Use Cases

- Students preparing resumes for internships and full-time roles  
- Career cells for evaluating candidate readiness  
- Educational demonstration of ATS-style resume screening systems  

---

## 📄 Internship Details

- **Program:** NPTEL Internship  
- **Duration:** 4 Weeks (5 January – 1 February)  
- **Project Type:** Individual Project  

---

## 📎 Repository

🔗 https://github.com/Parth-1709/NptelResumeProject

---

## 📜 License

This project is developed for academic and educational purposes.
