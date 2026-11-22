
import streamlit as st
import pandas as pd
import pickle

# Page Configuration
st.set_page_config(
    page_title="Insurance Price Prediction",
    page_icon="🏥",
    layout="centered"
)

# Load Model
with open("insurance_model.pkl", "rb") as file:
    model = pickle.load(file)

# Application Title
st.title("🏥 Medical Insurance Price Prediction")

st.write(
    "Enter customer details to estimate medical insurance charges."
)

st.divider()

# Input Fields
col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=35
    )

    bmi = st.number_input(
        "BMI",
        min_value=10.0,
        max_value=60.0,
        value=28.5
    )

with col2:
    children = st.number_input(
        "Number of Children",
        min_value=0,
        max_value=10,
        value=2
    )

    smoker = st.selectbox(
        "Smoking Status",
        ["No", "Yes"]
    )

st.divider()

# Prediction
if st.button("Predict Insurance Charges", type="primary"):

    smoker_value = 1 if smoker == "Yes" else 0

    new_customer = pd.DataFrame({
        "age": [age],
        "bmi": [bmi],
        "children": [children],
        "smoker": [smoker_value]
    })

    prediction = model.predict(new_customer)[0]

    st.success("Prediction Completed!")

    st.subheader("Estimated Insurance Charges")

    st.markdown(f"## {prediction:,.2f}")

    st.info(
        f"""
        Customer Details:

        Age: {age} Years

        BMI: {bmi}

        Children: {children}

        Smoker: {smoker}
        """
    )

st.divider()

st.caption(
    "Developed using Python, Pandas, "
    "Scikit-Learn and Streamlit | Ashok IT"
)
