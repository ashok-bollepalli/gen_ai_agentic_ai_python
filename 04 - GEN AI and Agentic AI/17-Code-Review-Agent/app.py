import json
import streamlit as st

from agent import review_code
from review_tools import source_statistics, static_analysis

st.set_page_config(page_title="AI Code Review Agent", page_icon="🧑‍💻", layout="wide")
st.title("🧑‍💻 AI Code Review & Developer Assistant")
st.write("Review Python code for likely bugs, security risks, quality issues, and missing tests.")

uploaded = st.file_uploader("Upload a Python file (.py)", type=["py"])
default_code = """def average(values):
    return sum(values) / len(values)

print(average([10, 20, 30]))
"""

source = default_code
if uploaded:
    try:
        source = uploaded.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        st.error("The file must be UTF-8 encoded.")
        st.stop()

source = st.text_area("Python source code", value=source, height=320)

col1, col2 = st.columns([1, 3])
with col1:
    run_review = st.button("Run full AI review", type="primary")
with col2:
    st.caption("Submitted code is analyzed as text; this app does not execute it.")

if run_review:
    if not source.strip():
        st.error("Paste or upload source code first.")
        st.stop()

    with st.spinner("Running static checks and AI review..."):
        try:
            report = review_code(source)
            st.session_state["report"] = report
        except Exception as exc:
            st.error("Review failed. Check the API key, model configuration, and server logs.")
            print(f"Review error: {exc}")

report = st.session_state.get("report")
if report:
    st.subheader("Review Summary")
    st.write(report["summary"])

    stats = report["statistics"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Lines", stats["line_count"])
    c2.metric("Functions", stats["function_count"])
    c3.metric("Classes", stats["class_count"])
    c4.metric("Imports", stats["import_count"])

    st.subheader("Findings")
    findings = report.get("findings", [])
    if not findings:
        st.success("The AI reviewer did not report findings. This does not prove the code is defect-free.")
    for finding in findings:
        severity = finding.get("severity", "info").upper()
        title = finding.get("title", "Finding")
        line = finding.get("line")
        location = f" — line {line}" if line else ""
        with st.expander(f"[{severity}] {title}{location}", expanded=True):
            st.write(finding.get("explanation", ""))
            st.write("**Recommendation:**", finding.get("recommendation", ""))
            if finding.get("evidence"):
                st.code(finding["evidence"])

    with st.expander("Static analysis results"):
        st.json(report["static_analysis"])

    with st.expander("Strengths and assumptions"):
        st.write("**Strengths**")
        st.write(report.get("strengths", []))
        st.write("**Assumptions**")
        st.write(report.get("assumptions", []))

    tests = report.get("test_suggestions", {})
    st.subheader("Suggested Pytest Tests")
    st.write(tests.get("testing_notes", []))
    test_code = tests.get("pytest_code", "")
    st.code(test_code, language="python")
    st.download_button(
        "Download suggested tests",
        data=test_code,
        file_name="test_suggested.py",
        mime="text/x-python",
    )

    report_json = json.dumps(report, indent=2, ensure_ascii=False)
    st.download_button(
        "Download full review report (JSON)",
        data=report_json,
        file_name="code_review_report.json",
        mime="application/json",
    )
    st.info(report["disclaimer"])
