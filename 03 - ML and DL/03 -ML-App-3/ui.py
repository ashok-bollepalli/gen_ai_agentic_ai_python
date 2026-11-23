
import streamlit as st
import pandas as pd
import pickle


# Load ML Model
model = pickle.load(open("loan_model.pkl", "rb"))


# Page Configuration
st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="centered"
)


# Page Title
st.title("🏦 Loan Approval Prediction")

st.write("Enter applicant details to predict loan approval.")


# Applicant Details

st.subheader("Applicant Information")

gender = st.selectbox("Gender", ["Male", "Female"])

married = st.selectbox("Married", ["Yes", "No"])

dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])

education = st.selectbox(
    "Education",
    ["Graduate", "Not Graduate"]
)

self_employed = st.selectbox(
    "Self Employed",
    ["Yes", "No"]
)

property_area = st.selectbox(
    "Property Area",
    ["Urban", "Semiurban", "Rural"]
)


# Financial Details

st.subheader("Financial Information")

applicant_income = st.number_input(
    "Applicant Income",
    min_value=0,
    value=5000
)

coapplicant_income = st.number_input(
    "Coapplicant Income",
    min_value=0,
    value=1000
)

loan_amount = st.number_input(
    "Loan Amount",
    min_value=0,
    value=150
)

loan_term = st.number_input(
    "Loan Term (Months)",
    min_value=1,
    value=360
)

credit_history = st.selectbox(
    "Credit History",
    [1, 0],
    format_func=lambda x: "Good" if x == 1 else "Poor"
)


# Prediction Button

if st.button("Predict Loan Status"):

    # Convert Input into DataFrame

    new_loan = pd.DataFrame({
        "gender": [gender],
        "married": [married],
        "dependents": [dependents],
        "education": [education],
        "self_employed": [self_employed],
        "applicant_income": [applicant_income],
        "coapplicant_income": [coapplicant_income],
        "loan_amount": [loan_amount],
        "loan_term": [loan_term],
        "credit_history": [credit_history],
        "property_area": [property_area]
    })

    # Convert Categorical Values
    columns = [
        "gender",
        "married",
        "dependents",
        "education",
        "self_employed",
        "property_area"
    ]

    # Use same encoding as training
    encoders = pickle.load(open("loan_encoders.pkl", "rb"))

    for col in columns:
        new_loan[col] = encoders[col].transform(new_loan[col])

    # Predict
    prediction = model.predict(new_loan)

    # Display Result
    st.subheader("Prediction Result")

    if prediction[0] == 1:
        st.success("🎉 Loan Approved!")
    else:
        st.error("❌ Loan Rejected!")
