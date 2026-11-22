
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Step 1: Read Dataset
df = pd.read_csv("dataset.csv")

print(df)

# Step 2: Understand Data
print(df.head())
print(df.shape)
print(df.info())
print(df.describe())

# Step 3: Check Missing Values
print(df.isnull().sum())

# Step 4: Separate Input and Output
# X = Independent variables
# y = Dependent variable

X = df[["age", "bmi", "children", "smoker"]]
y = df["charges"]

# Step 5: Train and Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print("Training Data:", X_train.shape)
print("Testing Data:", X_test.shape)

# Step 6: Create Model
model = DecisionTreeRegressor(
    max_depth=3,
    random_state=42
)

# Step 7: Train Model
model.fit(X_train, y_train)

# Step 8: Make Predictions
y_pred = model.predict(X_test)

print("Actual Values:")
print(y_test.values)

print("Predicted Values:")
print(y_pred)

# Step 9: Evaluate Model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error:", mae)
print("R2 Score:", r2)

# Step 10: Test with New Customer
new_customer = pd.DataFrame({
    "age": [35],
    "bmi": [28.5],
    "children": [2],
    "smoker": [1]
})

prediction = model.predict(new_customer)

print("Predicted Insurance Charges:", prediction[0])

# Step 11: Save Model
with open("insurance_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model Saved Successfully!")
