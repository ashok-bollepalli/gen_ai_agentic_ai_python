from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


# ==========================================
# CREATE LLM
# ==========================================

llm = LLM(
    model="openai/gpt-5.5-pro",
    api_key=api_key,
    reasoning_effort="medium"
)


# ==========================================
# CREATE AGENTS
# ==========================================

business_analyst = Agent(
    role="Business Analyst",
    goal=(
        "Analyze the project requirements and identify "
        "business requirements, users and application features."
    ),
    backstory=(
        "You are an experienced Business Analyst. "
        "You understand business requirements and convert "
        "business ideas into clear functional requirements."
    ),
    llm=llm,
    verbose=True
)


technical_architect = Agent(
    role="Technical Architect",
    goal=(
        "Design the technical architecture, technologies, "
        "database and major technical components."
    ),
    backstory=(
        "You are an experienced Software Architect specialized "
        "in designing scalable enterprise applications."
    ),
    llm=llm,
    verbose=True
)


project_planner = Agent(
    role="Project Planner",
    goal=(
        "Create a practical development roadmap with modules, "
        "milestones, testing and deployment activities."
    ),
    backstory=(
        "You are an experienced Project Manager who converts "
        "software requirements into development plans."
    ),
    llm=llm,
    verbose=True
)


# ==========================================
# FUNCTION
# ==========================================

def create_project_plan(project_description):

    project_task = Task(

        description=f"""

        Create a complete project plan for:

        {project_description}

        You have access to three specialist agents:

        1. Business Analyst
           - Business requirements
           - Users
           - Application features

        2. Technical Architect
           - Architecture
           - Technologies
           - Database
           - APIs

        3. Project Planner
           - Development modules
           - Milestones
           - Testing
           - Deployment

        Delegate appropriate work to the specialists.

        Review their contributions and create one
        final consolidated project plan.

        The final answer should be simple and suitable
        for software development students.

        """,

        expected_output="""

        A complete project plan containing:

        1. PROJECT OVERVIEW

        2. BUSINESS REQUIREMENTS

        3. USERS

        4. APPLICATION FEATURES

        5. TECHNICAL ARCHITECTURE

        6. TECHNOLOGIES

        7. DATABASE DESIGN

        8. API REQUIREMENTS

        9. DEVELOPMENT MODULES

        10. DEVELOPMENT MILESTONES

        11. TESTING PLAN

        12. DEPLOYMENT PLAN

        13. FINAL SUMMARY

        """
    )


    # ==========================================
    # HIERARCHICAL CREW
    # ==========================================

    crew = Crew(
        agents=[
            business_analyst,
            technical_architect,
            project_planner
        ],

        tasks=[project_task],
        process=Process.hierarchical,
        manager_llm=llm,
        verbose=True
    )


    # ==========================================
    # EXECUTE
    # ==========================================

    result = crew.kickoff()

    return result