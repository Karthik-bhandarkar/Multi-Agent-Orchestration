import json
import os
import sys
from src.db.init_db import initialize_database
from src.db.student_repository import StudentRepository
from src.core.config import settings

# Ensure UTF-8 output stream encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = "logs/json_verification"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_manual_verification():
    print("==================================================")
    print("EDUPULSE AI - MANUAL SYSTEM VERIFICATION RUNNER")
    print("==================================================")

    # 1. Initialize Database
    print("\n[STEP 1] Initializing SQLite Database...")
    initialize_database()
    print(f"SUCCESS: Database created at: {settings.DB_PATH}")

    # 2. Query Student Repository
    print("\n[STEP 2] Querying StudentRepository Records...")
    with StudentRepository() as repo:
        marks_102 = repo.get_student_marks("102")
        summary_102 = repo.get_student_summary("102")
        summary_103 = repo.get_student_summary("103")
        summary_104 = repo.get_student_summary("104")
        exists_102 = repo.student_exists("102")

    # 3. Format Answers into JSON Verification Structure
    verification_data = {
        "database_path": settings.DB_PATH,
        "student_102": {
            "exists": exists_102,
            "marks": marks_102,
            "summary": summary_102,
        },
        "student_103_summary": summary_103,
        "student_104_summary": summary_104,
    }

    # 4. Save to JSON File
    output_file = os.path.join(OUTPUT_DIR, "manual_verification_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(verification_data, f, indent=4)

    print(f"\nSUCCESS: JSON Verification Results saved to: {output_file}")
    print("\nJSON Content Preview:")
    print(json.dumps(verification_data, indent=4))
    print("\n==================================================")


if __name__ == "__main__":
    run_manual_verification()
