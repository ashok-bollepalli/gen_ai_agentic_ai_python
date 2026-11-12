import streamlit as st
import pandas as pd
import pickle

# -----------------------------
# Load trained model
# -----------------------------
with open("house_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("🏠 House Price Prediction")
st.write("Enter the house details below to predict the price.")

# -----------------------------
# Input Fields
# -----------------------------

area = st.number_input(
    "Area (Square Feet)",
    min_value=100,
    max_value=10000,
    value=2000,
    step=100
)

bedrooms = st.number_input(
    "Number of Bedrooms",
    min_value=1,
    max_value=20,
    value=3,
    step=1
)

bathrooms = st.number_input(
    "Number of Bathrooms",
    min_value=1,
    max_value=20,
    value=2,
    step=1
)

age = st.number_input(
    "House Age (Years)",
    min_value=0,
    max_value=100,
    value=5,
    step=1
)

# -----------------------------
# Prediction Button
# -----------------------------

if st.button("Predict House Price"):

    # Create DataFrame

    new_house = pd.DataFrame({
        "area" : [area],
        "bedrooms" : [bedrooms],
        "bathrooms" : [bathrooms],
        "age" : [age]
    })

    # Make Prediction
    predicted_price = model.predict(new_house)

    # Display Result

    st.success(
        f"Predicted House Price: ₹{predicted_price[0]:,.2f}"
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.write("Machine Learning Model: Linear Regression")