import streamlit as st

from project_planning_service import create_project_plan


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Project Planner",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("🤖 AI Project Planner")

st.write(
    "Create a complete software project plan using "
    "CrewAI Hierarchical Agents."
)


st.divider()


# ==========================================
# PROJECT INPUT
# ==========================================

st.subheader("📋 Project Requirements")

project_description = st.text_area(
    "Enter your project description",
    height=180,
    placeholder="""
Example:

Online Food Delivery Application

The application should allow customers to browse
restaurants, view menus, add food to cart, place orders,
make payments and track deliveries.

Restaurants should be able to manage menus and orders.

Delivery partners should be able to accept deliveries
and update delivery status.
"""
)


# ==========================================
# GENERATE BUTTON
# ==========================================

if st.button(
    "🚀 Generate Project Plan",
    type="primary",
    use_container_width=True
):

    if not project_description.strip():

        st.warning(
            "Please enter project requirements."
        )

    else:

        # ==========================================
        # SHOW PROGRESS
        # ==========================================

        with st.spinner(
            "🤖 AI agents are working on your project..."
        ):

            try:

                result = create_project_plan(
                    project_description
                )

                st.success(
                    "Project plan generated successfully!"
                )


                # ==========================================
                # DISPLAY RESULT
                # ==========================================

                st.divider()

                st.subheader(
                    "📊 Final Project Plan"
                )

                st.markdown(
                    str(result)
                )


                # ==========================================
                # DOWNLOAD
                # ==========================================

                st.download_button(
                    label="📥 Download Project Plan",
                    data=str(result),
                    file_name="project_plan.txt",
                    mime="text/plain",
                    use_container_width=True
                )


            except Exception as e:

                st.error(
                    f"Unable to generate project plan: {e}"
                )