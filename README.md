# TutorPolicyBench v0.1.0

**Longitudinal Evaluation of Agentic Tutoring Policies under Delayed Retention, Hint Budgets, and Learner-Model Mismatch**

TutorPolicyBench is a lightweight, reproducible benchmark for evaluating *tutoring action-selection policies*, rather than merely scoring the correctness or fluency of generated explanations. It simulates multi-session mathematics learning and compares fixed and adaptive policies under controlled learner profiles, observation noise, retention decay, and interaction-cost budgets.

The benchmark runs on Python 3.9+ with no mandatory third-party runtime dependencies. An optional Ollama adapter allows a local language model to select structured tutoring actions; deterministic baselines remain the reproducible reference.

## Scope and limitations

- The default benchmark uses **synthetic learners and synthetic skill trajectories**.
- The simulator is a transparent experimental model, not a validated psychological or educational model.
- An optional calibration utility reads the public ASSISTments 2009–2010 Skill Builder CSV and produces aggregate skill-level descriptive statistics. It does not estimate causal effects of hints or prove real learning gains.
- No raw student dataset is bundled. Do not commit raw student-level data to GitHub.
- This project does not establish that an AI tutor improves real students' learning. Human-subject evaluation and educator review would be required for that claim.

## Research questions

- **RQ1:** Under equal interaction-cost budgets, do adaptive tutoring policies produce higher delayed simulated retention than direct-answer and fixed-hint baselines?
- **RQ2:** How sensitive are policy rankings to observation noise and mismatch between the learner model used by the tutor and the simulated learner?
- **RQ3:** What trade-offs arise between immediate exercise success, delayed transfer, hint usage, answer revelation, and interaction cost?

## Hypotheses

- **H1:** The adaptive multi-agent policy will improve delayed simulated retention relative to direct-answer and fixed-hint baselines under the simulator's stated transition assumptions.
- **H2:** Increasing observation noise and learner-model mismatch will reduce the advantage of adaptive policies.
- **H3:** Policies that reveal answers more often may increase immediate task completion while producing lower delayed retention in the simulator.

These are falsifiable hypotheses, not reported findings.

## Policies

1. `direct_answer`: reveals the answer immediately; low-learning reference baseline.
2. `fixed_hint`: follows a fixed hint/worked-example sequence independent of estimated mastery.
3. `bkt_threshold`: uses a simple Beta-Binomial mastery estimate to choose between hint, worked example, and retrieval practice.
4. `multi_agent`: diagnostic, misconception, pedagogical-planning, and progress-check roles coordinate a bounded action choice.
5. `ollama`: optional local model selects one structured action per turn; the simulator validates the action and enforces budgets.

The rule-based multi-agent policy is a transparent baseline. It is not an LLM-based multi-agent system.

## Setup in Visual Studio Code

Open the extracted project folder in VS Code, then open **Terminal → New Terminal**.

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --no-build-isolation -e .
python -m unittest discover -s tests -v
python -m tutor_policy_bench.cli --seeds 10
```

Windows PowerShell activation: `.venv\\Scripts\\Activate.ps1`.

## Optional local Ollama evaluation

If Ollama is running locally and a model is already available:

```bash
python -m tutor_policy_bench.cli --seeds 3 --policies ollama --model qwen2.5:3b
```

The adapter uses `http://localhost:11434`. No model is downloaded by this project. The default experiment does not require Ollama.

## Optional ASSISTments calibration

1. Download the 2009–2010 **Skill Builder** dataset from the official ASSISTments page linked in `docs/DATA_AND_PROVENANCE.md`.
2. Place the CSV at `data/raw/skill_builder_data.csv`.
3. Run:

```bash
python scripts/calibrate_assistments.py \
  --input data/raw/skill_builder_data.csv \
  --output data/derived/assistments_skill_priors.csv
```

The script uses aggregate skill-level correctness, hints, attempts, and response-time statistics. It does not export student identifiers or free-text answers. The 2009–2010 dataset is old and should not be treated as representative of present-day learners or Pakistani learners.

## Outputs

The experiment runner writes `outputs/episode_results.csv`, `outputs/policy_summary.csv`, and `outputs/summary.json`. The summary includes mean, standard deviation, and exploratory 95% normal-approximation intervals. Retain seed-level episode rows for paired comparisons. Do not report synthetic results as field evidence.

## Paper-grade protocol

- Use at least 30 seeds for main simulation experiments.
- Pre-register policy parameters and separate development seeds from held-out evaluation seeds.
- Run ablations: disable misconception detection, disable delayed retention, and remove observation noise.
- Report paired seed-level differences and confidence intervals.
- Calibrate simulator parameters against public data only as descriptive priors; test sensitivity to alternative parameter settings.
- Seek educator and student review before making claims about real tutoring effectiveness.

## Repository structure

- `src/tutor_policy_bench/`: learner simulator, policy baselines, multi-agent roles, metrics, experiment runner, optional Ollama adapter
- `tests/`: unit and integration tests
- `docs/`: research assessment, methodology, protocol, data dictionary, ethics, limitations, sources
- `scripts/`: optional ASSISTments calibration utility
- `data/`: empty raw/derived folders; no real student data included

## Suggested repository name
`tutor-policy-bench`

This v0.1.0 release is a general benchmark, not a Pakistan-specific curriculum or language evaluation. A future local study would require curriculum mapping and educator-reviewed Urdu/Roman Urdu materials.
