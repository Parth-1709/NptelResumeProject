def project_scoring(
    project_skills: set,
    project_actions: set,
    jd_skills: set,
    max_score: int = 15
) -> dict:
    if not project_skills and not project_actions:
        return {
            "score": 0,
            "matched_projects": [],
            "missing_projects": sorted(list(jd_skills)),
            "match_percentage": 0
        }

    base_score = 3
    action_bonus = 2 if project_actions else 0

    if not jd_skills:
        return {
            "score": min(base_score + action_bonus, max_score),
            "matched_projects": [],
            "missing_projects": [],
            "match_percentage": 100
        }

    matched = project_skills & jd_skills
    missing = jd_skills - matched

    usage_ratio = len(matched) / len(jd_skills)
    usage_score = round(
        usage_ratio * (max_score - base_score - action_bonus)
    )

    final_score = base_score + action_bonus + usage_score

    return {
        "score": min(final_score, max_score),
        "matched_projects": sorted(list(matched)),
        "missing_projects": sorted(list(missing)),
        "match_percentage": round(usage_ratio * 100, 2)
    }
