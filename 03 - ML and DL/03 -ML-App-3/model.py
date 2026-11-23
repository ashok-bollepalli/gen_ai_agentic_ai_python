import pandas as pd
import matplotlib.pyplot as plt
import pickle

from db_service import load_data

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# Step 1: Load Data from MySQL

df = load_data()

print(df.head())

# Step 2: Remove ID Column

df = df.drop(columns=["id"])

# Step 3: Convert Categorical Data
columns = [
    "gender",
    "married",
    "dependents",
    "education",
    "self_employed",
    "property_area"
]

encoders = {}

for col in columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le
print(df)

# Step 4: Convert Target Variable

df["loan_status"] = df["loan_status"].map({
    "Y": 1,
    "N": 0
})

print("*" * 50)
print(df)

# Step 5: Separate Input and Output
X = df.drop("loan_status", axis=1)

y = df["loan_status"]

# Step 6: Split Data

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Step 7 : Create model
model = LogisticRegression()

# Step 8 : Train model
model.fit(X_train, y_train)

print("Model Training Completed!")

# Step 9: Prediction
y_pred = model.predict(X_test)

# Step 10: Evaluate Model

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy * 100)

# Step 13: Test New Loan Application

new_loan = pd.DataFrame({
    "gender": [1],
    "married": [1],
    "dependents": [0],
    "education": [0],
    "self_employed": [0],
    "applicant_income": [5000],
    "coapplicant_income": [1000],
    "loan_amount": [150],
    "loan_term": [360],
    "credit_history": [1],
    "property_area": [2]
})

# Predict Loan Status

prediction = model.predict(new_loan)

if prediction[0] == 1:
    print("Loan Approved")
else:
    print("Loan Rejected")

# Step 14: Save Model

pickle.dump(model, open("loan_model.pkl", "wb"))
pickle.dump(encoders, open("loan_encoders.pkl", "wb"))

print("Model Saved Successfully!")
