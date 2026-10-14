
import pandas as pd
import numpy as np

INPUT_FILE = "memory_data.csv"
OUTPUT_FILE = "leak_analysis.csv"

df = pd.read_csv(INPUT_FILE)
df = df.dropna(
    subset=["pid", "timestamp", "memory_mb", "process_name"]
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="coerce"
)
df["memory_mb"] = pd.to_numeric(
    df["memory_mb"], errors="coerce"
)
df = df.dropna(
    subset=["timestamp", "memory_mb"]
)

results = []

for pid, group in df.groupby("pid"):
    group = group.sort_values("timestamp")

    if len(group) < 5:
        continue

    times = (
        group["timestamp"] - group["timestamp"].iloc[0]
    ).dt.total_seconds().to_numpy()

    memory = group["memory_mb"].to_numpy()

    elapsed = times[-1] - times[0]

    if elapsed <= 0:
        continue

    # Estimate memory growth using a linear trend.
    slope, intercept = np.polyfit(times, memory, 1)
    predicted = slope * times + intercept

    # Calculate goodness of fit.
    residual_sum = np.sum((memory - predicted) ** 2)
    total_sum = np.sum((memory - np.mean(memory)) ** 2)

    r_squared = (
        1 - residual_sum / total_sum
        if total_sum > 0
        else 0
    )

    growth_mb = memory[-1] - memory[0]
    growth_per_minute = slope * 60

    # Heuristic for sustained growth, not proof of a leak.
    suspicious = (
        growth_mb >= 20
        and growth_per_minute > 0
        and r_squared >= 0.5
    )

    results.append({
        "pid": int(pid),
        "process_name": str(group["process_name"].iloc[-1]),
        "samples": len(group),
        "duration_seconds": round(elapsed, 2),
        "start_memory_mb": round(memory[0], 2),
        "end_memory_mb": round(memory[-1], 2),
        "growth_mb": round(growth_mb, 2),
        "growth_mb_per_minute": round(growth_per_minute, 2),
        "trend_r_squared": round(r_squared, 3),
        "status": (
            "Suspicious Growth"
            if suspicious
            else "No Significant Growth"
        )
    })

result_df = pd.DataFrame(results)

if result_df.empty:
    print("Not enough valid samples to analyze.")
else:
    result_df = result_df.sort_values(
        "growth_mb", ascending=False
    )
    result_df.to_csv(OUTPUT_FILE, index=False)

    print("\nMemory Growth Analysis")
    print(result_df.to_string(index=False))
    print(f"\nSaved results to {OUTPUT_FILE}")
