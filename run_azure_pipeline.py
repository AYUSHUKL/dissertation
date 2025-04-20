from azure_metrics_collector import collect_azure_metrics
from predictor import run_inference

if __name__ == "__main__":
    print("📡 Collecting metrics from Azure...")
    metrics = collect_azure_metrics()
    print("📦 Collected metrics:", metrics)

    print("🧠 Running AI model for fault detection...")
    result = run_inference(metrics)
    print(f"✅ Result: {result}")
