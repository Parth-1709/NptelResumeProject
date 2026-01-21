def section_splitter(resume_content: str) -> dict:
    sections = {
        "skills": "",
        "education": "",
        "experience": "",
        "projects": "",
    }

    current_section = None
    lines = resume_content.split("\n")

    for line in lines:
        clean_line = line.strip().lower()

        if clean_line in ["skills", "technical skills", "skill set"]:
            current_section = "skills"
            continue
        elif clean_line in ["education", "academic background"]:
            current_section = "education"
            continue
        elif clean_line in ["experience", "work experience", "internships"]:
            current_section = "experience"
            continue
        elif clean_line in ["projects", "personal projects"]:
            current_section = "projects"
            continue
        elif clean_line in ["keywords"]:
            current_section = "keywords"
            continue

        if current_section:
            sections[current_section] += line + "\n"

    return sections
