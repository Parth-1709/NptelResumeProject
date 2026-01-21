def experience_scoring(
    experience_skills: set,
    experience_actions: set,
    jd_skills: set,
    max_score: int = 25
) -> dict:
    if not experience_skills and not experience_actions:
        return {
            "score": 0,
            "matched_experience": [],
            "missing_experience": sorted(list(jd_skills)),
            "match_percentage": 0
        }

    base_score = 5
    action_bonus = 3 if experience_actions else 0
    if not jd_skills:
        return {
            "score": min(base_score + action_bonus, max_score),
            "matched_experience": [],
            "missing_experience": [],
            "match_percentage": 100
        }

    matched = experience_skills & jd_skills
    missing = jd_skills - matched

    usage_ratio = len(matched) / len(jd_skills)
    if usage_ratio == 0 and experience_actions:
        relevance_bonus = 2
    else:
        relevance_bonus = 0
    usage_score = round(
        usage_ratio * (max_score - base_score - action_bonus)
    )

    final_score = base_score + action_bonus + relevance_bonus + usage_score

    return {
        "score": min(final_score, max_score),
        "matched_experience": sorted(list(matched)),
        "missing_experience": sorted(list(missing)),
        "match_percentage": round(usage_ratio * 100, 2)
    }
