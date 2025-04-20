from gcp_metrics_collector import collect_gcp_metrics
from predictor import run_inference
from datetime import datetime

LOG_FILE = "results_log.txt"

def log_result(result, metrics):
    """
    Logs the inference result with timestamp and metrics in dashboard-compatible format.
    """
    now = datetime.utcnow().isoformat() + "Z"

    # Ensure 10 metrics: pad with 0s if fewer
    metric_values = list(metrics.values())
    if len(metric_values) < 10:
        metric_values += [0] * (10 - len(metric_values))
    else:
        metric_values = metric_values[:10]  # only take first 10 if more

    log_line = f"{now},{result}," + ",".join(map(str, metric_values)) + ",GCP\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    print("📝 Logged to results_log.txt")

if __name__ == "__main__":
    print("📡 Collecting metrics from GCP...")
    metrics = collect_gcp_metrics()
    print("📦 Collected metrics:", metrics)

    print("🧠 Running AI model for fault detection...")
    result = run_inference(metrics)
    print(f"✅ Result: {result}")

    log_result(result, metrics)
