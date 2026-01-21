def skills_scoring(resume_skills: set, jd_skills: set, max_score: int = 60) -> dict:
   
    if not jd_skills:
        return {
            "score": max_score,
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": 100
        }

    if not resume_skills:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": sorted(list(jd_skills)),
            "match_percentage": 0
        }

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    match_ratio = len(matched) / len(jd_skills)
    score = round(match_ratio * max_score)

    return {
        "score": score,
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
        "match_percentage": round(match_ratio * 100, 2)
    }
