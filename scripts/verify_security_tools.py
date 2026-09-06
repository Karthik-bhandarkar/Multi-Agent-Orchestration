import json
import os
import sys
import time
from src.tools.safe_calculator import SafeMathParser

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = "logs/json_verification"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def verify_safe_calculator():
    calc = SafeMathParser()
    test_cases = [
        {"expr": "22 * 4 + 3", "type": "valid_arithmetic"},
        {"expr": "2 ** 10", "type": "valid_exponentiation"},
        {"expr": "(100 - 25) / 5", "type": "valid_parenthesis"},
        {"expr": "100 / 0", "type": "division_by_zero"},
        {"expr": "__import__('os').system('id')", "type": "rce_injection"},
        {"expr": "open('/etc/passwd').read()", "type": "file_read_injection"},
        {"expr": "lambda x: x+1", "type": "code_block_injection"},
    ]

    results = []
    for test in test_cases:
        expr = test["expr"]
        expr_type = test["type"]
        start_time = time.perf_counter()
        status = "SUCCESS"
        result_value = None
        error_message = None

        try:
            result_value = calc.evaluate(expr)
        except Exception as e:
            status = "BLOCKED_SECURITY" if "injection" in expr_type or "rce" in expr_type else "ERROR"
            error_message = str(e)

        latency_ms = (time.perf_counter() - start_time) * 1000

        results.append({
            "expression": expr,
            "category": expr_type,
            "status": status,
            "evaluated_result": result_value,
            "error_detail": error_message,
            "latency_ms": round(latency_ms, 4)
        })

    verification_data = {
        "component": "SafeMathParser (AST Security Calculator)",
        "total_tests": len(results),
        "test_results": results
    }

    output_path = os.path.join(OUTPUT_DIR, "security_calculator_verification.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(verification_data, f, indent=4)

    print("==================================================")
    print("SECURITY CALCULATOR AUTOMATED TEST RESULTS")
    print("==================================================")
    print(json.dumps(verification_data, indent=4))
    print(f"\nSaved verification JSON report to: {output_path}")
    print("==================================================")


if __name__ == "__main__":
    verify_safe_calculator()
