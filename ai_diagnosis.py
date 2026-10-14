
import requests
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
input_file = BASE_DIR / "leak_analysis.csv"
output_file = BASE_DIR / "ai_diagnostic_report.md"

print("MemGuardAI: Starting AI diagnosis...", flush=True)

if not input_file.exists():
    print("ERROR: leak_analysis.csv not found.", flush=True)
    print("Run: python analyze_growth.py", flush=True)
    raise SystemExit(1)

data = pd.read_csv(input_file)
print("Memory analysis loaded.", flush=True)

prompt = f"""
Analyze these application memory growth results:

{data.to_string(index=False)}

Write a diagnostic report containing:
1. Summary
2. Possible memory leak indicators
3. Evidence from the data
4. Recommended debugging steps

Do not claim a confirmed memory leak from growth alone.
"""

try:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2:3b",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        },
        timeout=300
    )
    response.raise_for_status()

    report = response.json()["message"]["content"]
    output_file.write_text(report, encoding="utf-8")

    print(f"SUCCESS: Report saved to {output_file}", flush=True)

except Exception as error:
    print(f"ERROR: {error}", flush=True)
