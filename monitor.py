
import psutil
import time
import csv
from datetime import datetime

OUTPUT_FILE = "memory_data.csv"


def collect_memory_data():
    """Collect memory usage for running applications."""

    records = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_info"]
    ):
        try:
            info = process.info
            memory_info = info["memory_info"]

            if memory_info is None:
                continue

            memory_mb = memory_info.rss / (1024 * 1024)

            records.append({
                "timestamp": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "pid": info["pid"],
                "process_name": info["name"] or "Unknown",
                "memory_mb": round(memory_mb, 2)
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return records


def main():
    print("MemGuard AI - Memory Monitor")
    print("Collecting data for 30 seconds...")
    print("Please wait.\n")

    all_records = []

    for second in range(30):
        records = collect_memory_data()
        all_records.extend(records)

        print(
            f"Sample {second + 1}/30 | "
            f"Processes recorded: {len(records)}"
        )

        time.sleep(1)

    if all_records:
        with open(
            OUTPUT_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "timestamp",
                    "pid",
                    "process_name",
                    "memory_mb"
                ]
            )
            writer.writeheader()
            writer.writerows(all_records)

        print(f"\nSaved data to {OUTPUT_FILE}")
        print(f"Total records: {len(all_records)}")
    else:
        print("No process data was collected.")


if __name__ == "__main__":
    main()
