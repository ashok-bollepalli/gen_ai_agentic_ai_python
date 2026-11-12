from review_tools import syntax_check, source_statistics, validate_source


def test_valid_syntax():
    assert syntax_check("def add(a, b):\n    return a + b\n")["valid"] is True


def test_invalid_syntax():
    result = syntax_check("def add(:\n    pass")
    assert result["valid"] is False
    assert result["error"]["line"] == 1


def test_source_statistics():
    result = source_statistics(
        "import os\n\nclass Example:\n    def run(self):\n        return 1\n"
    )
    assert result["line_count"] == 5
    assert result["class_count"] == 1
    assert result["function_count"] == 1
    assert result["import_count"] == 1


def test_empty_source_rejected():
    try:
        validate_source("  ")
    except ValueError:
        return
    assert False, "Expected ValueError"
