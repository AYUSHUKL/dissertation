import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder
import joblib

# Sample AWS Lambda failure logs (Replace with real logs)
data = {
    "cpu_usage": [30, 80, 55, 90, 20, 75],
    "memory_usage": [256, 1024, 512, 2048, 128, 750],
    "execution_time": [500, 1200, 850, 2200, 300, 1700],
    "error_count": [0, 5, 3, 10, 0, 7],
    "error_type": ["None", "CloudFormationError", "APIGatewayError", "NoPassword", "None", "VPCError"]
}

df = pd.DataFrame(data)

# Encode error types using One-Hot Encoding
encoder = OneHotEncoder()
error_encoded = encoder.fit_transform(df[['error_type']]).toarray()
error_columns = encoder.get_feature_names_out(['error_type'])

df_encoded = pd.DataFrame(error_encoded, columns=error_columns)

# Prepare training data
X = pd.concat([df.drop(columns=['error_type']), df_encoded], axis=1)

# Train Isolation Forest Model
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(X)

# Save model
joblib.dump(model, 'ai_fault_detector.pkl')
print("✅ Model trained and saved successfully.")
