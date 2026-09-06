"""
EduPulse AI — Pytest Suite for Security Tools & Guardrails
Validates AST arithmetic evaluator, sub-5ms crisis guardrail latency, and LangChain SQL marks tool.
"""

import time
import pytest
from src.tools.safe_calculator import SafeMathParser
from src.tools.safety_guardrail import check_crisis
from src.tools.marks_tool import student_marks_tool


class TestSafeCalculator:
    def setup_method(self):
        self.parser = SafeMathParser()

    def test_basic_arithmetic(self):
        assert self.parser.evaluate("10 + 20") == 30
        assert self.parser.evaluate("100 - 45") == 55
        assert self.parser.evaluate("12 * 5") == 60
        assert self.parser.evaluate("50 / 2") == 25.0
        assert self.parser.evaluate("2 ** 3") == 8

    def test_operator_precedence(self):
        assert self.parser.evaluate("2 + 3 * 4") == 14

    def test_zero_division_safety(self):
        with pytest.raises(ValueError, match="Division by zero"):
            self.parser.evaluate("10 / 0")

    def test_rce_prevention_import(self):
        with pytest.raises(ValueError, match="Security Block"):
            self.parser.evaluate("__import__('os').system('dir')")

    def test_rce_prevention_function_call(self):
        with pytest.raises(ValueError, match="Security Block"):
            self.parser.evaluate("eval('1 + 1')")


class TestSafetyGuardrail:
    def test_crisis_suicide_detection(self):
        res = check_crisis("I feel so overwhelmed and I want to die")
        assert res is not None
        assert res["is_crisis"] is True
        assert res["risk_category"] == "suicide"
        assert "helplines" in res

    def test_crisis_self_harm_detection(self):
        res = check_crisis("I feel terrible and I want to harm myself tonight")
        assert res is not None
        assert res["is_crisis"] is True
        assert res["risk_category"] == "self_harm"

    def test_safe_academic_input_no_crisis(self):
        res = check_crisis("Can you help me calculate my math scores and GPA?")
        assert res is None

    def test_word_boundary_false_positive_safety(self):
        res = check_crisis("I am following a healthy diet plan for my exam preparation")
        assert res is None

    def test_crisis_detection_performance_under_5ms(self):
        start = time.perf_counter()
        _ = check_crisis("I am feeling hopeless and want to end my life")
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert elapsed_ms < 5.0, f"Guardrail latency exceeded threshold: {elapsed_ms:.3f}ms"


class TestMarksTool:
    def test_marks_tool_valid_roll_no(self):
        output = student_marks_tool.invoke({"roll_no": "102"})
        assert "Student Summary for Roll No 102" in output
        assert "Aarav Sharma" in output
        assert "Data Structures" in output

    def test_marks_tool_invalid_roll_no(self):
        output = student_marks_tool.invoke({"roll_no": "99999"})
        assert "No student found" in output
