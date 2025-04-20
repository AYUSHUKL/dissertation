def extract_standard_features(metrics: dict) -> list:
    """
    Standardizes metrics from AWS, Azure, GCP into a 9-length feature vector.
    Missing metrics are filled with 0.

    Expected Feature Order:
    [Duration, MaxMemoryUsed, Invocations, Errors, Throttles, ConcurrentExecutions,
     CpuTime, execution_count, execution_times]
    """
    return [
        metrics.get("Duration", 0),                 # AWS/GCP
        metrics.get("MaxMemoryUsed", 0),            # AWS
        metrics.get("Invocations", 0),              # AWS
        metrics.get("Errors", 0),                   # AWS
        metrics.get("Throttles", 0),                # AWS
        metrics.get("ConcurrentExecutions", 0),     # AWS
        metrics.get("CpuTime", 0),                  # Azure
        metrics.get("execution_count", 0),          # GCP
        metrics.get("execution_times", 0),          # GCP
    ]
