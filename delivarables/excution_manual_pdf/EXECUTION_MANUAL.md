# VitalSync AI: System Execution & Deployment Manual

**Project Name:** VitalSync AI  
**Author:** Mohammed Salman Hussain  
**Target Environment:** Local Machine (Windows / Linux / macOS)  
**Python Runtime:** Python 3.10 to 3.14  

---

## 1. System Requirements

### Hardware Requirements
* **Processor**: Intel Core i5 / AMD Ryzen 5 or higher
* **RAM**: 8 GB minimum (16 GB recommended for Ollama GPU acceleration)
* **Storage**: 2 GB free disk space
* **GPU (Optional)**: NVIDIA GPU with CUDA support for local Qwen SLM acceleration (CPU mode fully supported via deterministic fallback)

### Software Requirements
* **Operating System**: Windows 10/11, Ubuntu 20.04+, macOS Ventura+
* **Python**: Version 3.10 or newer (tested on Python 3.14)
* **Web Browser**: Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari (modern ES6+ module support)
* **Local LLM Engine (Optional)**: Ollama (`ollama run qwen3.5:0.8b`)

---

## 2. Installation & Quick Setup

### Step 1: Open Terminal in Project Root
```bash
cd c:\Users\salman\Desktop\projects\p2
```

### Step 2: Install Dependencies (Optional/Standard)
```bash
pip install fastapi uvicorn scikit-learn pydantic requests pytest
```
*(Note: VitalSync AI is built with zero-dependency fallback architecture. If scikit-learn or joblib are absent, the system automatically runs on calibrated analytical regression models without crashing!)*

---

## 3. How to Launch the Application

### Option A: 1-Click Batch Launcher (Windows)
Simply double-click the file:
```
run_demo.bat
```
This script automatically:
1. Verifies your Python installation.
2. Checks project integrity.
3. Launches the FastAPI backend server on `http://localhost:8000`.
4. Automatically opens your default web browser to the dashboard.

### Option B: Manual Command-Line Startup
```bash
python api_server.py
```
Then open your browser and navigate to:
```
http://localhost:8000
```

---

## 4. Running the Automated Test Suite

To verify all mathematical calculations, machine learning models, and clinical triage rules:
```bash
python -m pytest tests/test_phase1.py tests/test_phase2.py tests/test_phase3_4.py
```
*Expected Output:*
```
============================= 24 passed in 0.28s ==============================
```

---

## 5. Live Presentation Demonstration Flow (Quick Guide)

1. **CS Student Persona**: Click `🎓 CS Student` $\rightarrow$ Observe Sleep Latency ($\sim 38\text{m}$) and the 24h Pharmacokinetic Caffeine Decay Curve in Tab 3.
2. **Clinical Safety Red Lockout**: Click `🚨 Red Emergency` $\rightarrow$ Observe the immediate Level 3 Red Hypertensive Crisis banner.
3. **What-If Simulation**: Go to Tab 5 $\rightarrow$ Drag the bedtime phone slider to 60 min $\rightarrow$ Watch the green latency drop update in real time.
4. **AI Report**: Go to Tab 7 $\rightarrow$ Click `✨ Generate AI Consultation Report` $\rightarrow$ Formats into 4 distinct clinical cards with action levers.
5. **Print Export**: Go to Tab 8 $\rightarrow$ Click `🖨️ Print / Save PDF` $\rightarrow$ Displays hospital-grade white A4 print document.
