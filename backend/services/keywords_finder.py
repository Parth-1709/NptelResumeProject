from services.nlp_processor import preprocess

TECH_SKILLS = {
    "react": ["react", "reactjs", "react.js"],
    "nodejs": ["node", "nodejs"],
    "python": ["python"],
    "java": ["java"],
    "sql": ["sql"],
    "docker": ["docker"],
    "aws": ["aws"],
    "fastapi": ["fastapi"],
    "git": ["git"],
}

ACTION_VERBS = {
    "develop": ["develop"],
    "execute": ["execute"],
    "optimize": ["optimize"],
    "collaborate": ["collaborate"],
    "enhance": ["enhance"],
    "build": ["build"],
    "implement": ["implement"],
    "design": ["design"],
    "integrate": ["integrate"],
}


def extract_skills(text: str) -> set:
    tokens = preprocess(text)
    found = set()

    for canonical, aliases in TECH_SKILLS.items():
        if any(alias in tokens for alias in aliases):
            found.add(canonical)

    return found


def extract_actions(text: str) -> set:
    tokens = preprocess(text)
    found = set()

    for canonical, aliases in ACTION_VERBS.items():
        if any(alias in tokens for alias in aliases):
            found.add(canonical)

    return found
