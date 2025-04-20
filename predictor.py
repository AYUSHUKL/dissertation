import joblib
import numpy as np
from feature_extractor import extract_standard_features

def run_inference(metrics_dict: dict, model_path="ai_fault_detector.pkl"):
    """
    Load model and run inference.

    Args:
        metrics_dict (dict): Dictionary of collected metrics.
        model_path (str): Path to the pre-trained model.

    Returns:
        str: "Fault Detected" or "No Fault"
    """
    # Load model
    model = joblib.load(model_path)

    # Convert raw metrics to standard input vector
    feature_vector = extract_standard_features(metrics_dict)
    input_array = np.array(feature_vector).reshape(1, -1)

    # Run prediction
    prediction = model.predict(input_array)[0]

    return "Fault Detected" if prediction == -1 else "No Fault"

