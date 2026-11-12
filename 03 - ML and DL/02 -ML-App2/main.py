import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# Load Dataset

df = pd.read_csv("dataset.csv")

print(df)


# Understand Data

print(df.head())
print(df.tail())
print(df.shape)
print(df.columns)
print(df.info())
print(df.describe())


# Check Missing Values

print("Missing Values:")
print(df.isnull().sum())


# Check Duplicate Records

print("Duplicate Records:")
print(df.duplicated().sum())

df = df.drop_duplicates()

print(df)


# Create EDA

plt.figure(figsize=(7,5))

sns.countplot(
    x="loan_status",
    data=df
)

plt.xlabel("Loan Status")
plt.ylabel("Number of Applications")
plt.title("Loan Approval Distribution")

plt.show()


# Applicant Income vs Loan Amount

plt.figure(figsize=(8,5))

plt.scatter(
    df["applicant_income"],
    df["loan_amount"]
)

plt.xlabel("Applicant Income")
plt.ylabel("Loan Amount")
plt.title("Applicant Income vs Loan Amount")

plt.show()


# Credit History vs Loan Status

plt.figure(figsize=(7,5))

sns.countplot(
    x="credit_history",
    hue="loan_status",
    data=df
)

plt.xlabel("Credit History")
plt.ylabel("Number of Applications")
plt.title("Credit History vs Loan Status")

plt.show()


# Convert Categorical Data into Numerical Data

le = LabelEncoder()

categorical_columns = [
    "gender",
    "married",
    "dependents",
    "education",
    "self_employed",
    "property_area"
]

for column in categorical_columns:
    df[column] = le.fit_transform(df[column])


# Convert Target Variable

df["loan_status"] = df["loan_status"].map({
    "Y": 1,
    "N": 0
})


print(df.head())


# Define Independent and Dependent Variables

X = df.drop("loan_status", axis=1)

y = df["loan_status"]

print("X:")
print(X)

print("y:")
print(y)


# Split Dataset - 80/20

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("X_Train:", X_train.shape)
print("X_Test :", X_test.shape)

print("Y_Train:", y_train.shape)
print("Y_Test :", y_test.shape)


# Create Classification Model

model = LogisticRegression(max_iter=1000)


# Model Training

model.fit(X_train, y_train)

print("*********** Model Training Completed ***********")


# Make Predictions

y_predict = model.predict(X_test)

print("Predictions:")
print(y_predict)


# Compare Actual vs Predicted

result = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_predict
})

print(result)


# Accuracy

accuracy = accuracy_score(
    y_test,
    y_predict
)

print("Accuracy:", accuracy)
print("Accuracy %:", accuracy * 100)


# Precision

precision = precision_score(
    y_test,
    y_predict,
    zero_division=0
)

print("Precision:", precision)


# Recall

recall = recall_score(
    y_test,
    y_predict,
    zero_division=0
)

print("Recall:", recall)


# F1 Score

f1 = f1_score(
    y_test,
    y_predict,
    zero_division=0
)

print("F1 Score:", f1)


# Classification Report

print(
    classification_report(
        y_test,
        y_predict,
        zero_division=0
    )
)


# Confusion Matrix

cm = confusion_matrix(
    y_test,
    y_predict
)

print("Confusion Matrix:")
print(cm)


# Visualize Confusion Matrix

plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Rejected", "Approved"],
    yticklabels=["Rejected", "Approved"]
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Loan Approval Confusion Matrix")

plt.show()


# Test with New / Unseen Loan Data

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


# Predict New Loan Application

prediction = model.predict(new_loan)

print("Prediction:", prediction)


# Display Meaningful Result

if prediction[0] == 1:
    print("Loan Approved")
else:
    print("Loan Rejected")


# Prediction Probability

probability = model.predict_proba(new_loan)

print(probability)

rejected_probability = probability[0][0] * 100
approved_probability = probability[0][1] * 100

print(
    f"Rejected Probability : {rejected_probability:.2f}%"
)

print(
    f"Approved Probability : {approved_probability:.2f}%"
)


# Final Model Performance

print("\n================================")
print("      MODEL PERFORMANCE")
print("================================")

print(f"Accuracy  : {accuracy:.2f}")
print(f"Precision : {precision:.2f}")
print(f"Recall    : {recall:.2f}")
print(f"F1 Score  : {f1:.2f}")


# Save the ML Model

with open(
    "loan_approval_model.pkl",
    "wb"
) as file:

    pickle.dump(model, file)

print(
    "*********** Model Saved Successfully ***********"
)


# Load the Saved Model

with open(
    "loan_approval_model.pkl",
    "rb"
) as file:

    loaded_model = pickle.load(file)


# Test Loaded Model

prediction = loaded_model.predict(new_loan)

print("Prediction from Loaded Model:", prediction)