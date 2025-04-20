from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
import datetime

subscription_id = "provide<>your<>subs<>id"
resource_id = "provide<>your<>resource<>id"

def collect_azure_metrics():
    credential = DefaultAzureCredential()
    monitor_client = MonitorManagementClient(credential, subscription_id)

    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(minutes=5)
    timespan = f"{start_time.isoformat()}/{end_time.isoformat()}"

    metrics = ["CpuTime", "Requests", "Errors"]
    collected = {}

    for metric in metrics:
        try:
            result = monitor_client.metrics.list(
                resource_id,
                timespan=timespan,
                interval=None,
                metricnames=metric,
                aggregation="Total"
            )
            if result.value and result.value[0].timeseries[0].data:
                collected[metric] = result.value[0].timeseries[0].data[-1].total or 0.0
            else:
                collected[metric] = 0.0
        except Exception as e:
            print(f"⚠️ Metric {metric} could not be collected: {e}")
            collected[metric] = 0.0

    return collected
