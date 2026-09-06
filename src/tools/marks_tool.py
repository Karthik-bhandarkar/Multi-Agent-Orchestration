"""
EduPulse AI — LangChain Student Marks Inspection Tool
Exposes a thread-safe database lookup tool for LangChain multi-agent orchestration.
"""

from langchain_core.tools import tool
from src.db.student_repository import StudentRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


@tool
def student_marks_tool(roll_no: str) -> str:
    """
    Looks up student academic performance, subject marks, and pass/fail summary from the SQLite database.

    Args:
        roll_no (str): The roll number of the student (e.g., '101', '102', '103', '104').

    Returns:
        str: Formatted text summary of student academic records or error message.
    """
    clean_roll = str(roll_no).strip()
    if not clean_roll:
        return "Error: Roll number cannot be empty."

    try:
        with StudentRepository() as repo:
            summary = repo.get_student_summary(clean_roll)
            if "error" in summary:
                return f"No student found with Roll Number '{clean_roll}'."

            marks_list = repo.get_student_marks(clean_roll)

        name = summary.get("student_name", "Unknown")
        avg_score = summary.get("avg_score", 0.0)
        avg_attendance = summary.get("avg_attendance", 0.0)
        status = summary.get("status", "FAIL")

        marks_detail = "\n".join(
            [f"  - {item['subject']}: {item['score']}/100 (Attendance: {item['attendance_percentage']}%)" for item in marks_list]
        )

        result_str = (
            f"Student Summary for Roll No {clean_roll}:\n"
            f"• Name: {name}\n"
            f"• Average Score: {avg_score:.2f}\n"
            f"• Average Attendance: {avg_attendance:.2f}%\n"
            f"• Overall Status: {status}\n"
            f"• Subject Breakdown:\n{marks_detail}"
        )

        logger.info(f"student_marks_tool executed successfully for roll_no={clean_roll}")
        return result_str

    except Exception as e:
        logger.error(f"Error in student_marks_tool for roll_no={clean_roll}: {str(e)}")
        return f"Error querying database for roll number {clean_roll}: {str(e)}"
