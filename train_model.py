import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
df = pd.read_csv("student_dataset.csv")

# Features and target
X = df.drop("final_cgpa", axis=1)
y = df["final_cgpa"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(n_estimators=100)

# Train
model.fit(X_train, y_train)

# Accuracy
score = model.score(X_test, y_test)
print("Model Accuracy (R2 Score):", score)

# Save model
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")