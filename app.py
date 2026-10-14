
import streamlit as st
import pandas as pd
import psutil
import os

st.set_page_config(
    page_title="MemGuard AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MemGuard AI")
st.caption("Memory Monitoring and Anomaly Detection")

# Current system memory
memory = psutil.virtual_memory()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total RAM",
    f"{memory.total / (1024 ** 3):.2f} GB"
)

col2.metric(
    "RAM Used",
    f"{memory.used / (1024 ** 3):.2f} GB"
)

col3.metric(
    "Memory Usage",
    f"{memory.percent:.1f}%"
)

st.progress(int(memory.percent))

if memory.percent >= 85:
    st.warning("High system memory usage detected.")
else:
    st.success("System memory is below the warning threshold.")

st.divider()
st.header("AI Anomaly Detection Results")

analysis_file = "memory_analysis.csv"

if os.path.exists(analysis_file):
    df = pd.read_csv(analysis_file)

    if not df.empty and "status" in df.columns:
        suspicious = df[df["status"] == "Suspicious"]
        normal = df[df["status"] == "Normal"]

        a, b, c = st.columns(3)

        a.metric("Records Analyzed", len(df))
        b.metric("Normal Records", len(normal))
        c.metric("Suspicious Records", len(suspicious))

        st.subheader("Process Memory Analysis")

        if "process_name" in df.columns:
            process_options = sorted(
                df["process_name"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_process = st.selectbox(
                "Select a process",
                ["All Processes"] + process_options
            )

            if selected_process != "All Processes":
                df = df[
                    df["process_name"].astype(str)
                    == selected_process
                ]

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                errors="coerce"
            )

        if "memory_mb" in df.columns:
            st.line_chart(
                df.set_index("timestamp")["memory_mb"]
                if "timestamp" in df.columns
                else df["memory_mb"]
            )

        st.subheader("Detection Details")

        if "timestamp" in df.columns:
            df["timestamp"] = df["timestamp"].astype(str)

        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download Analysis CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="memory_analysis.csv",
            mime="text/csv"
        )
    else:
        st.info(
            "Analysis file is empty or missing the status column. "
            "Run python train_model.py again."
        )
else:
    st.info(
        "No analysis results found. Run these commands first:\n\n"
        "1. python monitor.py\n"
        "2. python train_model.py"
    )

st.divider()
st.caption(
    "Prototype: unusual memory values are not proof of a memory leak."
)

st.divider()
st.header("📝 Diagnostic Report")

import os

report_file = "diagnostic_report.md"

if os.path.exists(report_file):
    with open(report_file, "r", encoding="utf-8") as file:
        report_text = file.read()

    st.markdown(report_text)

    st.download_button(
        label="Download Diagnostic Report",
        data=report_text,
        file_name="diagnostic_report.md",
        mime="text/markdown"
    )

    st.success("Diagnostic report is ready.")
else:
    st.info(
        "No diagnostic report found. Run these commands "
        "in the terminal first:"
    )
    st.code(
        "python analyze_growth.py\n"
        "python generate_report.py"
    )
