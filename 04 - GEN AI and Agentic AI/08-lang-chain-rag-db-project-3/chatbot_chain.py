from langchain_core.output_parsers import StrOutputParser

from db_service import search_courses

from rag_service import retrieve_documents

from prompt import get_student_prompt

from llm_provider import get_llm


# =========================================================
# LLM
# =========================================================

llm = get_llm()


# =========================================================
# PROMPT
# =========================================================

prompt = get_student_prompt()


# =========================================================
# FORMAT COURSE DATA
# =========================================================

def format_courses(courses):

    if not courses:

        return "No matching courses found."


    result = []


    for course in courses:

        result.append(

            f"""
Course Code: {course['course_code']}

Course Name: {course['course_name']}

Description: {course['description']}

Duration: {course['duration']}

Fee: ₹{course['fee']}

Eligibility: {course['eligibility']}

Mode: {course['mode']}
"""
        )


    return "\n".join(result)


# =========================================================
# COURSE DATABASE SEARCH
# =========================================================

def get_course_data(question):

    question_lower = question.lower()


    keywords = [

        "python",

        "data science",

        "generative ai",

        "artificial intelligence",

        "machine learning",

        "course",

        "courses",

        "fee",

        "fees",

        "price",

        "duration",

        "eligibility",

        "online",

        "classroom"
    ]


    found_keywords = []


    for keyword in keywords:

        if keyword in question_lower:

            found_keywords.append(
                keyword
            )


    # No course-related keyword
    if not found_keywords:

        return "No course database lookup required."


    courses = []


    for keyword in found_keywords:

        results = search_courses(
            keyword
        )

        courses.extend(results)


    # =====================================================
    # REMOVE DUPLICATE COURSES
    # =====================================================

    unique_courses = {}


    for course in courses:

        unique_courses[
            course["course_code"]
        ] = course


    courses = list(
        unique_courses.values()
    )


    return format_courses(
        courses
    )


# =========================================================
# RAG CONTEXT
# =========================================================

def get_rag_context(question):

    documents = retrieve_documents(
        question
    )


    if not documents:

        return "No relevant information found."


    context = []


    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown"
        )


        context.append(

            f"""
Source: {source}

{document.page_content}
"""
        )


    return "\n".join(context)


# =========================================================
# MAIN CHAT FUNCTION
# =========================================================

def ask_question(question):

    # -----------------------------------------------------
    # STEP 1: DATABASE CALL
    # -----------------------------------------------------

    course_data = get_course_data(question)


    # -----------------------------------------------------
    # STEP 2: RAG CALL
    # -----------------------------------------------------

    rag_context = get_rag_context(question)


    # -----------------------------------------------------
    # STEP 3: CREATE LANGCHAIN CHAIN
    # -----------------------------------------------------

    chain = ( prompt | llm |  StrOutputParser() )


    # -----------------------------------------------------
    # STEP 4: SEND DATA TO CHAIN and Execute that chain
    # -----------------------------------------------------

    answer = chain.invoke(

        {
            "course_data": course_data,
            "rag_context": rag_context,
            "question": question
        }
    )


    return answer