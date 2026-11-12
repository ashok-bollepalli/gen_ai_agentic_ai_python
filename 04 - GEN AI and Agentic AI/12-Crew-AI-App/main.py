from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def generate_course_content(course_name):

    llm = LLM(
        model = "openai/gpt-6-astra",
        api_key = api_key
    )

    research_agent = Agent(
        role="Course Researcher",
        goal=(
            "Research the given course and identify important topics, "
            "student skills, and practical project ideas."
        ),
        backstory=(
            "You are an experienced technical course researcher."
        ),
        llm=llm,
        verbose=True
    )

    writer_agent = Agent(
        role="Course Content Writer",
        goal=(
            "Create simple, clear and student-friendly course content."
        ),
        backstory=(
            "You are an experienced educational content writer."
        ),
        llm=llm,
        verbose=True
    )

    research_task = Task(
        description=f"""
           Research the course: {course_name}

           Identify the following:

           1. Important topics students should learn
           2. Skills students will gain after completing the course
           3. Practical project ideas students can develop

           Keep the research simple and useful for students.

           Return the result in a structured format.
           """,

        expected_output="""
           A structured research report containing:
           - Important Topics
           - Student Skills
           - Project Ideas
           """,

        agent = research_agent
    )

    writing_task = Task(
        description=f"""
            Create course content for the course: {course_name}

            Use the research result produced by the Course Researcher.

            Prepare the following:

            1. Course Introduction
               - Explain what the course is
               - Explain why students should learn it

            2. Course Highlights
               - List the important topics
               - List the skills students will learn
               - Mention practical project ideas

            3. Final Student-Friendly Summary
               - Give a simple summary of the complete course
               - Explain what students will be able to do after
                 completing the course

            Use simple English.
            Make the content suitable for students.
            """,

        expected_output="""
            A complete student-friendly course document containing:

            COURSE INTRODUCTION

            COURSE HIGHLIGHTS

            IMPORTANT TOPICS

            SKILLS STUDENTS WILL LEARN

            PROJECT IDEAS

            FINAL STUDENT-FRIENDLY SUMMARY
            """,
            agent = writer_agent,
            context = [research_task]
    )

    crew = Crew(
        agents = [research_agent, writer_agent],
        tasks = [research_task, writing_task],
        process = Process.sequential,
        verbose = True
    )

    # execute multi agents
    result = crew.kickoff()

    return result