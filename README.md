# MemGuardAI — AI-Powered Memory Leak Detection

## Overview
MemGuardAI is a Python-based project that monitors process memory usage, analyzes memory growth, and generates diagnostic reports using a local AI model.

## Features
- Process memory monitoring
- Memory usage data collection
- Memory growth and anomaly analysis
- Rule-based diagnostic reports
- AI-powered diagnosis using Ollama
- Streamlit dashboard
- Diagnostic report export

## Technologies Used
- Python
- Streamlit
- Pandas
- Scikit-learn
- Psutil
- Ollama
- Llama 3.2

## Project Structure
- `app.py` — Dashboard
- `monitor.py` — Memory monitoring
- `analyze_growth.py` — Memory growth analysis
- `train_model.py` — Anomaly detection model
- `detect_leaks.py` — Basic leak detection
- `generate_report.py` — Diagnostic report generation
- `ai_diagnosis.py` — AI diagnosis
- `simulate_leak.py` — Memory growth simulation

## Setup


1. Create and activate a Python virtual environment.
2. Install dependencies from `requirements.txt`.
3. Install Ollama and download the model:

   `ollama pull llama3.2:3b`

4. Run the dashboard:

   `python -m streamlit run app.py`

## Disclaimer
MemGuardAI identifies possible memory growth and anomalies. Its findings are diagnostic indicators, not proof of a memory leak.