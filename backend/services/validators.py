from fastapi import HTTPException
import re
from typing import Optional
from services.keywords_finder import TECH_SKILLS

def validate_document_type(text: str) -> Optional[str]:
    """
    Validates if the document appears to be a resume.
    Rejects content that looks like offer letters, huge certificates, or non-resume text.
    """
    text_lower = text.lower()
    
    # Signals of non-resume documents
    offer_letter_keywords = [
        "we are pleased to offer",
        "date of joining", 
        "salary breakdown",
        "acceptance of offer",
        "employment contract",
        "probation period"
    ]
    
    for phrase in offer_letter_keywords:
        if phrase in text_lower:
            return "Invalid Document Type. Looks like an offer letter or contract."

    # Assuming a resume must contain some basics (very loose check to be safe)
    # If it's completely empty or extremely short, might be invalid
    if len(text.strip()) < 50:
         return "Invalid Document. Content too short to be a resume."

    return None


def validate_safety_intent(text: str) -> Optional[str]:
    """
    Detects explicit illegal or harmful intent in job descriptions.
    Allows metaphorical 'killer', 'ninja' only when modifying a noun.
    """
    text_lower = text.lower()

    # 1. Illegal Intent - Immediate Rejection
    illegal_phrases = [
        "steal money",
        "hack bank", 
        "credit card theft",
        "evade taxes",
        "money laundering",
        "sell drugs",
        "harmful software",
        "malware distribution"
    ]
    
    for phrase in illegal_phrases:
        if phrase in text_lower:
            return "Safety Violation: Illegal or harmful content detected."

    # 2. Metaphorical vs Identity Check
    # "risky" words that are allowed ONLY if they modify a relevant noun
    risky_words = ["killer", "ninja", "rockstar", "pirate"]
    
    # Allowed contexts: word followed by specific professional nouns
    allowed_contexts = r"(developer|coder|programmer|engineer|manager|architect|designer|skill|feature|app|code|software)"
    
    # Pattern to find risky words
    # We look for the word, then check if it's followed by an allowed context.
    # If it is NOT followed by an allowed context, we trigger a violation (or check if it's an identity).
    
    for word in risky_words:
        # Find all occurrences of the word
        # Using word boundary \b to avoid matching inside other words
        matches = list(re.finditer(rf"\b{word}\b", text_lower))
        
        if not matches:
            continue

        # For each match, check context
        for match in matches:
            # Check if this specific instance is followed by an allowed noun "soon" (to account for maybe 'frontend __')
            # But specific requirement said: "modify a role or skill"
            
            # Let's check the immediate context (next word(s))
            # Create a small window after the word
            start_search = match.end()
            end_search = min(len(text_lower), start_search + 30) # Look ahead 30 chars
            next_chunk = text_lower[start_search:end_search]
            
            if re.match(rf"\s+{allowed_contexts}", next_chunk):
                continue # This usage is valid (e.g. "killer feature")
            
            # If not in allowed context, check if it's an identity phrase or noun usage that we want to reject
            # e.g. "is a killer", "looking for a ninja" (without specific role attached immediately?)
            
            # The rule: "Reject when such terms appear as nouns or identity-defining phrases"
            # "Reject ambiguous phrasing rather than attempting interpretation."
            
            # Simplest interpretation: If it's NOT explicitly "word noun", it's suspicious.
            # "ninja developer" -> OK
            # "python ninja" -> This is "noun word". The requirement said "modify a role". "python ninja" -> ninja modifies python? or ninja is the head noun? 
            # Usually "ninja" in "python ninja" acts as the noun signifying expertise. 
            # Wait, user said: "Ignore metaphorical adjectives ... when they modify a role or skill". 
            # "ninja developer" (ninja is adj). 
            # "python ninja" (ninja is noun). 
            # "Reject when such terms appear as nouns". 
            # So "python ninja" might be rejected under strict reading? 
            # User example: "developer who is a killer" -> Reject.
            # "killer code" -> "killer" modifies "code" -> OK.
            
            # Let's stick to the rule: Must match `(killer|ninja) (noun)` pattern to be safe.
            # If "python ninja" is common, maybe we should add it? 
            # But let's start strict as requested: "Prefer rejection over misinterpretation".
            
            return f"Safety Violation: Ambiguous or harmful use of '{word}'."

    return None


def validate_technical_signal(text: str) -> Optional[str]:
    """
    Checks if the JD contains any technical signal (keywords or general technical terms).
    Returns an error message if NO signal is found.
    """
    text_lower = text.lower()
    
    # 1. Check against specific Tech Skills (from keywords_finder)
    # Flatten the list of all aliases
    for aliases in TECH_SKILLS.values():
        for alias in aliases:
            if alias in text_lower:
                return None # Valid

    # 2. Check against General Technical Terms
    # These are broad terms that indicate a technical role even if specific stack isn't in our limited DB
    general_terms = [
        "software", "developer", "engineer", "devops", "architect", 
        "frontend", "backend", "fullstack", "mobile", "web", 
        "app", "application", "system", "database", "cloud", 
        "api", "server", "code", "programming", "coding", 
        "technical", "technology", "data", "algorithm", 
        "security", "network", "framework", "library", "tool"
    ]

    for term in general_terms:
        if term in text_lower:
            return None # Valid

    return "Invalid Job Description. No technical keywords or relevant terms found."

