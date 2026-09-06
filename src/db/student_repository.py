import sqlite3
import sys
from src.core.config import settings
from src.utils.logger import get_logger
from src.utils.exception import CustomException

logger = get_logger(__name__)


class StudentRepository:
    """
    Thread-safe, context-managed SQLite repository.
    Usage:
        with StudentRepository() as repo:
            rows = repo.get_student_marks("102")
    """

    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.DB_PATH
        self.conn: sqlite3.Connection | None = None

    def __enter__(self) -> "StudentRepository":
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON;")
            return self
        except Exception as e:
            raise CustomException(e, sys) from e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
                logger.error(f"Transaction rolled back due to: {exc_val}")
            self.conn.close()
        return False

    def get_student_marks(self, roll_no: str) -> list[dict]:
        """
        Parameterized INNER JOIN across students -> marks -> subjects.
        """
        try:
            query = """
                SELECT sub.name AS subject,
                       m.score AS score,
                       m.attendance_percentage AS attendance_percentage
                FROM students s
                INNER JOIN marks m ON s.student_id = m.student_id
                INNER JOIN subjects sub ON sub.subject_id = m.subject_id
                WHERE s.roll_no = ?
                ORDER BY sub.name;
            """
            cursor = self.conn.execute(query, (roll_no,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_student_summary(self, roll_no: str) -> dict:
        """
        GROUP BY aggregation: average score, average attendance, pass/fail.
        """
        try:
            query = """
                SELECT s.name AS student_name,
                       s.roll_no AS roll_no,
                       AVG(m.score) AS avg_score,
                       AVG(m.attendance_percentage) AS avg_attendance,
                       COUNT(m.mark_id) AS subjects_count
                FROM students s
                INNER JOIN marks m ON s.student_id = m.student_id
                WHERE s.roll_no = ?
                GROUP BY s.student_id;
            """
            cursor = self.conn.execute(query, (roll_no,))
            row = cursor.fetchone()

            if row is None:
                return {"error": f"No records found for roll_no {roll_no}"}

            summary = dict(row)
            summary["status"] = "PASS" if summary["avg_score"] > 40 else "FAIL"
            return summary
        except Exception as e:
            raise CustomException(e, sys) from e

    def student_exists(self, roll_no: str) -> bool:
        """Utility check used by agents before running expensive queries."""
        try:
            cursor = self.conn.execute(
                "SELECT 1 FROM students WHERE roll_no = ? LIMIT 1;", (roll_no,)
            )
            return cursor.fetchone() is not None
        except Exception as e:
            raise CustomException(e, sys) from e
