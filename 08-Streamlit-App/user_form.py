
import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Student Registration",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Student Registration Form")
st.write("Fill in the details and click Submit.")

# 2. Create Form
with st.form("student_registration"):

    # Text Input
    name = st.text_input("Student Name")

    # Text Area
    address = st.text_area("Address")

    # Dropdown
    course = st.selectbox(
        "Select Course",
        ["Java", "Python", "Gen AI", "Data Science"]
    )

    # Multi-select Dropdown
    skills = st.multiselect(
        "Select Skills",
        ["Python", "Java", "SQL", "Machine Learning", "LangChain"]
    )

    # Radio Button
    gender = st.radio(
        "Select Gender",
        ["Male", "Female", "Other"],
        horizontal=True
    )

    # Checkbox
    terms = st.checkbox("I agree to the terms and conditions")

    # Date Picker
    joining_date = st.date_input("Expected Joining Date")

    # Submit Button
    submitted = st.form_submit_button(
        "Submit Registration",
        type="primary",
        use_container_width=True
    )

# 3. Process Form
if submitted:

    if not name.strip():
        st.error("Please enter your name.")

    elif not terms:
        st.warning("Please accept the terms and conditions.")

    else:
        # Spinner while processing
        with st.spinner("Processing registration..."):
            time.sleep(3)  # Simulate processing time

        st.success("Registration submitted successfully! 🎉")

        # 4. Display Submitted Data
        st.subheader("Registration Details")

        st.write("**Student Name:**", name)
        st.write("**Address:**", address)
        st.write("**Course:**", course)
        st.write("**Skills:**", ", ".join(skills) if skills else "None selected")
        st.write("**Gender:**", gender)
        st.write("**Terms Accepted:**", terms)
        st.write("**Joining Date:**", joining_date)
