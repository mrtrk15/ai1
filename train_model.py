from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pickle

# Sample dummy dataset (replace later with real data)
X = np.array([
    [7.5, 20, 85, 40, 0, 3, 4, 3],
    [6.0, 10, 70, 30, 2, 5, 2, 2],
    [8.5, 25, 90, 45, 0, 2, 5, 4],
    [5.5, 8, 60, 25, 3, 6, 1, 1]
])

y = np.array([8.2, 6.5, 9.0, 5.8])  # CGPA output

# Train model
model = RandomForestRegressor()
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as model.pkl")