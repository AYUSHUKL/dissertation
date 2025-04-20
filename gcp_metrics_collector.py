from google.cloud import monitoring_v3
from datetime import datetime, timedelta
import pytz

project_id = ""
project_name = f"projects/{project_id}"

client = monitoring_v3.MetricServiceClient()

now = datetime.utcnow().replace(tzinfo=pytz.UTC)
interval = monitoring_v3.TimeInterval(
    end_time=now,
    start_time=now - timedelta(minutes=5)
)

metrics = [
    "cloudfunctions.googleapis.com/function/execution_count",
    "cloudfunctions.googleapis.com/function/execution_times",
    "cloudfunctions.googleapis.com/function/execution_failures"
]

def collect_gcp_metrics():
    collected = {}
    for metric in metrics:
        try:
            results = client.list_time_series(
                request={
                    "name": project_name,
                    "filter": f'metric.type = "{metric}"',
                    "interval": interval,
                    "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
                }
            )
            label = metric.split("/")[-1]
            for res in results:
                collected[label] = res.points[-1].value.double_value if res.points else 0.0
        except Exception as e:
            print(f"⚠️ Metric {metric} not found or empty: {e}")
            label = metric.split("/")[-1]
            collected[label] = 0.0  # fallback value

    return collected

if __name__ == "__main__":
    metrics_output = collect_gcp_metrics()
    print("✅ GCP Metrics Collected:", metrics_output)
