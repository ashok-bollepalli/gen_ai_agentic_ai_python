import streamlit as st

from db_service import (
    initialize_database,
    get_all_courses
)

from chatbot_chain import ask_question
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(

    page_title="Gen AI Student Assistant",

    page_icon="🎓",

    layout="wide"
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

initialize_database()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {

        font-size: 38px;

        font-weight: 700;

        color: #4F46E5;

        text-align: center;

        margin-bottom: 5px;
    }


    .subtitle {

        text-align: center;

        color: #6B7280;

        margin-bottom: 30px;
    }


    .course-card {

        background-color: #F8FAFC;

        padding: 15px;

        border-radius: 10px;

        margin-bottom: 10px;

        border: 1px solid #E5E7EB;
    }


    </style>
    """,

    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎓 Student Assistant")


    st.write(
        "Gen AI powered academic chatbot"
    )


    st.divider()


    # -----------------------------------------------------
    # COURSE LIST
    # -----------------------------------------------------

    st.subheader("📚 Available Courses")


    courses = get_all_courses()


    for course in courses:

        st.markdown(

            f"""
            <div class="course-card">

            <b>{course['course_code']}</b>

            <br>

            {course['course_name']}

            <br><br>

            💰 ₹{course['fee']}

            <br>

            ⏱️ {course['duration']}

            </div>
            """,

            unsafe_allow_html=True
        )


    st.divider()


    # -----------------------------------------------------
    # EXAMPLE QUESTIONS
    # -----------------------------------------------------

    st.subheader(
        "💡 Example Questions"
    )


    examples = [

        "What courses are available?",

        "What is the fee for Python?",

        "How long is Data Science?",

        "What is the attendance policy?",

        "What topics are covered in AI?",

        "What are the eligibility requirements?"
    ]


    for example in examples:

        if st.button(

            example,

            use_container_width=True
        ):

            st.session_state[
                "selected_question"
            ] = example


    st.divider()


    # -----------------------------------------------------
    # CLEAR CHAT
    # -----------------------------------------------------

    if st.button(

        "🗑️ Clear Chat",

        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.markdown(

    """
    <div class="main-title">

        🎓 Gen AI Student Assistant

    </div>

    <div class="subtitle">

        Ask questions about courses,
        fees, syllabus, eligibility
        and institute policies.

    </div>
    """,

    unsafe_allow_html=True
)


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# USER INPUT
# =========================================================

question = st.chat_input(

    "Ask your question..."
)


# =========================================================
# SIDEBAR QUESTION
# =========================================================

if "selected_question" in st.session_state:

    question = st.session_state.pop(
        "selected_question"
    )


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # -----------------------------------------------------
    # DISPLAY USER QUESTION
    # -----------------------------------------------------

    st.session_state.messages.append(

        {
            "role": "user",

            "content": question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)


    # -----------------------------------------------------
    # GET AI RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            try:

                answer = ask_question(
                    question
                )


            except Exception as e:

                answer = (

                    "❌ Sorry, something went wrong.\n\n"

                    f"Error: {str(e)}"
                )


        st.markdown(answer)


    # -----------------------------------------------------
    # SAVE AI RESPONSE
    # -----------------------------------------------------

    st.session_state.messages.append(

        {
            "role": "assistant",

            "content": answer
        }
    )
