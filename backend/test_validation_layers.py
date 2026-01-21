from services.validators import validate_document_type, validate_safety_intent
from fastapi import HTTPException
import traceback

def run_tests():
    print("Running Validation Layer Tests...\n")
    
    # --- Check 1: Document Type Validation ---
    print("--- Document Type Tests ---")
    
    valid_resume = "this is a software engineer resume with skills in python and java."
    try:
        validate_document_type(valid_resume)
        print("[PASS] Accepted valid resume text")
    except Exception as e:
        print(f"[FAIL] Rejected valid resume: {e}")

    offer_letter = "We are pleased to offer you the position of Senior Developer. Date of joining is..."
    try:
        validate_document_type(offer_letter)
        print("[FAIL] Accepted offer letter")
    except HTTPException:
        print("[PASS] Rejected offer letter")
    except Exception as e:
        print(f"[FAIL] Unexpected error on offer letter: {e}")

    employment_contract = "This employment contract is between Company X and..."
    try:
        validate_document_type(employment_contract)
        print("[FAIL] Accepted employment contract")
    except HTTPException:
        print("[PASS] Rejected employment contract")

    short_text = "hi"
    try:
        validate_document_type(short_text)
        print("[FAIL] Accepted short text")
    except HTTPException:
        print("[PASS] Rejected short text")


    # --- Check 2: Safety & Intent Filter ---
    print("\n--- Safety & Intent Tests ---")

    valid_jd = "looking for a software engineer with python skills."
    try:
        validate_safety_intent(valid_jd)
        print("[PASS] Accepted valid JD")
    except Exception as e:
        print(f"[FAIL] Rejected valid JD: {e}")

    illegal_intent = "we need someone to hack bank accounts and steal money."
    try:
        validate_safety_intent(illegal_intent)
        print("[FAIL] Accepted illegal intent")
    except HTTPException:
        print("[PASS] Rejected illegal intent")

    
    # Metaphorical vs Identity Tests
    
    # 1. Metaphorical adjective modifying a role/skill -> Should PASS
    metaphor_valid_1 = "looking for a killer developer for our team"
    try:
        validate_safety_intent(metaphor_valid_1)
        print(f"[PASS] Accepted '{metaphor_valid_1}'")
    except Exception as e:
        print(f"[FAIL] Rejected '{metaphor_valid_1}': {e}")

    metaphor_valid_2 = "we need a ninja coder for this project"
    try:
        validate_safety_intent(metaphor_valid_2)
        print(f"[PASS] Accepted '{metaphor_valid_2}'")
    except Exception as e:
        print(f"[FAIL] Rejected '{metaphor_valid_2}': {e}")
        
    metaphor_valid_3 = "must have killer skills in python"
    try:
        validate_safety_intent(metaphor_valid_3)
        print(f"[PASS] Accepted '{metaphor_valid_3}'")
    except Exception as e:
        print(f"[FAIL] Rejected '{metaphor_valid_3}': {e}")

    # 2. Identity/Noun usage -> Should REJECT
    metaphor_invalid_1 = "looking for a killer to join us"
    try:
        validate_safety_intent(metaphor_invalid_1)
        print(f"[FAIL] Accepted '{metaphor_invalid_1}'")
    except HTTPException:
        print(f"[PASS] Rejected '{metaphor_invalid_1}'")
        
    metaphor_invalid_2 = "we are hiring a ninja." # ambiguous
    try:
        validate_safety_intent(metaphor_invalid_2)
        print(f"[FAIL] Accepted '{metaphor_invalid_2}'")
    except HTTPException:
        print(f"[PASS] Rejected '{metaphor_invalid_2}'")

    metaphor_invalid_3 = "developer who is a killer"
    try:
        validate_safety_intent(metaphor_invalid_3)
        print(f"[FAIL] Accepted '{metaphor_invalid_3}'")
    except HTTPException:
        print(f"[PASS] Rejected '{metaphor_invalid_3}'")


if __name__ == "__main__":
    run_tests()
