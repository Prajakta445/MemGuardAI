
import pandas as pd

INPUT_FILE = "memory_data.csv"
OUTPUT_FILE = "leak_analysis.csv"

df = pd.read_csv(INPUT_FILE)
df = df.dropna(subset=["pid", "timestamp", "memory_mb"])

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

df = df.dropna(subset=["timestamp"])
df = df.sort_values(["pid", "timestamp"])

results = []

for pid, group in df.groupby("pid"):
    group = group.sort_values("timestamp")

    if len(group) < 5:
        continue

    first = group.iloc[0]
    last = group.iloc[-1]

    start_memory = float(first["memory_mb"])
    end_memory = float(last["memory_mb"])
    growth = end_memory - start_memory

    elapsed = (
        last["timestamp"] - first["timestamp"]
    ).total_seconds()

    if elapsed <= 0:
        continue

    growth_per_minute = growth / elapsed * 60

    if growth >= 20 and growth_per_minute > 0:
        status = "Suspicious Growth"
    else:
        status = "No Significant Growth"

    results.append({
        "pid": pid,
        "process_name": group.iloc[-1]["process_name"],
        "start_memory_mb": round(start_memory, 2),
        "end_memory_mb": round(end_memory, 2),
        "growth_mb": round(growth, 2),
        "growth_mb_per_minute": round(growth_per_minute, 2),
        "status": status,
        "samples": len(group),
        "duration_seconds": round(elapsed, 2)
    })

result_df = pd.DataFrame(results)

if not result_df.empty:
    result_df = result_df.sort_values(
        "growth_mb",
        ascending=False
    )
    result_df.to_csv(OUTPUT_FILE, index=False)

    print("\nMemory Growth Analysis")
    print(result_df.to_string(index=False))
    print(f"\nSaved results to {OUTPUT_FILE}")
else:
    print("Not enough valid process samples to analyze.")
