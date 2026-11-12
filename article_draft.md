# TutorPolicyBench: A Longitudinal Benchmark for Tutoring Action Policies under Delayed Retention and Interaction Budgets

## Abstract (planned study; no empirical claims yet)

This paper proposes a reproducible benchmark for evaluating tutoring action-selection policies across multiple learning sessions. Unlike single-turn answer-quality evaluation, the benchmark measures immediate exercise performance alongside delayed simulated transfer, mastery change, hint use, answer revelation, and interaction cost. It compares direct-answer, fixed-hint, knowledge-estimate threshold, and rule-based multi-agent policies under controlled learner profiles, observation noise, retention decay, and learner-model mismatch. A synthetic learner simulator provides counterfactual comparability across policies, while an optional ASSISTments calibration utility provides aggregate descriptive statistics for sensitivity analysis. The simulator is not a validated model of human learning, and all default outcomes are synthetic. The central research question is whether adaptive tutoring policies retain an advantage under realistic uncertainty and fixed interaction budgets. No claim of real-world educational efficacy is made.

## 1. Introduction

Educational AI evaluation has expanded beyond static question answering toward multi-turn tutoring interactions. EducationQ demonstrates the use of teacher, student, and evaluator agents to simulate teaching interactions, while ASSISTments provides longitudinal interaction records used in educational data mining. These lines of work motivate more outcome-oriented evaluation, but they do not remove the need to distinguish immediate task success from delayed retention or to test how policy rankings change when the learner model is misspecified.

## 2. Research questions and hypotheses

- RQ1: Under equal interaction-cost budgets, do adaptive policies improve delayed simulated retention over direct-answer and fixed-hint baselines?
- RQ2: How sensitive are policy rankings to observation noise and learner-model mismatch?
- RQ3: What trade-offs arise between immediate correctness, delayed transfer, hint use, answer revelation, and interaction cost?

H1–H3 are specified in `docs/RESEARCH_ASSESSMENT.md` and must be preregistered before confirmatory experiments.

## 3. Method

The benchmark uses three synthetic learner profiles, three mathematics skills, repeated sessions, noisy correctness observations, and an interaction-cost budget. The policy set includes direct-answer, fixed-hint, Beta-Binomial threshold, and deterministic multi-agent policies. An optional local Ollama adapter can be evaluated separately. The simulator's transition assumptions are documented in `docs/METHODOLOGY.md`.

## 4. Evaluation

Report episode-level results and paired seed-level differences for immediate accuracy, delayed transfer accuracy, mastery gain, hint count, answer reveal count, interaction cost, and budget rejections. Use at least 30 seeds for the main study, hold out seeds for evaluation, and include ablations and uncertainty intervals.

## 5. Limitations

All default learner trajectories are synthetic. The simulator is not a validated cognitive model, and the optional ASSISTments data can provide only aggregate descriptive priors because the historical release does not contain the full action-level sequence of hints and attempts. Human educator review and human-subject research are required before making claims about actual student outcomes.

## 6. Results

**To be completed only after the user runs and verifies the planned experiments. No results are claimed in this draft.**
