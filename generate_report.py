
import pandas as pd
from datetime import datetime

INPUT_FILE = "leak_analysis.csv"
OUTPUT_FILE = "diagnostic_report.md"


def generate_diagnosis(row):
    growth = row["growth_mb"]
    rate = row["growth_mb_per_minute"]
    r_squared = row["trend_r_squared"]

    if row["status"] == "Suspicious Growth":
        return (
            "This process showed sustained positive memory growth "
            "during the observed period. This can happen during "
            "normal work, caching, or a possible memory leak. "
            "Repeat the measurement over a longer period and check "
            "whether memory returns to baseline after the workload."
        )

    if growth < 0:
        return (
            "Memory usage decreased during the observation period. "
            "This may indicate that the process released memory. "
            "Continue monitoring if memory pressure remains a concern."
        )

    return (
        "The current screening rule did not flag this process. "
        "This does not prove that the process is free of memory leaks. "
        "Collect longer observations under a representative workload."
    )


def main():
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Missing {INPUT_FILE}. Run analyze_growth.py first.")
        return

    if df.empty:
        print("No process results are available.")
        return

    lines = [
        "# MemGuard AI Diagnostic Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "> This is an automated screening report, not proof of a memory leak.",
        "",
        "## Summary",
        "",
        f"- Processes analyzed: {len(df)}",
        f"- Flagged for suspicious growth: "
        f"{(df['status'] == 'Suspicious Growth').sum()}",
        "",
        "## Process Findings",
        ""
    ]

    for _, row in df.iterrows():
        lines.extend([
            f"### {row['process_name']} (PID {row['pid']})",
            "",
            f"- Status: {row['status']}",
            f"- Starting memory: {row['start_memory_mb']} MB",
            f"- Ending memory: {row['end_memory_mb']} MB",
            f"- Net growth: {row['growth_mb']} MB",
            f"- Growth rate: {row['growth_mb_per_minute']} MB/min",
            f"- Trend fit (R²): {row['trend_r_squared']}",
            "",
            "**Diagnostic guidance**",
            "",
            generate_diagnosis(row),
            "",
            "**Suggested checks**",
            "",
            "1. Repeat the test over a longer observation period.",
            "2. Compare memory usage before and after the same workload.",
            "3. Review application logs and recent code changes.",
            "4. Use a language-specific profiler to investigate allocations.",
            ""
        ])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print("Diagnostic report created:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
