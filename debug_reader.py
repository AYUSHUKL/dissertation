import pandas as pd

df = pd.read_csv(
    "results_log.txt",
    names=["timestamp", "result", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "platform"],
    header=None
)
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M:%S.%fZ", errors="coerce")
print(df.head())
