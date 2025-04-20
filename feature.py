import joblib

# Load trained model
model = joblib.load("ai_fault_detector.pkl")

# Print expected number of features
print(f"Model expects {model.n_features_in_} features as input.")
