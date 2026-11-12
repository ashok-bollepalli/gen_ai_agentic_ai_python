import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

MAX_SOURCE_CHARS = 40_000


def validate_source(source: str) -> None:
    if not source or not source.strip():
        raise ValueError("Source code cannot be empty.")
    if len(source) > MAX_SOURCE_CHARS:
        raise ValueError(f"Source code exceeds {MAX_SOURCE_CHARS} characters.")


def syntax_check(source: str) -> dict[str, Any]:
    """Parse source as Python without executing it."""
    try:
        ast.parse(source)
        return {"valid": True, "error": None}
    except SyntaxError as exc:
        return {
            "valid": False,
            "error": {
                "message": exc.msg,
                "line": exc.lineno,
                "offset": exc.offset,
                "text": exc.text,
            },
        }


def _run_static_tool(command: list[str], source: str, timeout: int = 12) -> dict[str, Any]:
    """Run a linter/scanner against a temporary source file; never execute the submitted code."""
    with tempfile.TemporaryDirectory(prefix="ai_code_review_") as temp_dir:
        source_path = Path(temp_dir) / "submitted_code.py"
        source_path.write_text(source, encoding="utf-8")
        full_command = [*command, str(source_path)]
        try:
            completed = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                shell=False,
            )
            return {
                "returncode": completed.returncode,
                "stdout": completed.stdout[:12000],
                "stderr": completed.stderr[:4000],
            }
        except FileNotFoundError:
            return {"unavailable": True, "message": f"Tool not installed: {command[0]}"}
        except subprocess.TimeoutExpired:
            return {"timeout": True, "message": f"{command[0]} timed out"}




def static_analysis(source: str) -> dict[str, Any]:
    validate_source(source)
    syntax = syntax_check(source)
    if not syntax["valid"]:
        return {
            "syntax": syntax,
            "ruff": {"skipped": "Fix Python syntax errors first."},
            "bandit": {"skipped": "Fix Python syntax errors first."},
        }

    ruff = _run_static_tool(
        [sys.executable, "-m", "ruff", "check", "--output-format=json"],
        source,
    )
    bandit = _run_static_tool(
        [sys.executable, "-m", "bandit", "-f", "json", "-q"],
        source,
    )

    ruff_items = []
    if not ruff.get("unavailable") and not ruff.get("timeout"):
        try:
            ruff_items = json.loads(ruff.get("stdout") or "[]")
        except json.JSONDecodeError:
            pass

    bandit_items = []
    if not bandit.get("unavailable") and not bandit.get("timeout"):
        try:
            bandit_items = json.loads(
                bandit.get("stdout") or "{}"
            ).get("results", [])
        except json.JSONDecodeError:
            pass

    return {
        "syntax": syntax,
        "ruff": {
            "available": not ruff.get("unavailable", False),
            "issues": [
                {
                    "code": item.get("code"),
                    "message": item.get("message"),
                    "line": item.get("location", {}).get("row"),
                    "fixable": bool(item.get("fix")),
                }
                for item in ruff_items
            ],
            "tool_message": ruff.get("message") or ruff.get("stderr"),
        },
        "bandit": {
            "available": not bandit.get("unavailable", False),
            "issues": [
                {
                    "test_id": item.get("test_id"),
                    "test_name": item.get("test_name"),
                    "severity": item.get("issue_severity"),
                    "confidence": item.get("issue_confidence"),
                    "line": item.get("line_number"),
                    "message": item.get("issue_text"),
                }
                for item in bandit_items
            ],
            "tool_message": bandit.get("message") or bandit.get("stderr"),
        },
    }


def source_statistics(source: str) -> dict[str, Any]:
    validate_source(source)
    syntax = syntax_check(source)
    result = {
        "line_count": len(source.splitlines()),
        "character_count": len(source),
        "syntax": syntax,
        "function_count": 0,
        "class_count": 0,
        "import_count": 0,
    }
    if syntax["valid"]:
        tree = ast.parse(source)
        result["function_count"] = sum(
            isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            for n in ast.walk(tree)
        )
        result["class_count"] = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
        result["import_count"] = sum(
            isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree)
        )
    return result
