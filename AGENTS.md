# AGENTS.md - Workspace Instructions & Standards

All agent interactions and code implementations in this repository must strictly adhere to the project rules defined in [.agents/rules/health_platform_rules.md](file:///.agents/rules/health_platform_rules.md).

## Core Directives Summary:
1. **Ethical Disclaimer & Medical Safety**: Lifestyle & wellness advice only. Not medical advice. Enforce the 3-Tier Clinical Triage System (Green, Yellow, Red).
2. **Zero Hallucinations**: All mathematical formulas and ML models must be validated, tested, and grounded in authentic datasets and peer-reviewed science.
3. **Homogeneous System Design**: All features link to a unified `UserHealthProfile` state orchestrated by a central `HealthOrchestrator`. No disconnected toy scripts.
4. **Anti-Cyberchondria Philosophy**: Demystify bodily signals with calm biological explanations to eliminate health anxiety.
5. **Local-First Privacy**: 100% offline/local execution. Local Python ML + local Qwen via Ollama on GPU. Zero external data transmission.
6. **Feature Rich & Modular**: Maximum feature coverage with toggleable UI visibility.
7. **Counterfactual Interactivity**: Support "What-If" real-time simulations.
