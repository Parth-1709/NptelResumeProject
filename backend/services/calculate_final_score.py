def calculate_final_score(
    skill_score: dict,
    experience_score: dict,
    project_score: dict,
    jd_skills: set,
    resume_skills: set,
    experience_skills: set,
    project_skills: set
) -> dict:
    total_score = (
        skill_score["score"]
        + experience_score["score"]
        + project_score["score"]
    )

    total_score = min(total_score, 100)

    missing_everywhere = (
        jd_skills
        - resume_skills
        - experience_skills
        - project_skills
    )

    match_level = "Low"
    if total_score >= 80:
        match_level = "High"
    elif total_score >= 50:
        match_level = "Medium"

    return {
        "final_score": total_score,
        "match_level": match_level,
        "breakdown": {
            "skills": skill_score,
            "experience": experience_score,
            "projects": project_score,
        },

        "skills_missing_everywhere": sorted(list(missing_everywhere))
    }
