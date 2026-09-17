# ============================================================
# COURSE CONTENT GENERATOR - MULTI AGENT SYSTEM
# Using CrewAI
# ============================================================

from crewai import Agent, Task, Crew, Process


# ============================================================
# 1. GET COURSE NAME FROM USER
# ============================================================

course_name = input("Enter Course Name: ")


# ============================================================
# 2. CREATE COURSE RESEARCHER AGENT
# ============================================================

researcher = Agent(
    role="Course Researcher",
    
    goal="Research the given course and identify important topics, "
         "student skills, and practical project ideas.",
    
    backstory="You are an experienced technical course researcher. "
              "You analyze a course and identify the most important "
              "topics that students should learn.",
    
    verbose=True
)


# ============================================================
# 3. CREATE CONTENT WRITER AGENT
# ============================================================

writer = Agent(
    role="Course Content Writer",
    
    goal="Create simple, clear and student-friendly course content "
         "using the research provided by the Course Researcher.",
    
    backstory="You are an experienced educational content writer. "
              "You convert technical research into simple content "
              "that students can easily understand.",
    
    verbose=True
)


# ============================================================
# 4. RESEARCH TASK
# ============================================================

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
    
    agent=researcher
)


# ============================================================
# 5. CONTENT WRITING TASK
# ============================================================

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
    
    agent=writer,
    context=[research_task]
)


# ============================================================
# 6. CREATE CREW
# ============================================================

crew = Crew(
    agents=[
        researcher,
        writer
    ],
    
    tasks=[
        research_task,
        writing_task
    ],
    
    process=Process.sequential,
    verbose=True
)


# ============================================================
# 7. START MULTI AGENT SYSTEM
# ============================================================

print("\n============================================")
print("       COURSE CONTENT GENERATOR")
print("============================================")

result = crew.kickoff()


# ============================================================
# 8. DISPLAY FINAL RESULT
# ============================================================

print("\n\n============================================")
print("          GENERATED COURSE CONTENT")
print("============================================\n")

print(result)

print("\n============================================")
print("              END OF PROJECT")
print("============================================")