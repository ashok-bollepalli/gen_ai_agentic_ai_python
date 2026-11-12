import streamlit as st
from main import generate_course_content


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Course Content Generator",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 35px;
}

.course-card {
    padding: 25px;
    border-radius: 15px;
    background-color: #f8f9fa;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🎓 AI Course Content Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Generate professional course content using CrewAI Multi-Agent System'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# INPUT SECTION
# ==========================================

st.markdown("### 📚 Course Details")

course_name = st.text_input(
    "Enter Course Name",
    placeholder="Example: Generative AI and Agentic AI"
)


# ==========================================
# GENERATE BUTTON
# ==========================================

generate_button = st.button(
    "🚀 Generate Course Content",
    use_container_width=True
)


# ==========================================
# GENERATE CONTENT
# ==========================================

if generate_button:

    if not course_name.strip():

        st.warning("Please enter a course name.")

    else:

        with st.spinner(
            "🤖 AI Agents are researching and creating course content..."
        ):

            try:

                result = generate_course_content(course_name)

                st.success(
                    "✅ Course content generated successfully!"
                )

                # ==================================
                # RESULT
                # ==================================

                st.markdown("## 📄 Generated Course Content")

                st.markdown(
                    '<div class="course-card">',
                    unsafe_allow_html=True
                )

                st.markdown(str(result))

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

                # ==================================
                # DOWNLOAD
                # ==================================

                st.download_button(
                    label="⬇️ Download Course Content",
                    data=str(result),
                    file_name=f"{course_name}_course_content.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"❌ Error while generating content: {str(e)}"
                )