from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from services.resume_parser import resume_parser
from services.section_splitter import section_splitter
from services.keywords_finder import extract_skills, extract_actions
from services.skills_scoring import skills_scoring
from services.experience_scoring import experience_scoring
from services.project_scoring import project_scoring
from services.calculate_final_score import calculate_final_score
from database import engine, get_db, Base
from models import User, Evaluation
from services.validators import validate_document_type, validate_safety_intent, validate_technical_signal
from pydantic import BaseModel
import json
from sqlalchemy import func

# ... (Load dotenv and App setup remain same) ...
load_dotenv()
# ... (Startup modifications remain same) ...
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserVerifyRequest(BaseModel):
    email: str
    name: str
# --- Endpoints ---

@app.post("/verify-user")
def verify_user(user: UserVerifyRequest, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            new_user = User(email=user.email, name=user.name, role="user")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {"role": new_user.role}
        return {"role": db_user.role}
    except Exception as e:
        print(f"DB Error (verify-user): {e}")
        # Fallback: Allow login as 'user' even if DB fails
        return {"role": "user"}


@app.get("/admin/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    user_count = db.query(User).count()
    
    # Calculate average score
    avg_score_result = db.query(func.avg(Evaluation.final_score)).scalar()
    avg_score = round(avg_score_result, 1) if avg_score_result else 0

    # Calculate top missing skills (This is a bit complex with comma-separated strings, but doable)
    # Ideally we'd fetch all and aggregate in python for simplicity with small data
    evaluations = db.query(Evaluation).all()
    skill_counts = {}
    for eval in evaluations:
        if eval.missing_skills:
            try:
                skills = json.loads(eval.missing_skills)
                for skill in skills:
                    skill_counts[skill] = skill_counts.get(skill, 0) + 1
            except:
                pass # Ignore parsing errors
    
    top_missing = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_missing_skills = [skill for skill, count in top_missing]

    return {
        "total_users": user_count,
        "avg_score": avg_score,
        "top_missing_skills": top_missing_skills if top_missing_skills else ["None yet"]
    }

@app.post("/evaluate")
async def evaluate_resume(
    jd_data: str = Form(...), 
    file: UploadFile = File(...), 
    email: str = Form(None), # Optional email
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported")

    # 1. Safety & Intent Filter on JD
    safety_error = validate_safety_intent(jd_data)
    if safety_error:
        return {
            "final_score": 0,
            "match_level": "Safety Violation",
            "score_breakdown": {
                "skills": 0,
                "experience": 0,
                "projects": 0
            },
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": [safety_error]
        }

    # 2. Technical Signal Validation on JD
    tech_error = validate_technical_signal(jd_data)
    if tech_error:
        return {
            "final_score": 0,
            "match_level": "Invalid Job Description",
            "score_breakdown": {
                "skills": 0,
                "experience": 0,
                "projects": 0
            },
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": [tech_error]
        }

    resume_content = await resume_parser(file)
    
    # 2. Document-Type Validation on Resume Content
    doc_type_error = validate_document_type(resume_content)
    if doc_type_error:
        return {
            "final_score": 0,
            "match_level": "Invalid Document Type",
            "score_breakdown": {
                "skills": 0,
                "experience": 0,
                "projects": 0
            },
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": [doc_type_error]
        }

    sections = section_splitter(resume_content)
    jd_skills = extract_skills(jd_data)

    skills_keywords = extract_skills(sections["skills"])

    experience_skills = extract_skills(sections["experience"])
    experience_actions = extract_actions(sections["experience"])

    projects_skills = extract_skills(sections["projects"])
    projects_actions = extract_actions(sections["projects"])

    skills_score = skills_scoring(skills_keywords, jd_skills)
    experience_score = experience_scoring(experience_skills, experience_actions, jd_skills)
    projects_score = project_scoring(projects_skills, projects_actions, jd_skills)
    final_score = calculate_final_score(skills_score, experience_score, projects_score, jd_skills, skills_keywords, experience_skills, projects_skills)
    
    # Save to Database
    try:
        missing_skills_json = json.dumps(final_score["skills_missing_everywhere"])
        new_eval = Evaluation(
            user_email=email,
            final_score=final_score["final_score"],
            missing_skills=missing_skills_json
        )
        db.add(new_eval)
        db.commit()
    except Exception as e:
        print(f"Failed to save evaluation: {e}")
        # Don't fail the request if saving stats fails, just log it.

    return {
        "final_score": final_score["final_score"],
        "match_level": final_score["match_level"], 
        "score_breakdown": {
            "skills": skills_score["score"],
            "experience": experience_score["score"],
            "projects": projects_score["score"]
        },
        "matched_skills": skills_score["matched_skills"],
        "missing_skills": final_score["skills_missing_everywhere"],
        "suggestions": generate_suggestions(
            final_score["final_score"],
            final_score["skills_missing_everywhere"]
        )
    }

def generate_suggestions(final_score: int, missing_skills: list) -> list:
    suggestions = []

    if final_score < 50:
        suggestions.append("Strengthen alignment with the job description by focusing on core required skills.")
    elif final_score < 70:
        suggestions.append("Good profile overall. Adding the missing skills can improve your match.")
    else:
        suggestions.append("Strong match for the role. Minor improvements can further strengthen your profile.")

    for skill in missing_skills:
        suggestions.append(f"Consider adding experience or projects demonstrating {skill}.")

    return suggestions
