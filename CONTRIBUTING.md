# Contributing to VitalSync AI

Thank you for your interest in contributing to **VitalSync AI**! Our mission is to provide an evidence-grounded, zero-hallucination, and anti-cyberchondria health intelligence platform that empowers everyday individuals while strictly adhering to safety and clinical guardrails.

---

## 🏛️ The 7 Core Architectural Directives

All pull requests, bug fixes, and feature additions **must strictly comply** with our 7 Core Directives (defined in [`.agents/rules/health_platform_rules.md`](file:///.agents/rules/health_platform_rules.md)):

1. **Ethical Disclaimer & Safety**:
   - The platform provides lifestyle and behavioral optimization only—never medical diagnosis or therapy.
   - Any new view, report, or endpoint must preserve the 3-Tier Clinical Safety Triage System (`Green`, `Yellow`, `Red`).
2. **Zero Hallucination & Rigorous Validation**:
   - All formulas must come from peer-reviewed literature (e.g., Mifflin-St Jeor, Katch-McArdle, 1st-order pharmacokinetics).
   - All machine learning additions must be trained on authentic datasets with validated cross-validation metrics.
3. **Homogeneous Architecture**:
   - All features must link to the unified `UserHealthProfile` state and pass through `HealthOrchestrator`. No orphaned or toy scripts.
4. **Anti-Cyberchondria Philosophy**:
   - Demystify bodily sensations with biological explanations rather than disease lists. Focus on the top 3 actionable levers.
5. **Local-First Privacy & Zero Telemetry**:
   - 100% offline localhost execution. No external cloud API calls for user health data. Local ML + local Qwen via Ollama on GPU.
6. **Feature Modularity**:
   - Keep features toggleable in the UI so users can switch between Quick (2-minute) and Deep intake modes.
7. **Counterfactual Simulation**:
   - Keep metrics interactive, allowing "What-If" simulations.

---

## 🛠️ Development Setup

### 1. Clone & Environment Setup
```bash
# Clone the repository
git clone https://github.com/vitalsync-ai/vitalsync-ai.git
cd vitalsync-ai

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running Automated Tests
We maintain 100% passing automated test coverage across our core math, ML models, triage rules, and orchestrator.
```bash
pytest
```
Ensure all 24 tests pass before submitting any pull request.

### 3. Local Servers
- **FastAPI Backend + Modern Glassmorphic Web UI**:
  ```bash
  uvicorn api_server:app --reload --port 8000
  ```
  Visit: `http://localhost:8000`

- **Streamlit Pro Dashboard**:
  ```bash
  streamlit run app.py
  ```
  Visit: `http://localhost:8501`

---

## 🧪 Adding New Features

### Adding a New Mathematical Calculator
1. Implement the mathematical logic in [`calculators.py`](file:///calculators.py) with docstrings citing the literature.
2. Add fields to `MathematicalMetrics` in [`schemas.py`](file:///schemas.py).
3. Write automated unit tests in [`tests/test_phase1.py`](file:///tests/test_phase1.py) covering edge cases and boundary conditions.

### Adding or Retraining a Machine Learning Model
1. Place training code in [`train_models.py`](file:///train_models.py).
2. Save serialized pipeline bundles in `models/` with calibrated prediction probabilities.
3. Add inference methods to `MLInferenceEngine` in [`ml_inference.py`](file:///ml_inference.py).
4. Verify with integration tests in [`tests/test_phase2.py`](file:///tests/test_phase2.py).

---

## 📬 Pull Request Process
1. Fork the repository and create your feature branch: `git checkout -b feature/amazing-feature`.
2. Commit your changes: `git commit -m "feat: add validated hydration sweat-rate calculator"`.
3. Push to your branch: `git push origin feature/amazing-feature`.
4. Open a Pull Request with a clear description and test verification log.
