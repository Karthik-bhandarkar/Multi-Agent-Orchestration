import pytest
import time
from src.db.student_repository import StudentRepository
from src.db.init_db import initialize_database


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    initialize_database()


class TestStudentQueries:
    def test_get_marks_valid_roll_no(self):
        with StudentRepository() as repo:
            marks = repo.get_student_marks("102")
        assert len(marks) == 4
        assert all("subject" in m and "score" in m for m in marks)

    def test_get_marks_invalid_roll_no_returns_empty(self):
        with StudentRepository() as repo:
            marks = repo.get_student_marks("999")
        assert marks == []

    def test_get_summary_pass_status(self):
        with StudentRepository() as repo:
            summary = repo.get_student_summary("103")
        assert summary["status"] == "PASS"
        assert summary["avg_score"] > 40

    def test_get_summary_fail_status(self):
        with StudentRepository() as repo:
            summary = repo.get_student_summary("104")
        assert summary["status"] == "FAIL"

    def test_student_exists(self):
        with StudentRepository() as repo:
            assert repo.student_exists("102") is True
            assert repo.student_exists("000") is False


class TestSQLInjectionSafety:
    def test_injection_attempt_returns_empty(self):
        with StudentRepository() as repo:
            malicious = repo.get_student_marks("102' OR '1'='1")
        assert malicious == []

    def test_injection_drop_table_attempt(self):
        with StudentRepository() as repo:
            repo.get_student_marks("102'; DROP TABLE students; --")
        with StudentRepository() as repo:
            assert repo.student_exists("102") is True


class TestConnectionLifecycle:
    def test_connection_closes_after_context(self):
        repo = StudentRepository()
        with repo:
            pass
        with pytest.raises(Exception):
            repo.conn.execute("SELECT 1;")

    def test_rollback_on_exception(self):
        with pytest.raises(ZeroDivisionError):
            with StudentRepository() as repo:
                repo.get_student_marks("102")
                raise ZeroDivisionError("forced error for rollback test")


class TestPerformance:
    def test_query_latency_under_5ms(self):
        with StudentRepository() as repo:
            start = time.perf_counter()
            repo.get_student_marks("102")
            elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"\n[BENCHMARK] SQL query latency: {elapsed_ms:.3f} ms")
        assert elapsed_ms < 5.0
