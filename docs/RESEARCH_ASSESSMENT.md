# Research and novelty assessment (provisional)

## Established work

- EducationQ (2025) already presents a multi-agent teacher–student–evaluator dialogue framework and evaluates teaching effectiveness through simulated interactions and pre/post performance. Therefore, this project does **not** claim novelty for multi-agent tutoring, simulated students, or pedagogical dialogue evaluation.
- Knowledge tracing is a mature research area with extensive public benchmarks, including ASSISTments. Predicting correctness or mastery alone is not a new contribution.
- ASSISTments 2009–2010 Skill Builder data include correctness, attempts, hint counts, response times, and skill labels, but the official dataset page notes that the release does not contain the exact action-level sequence of hints and attempts.

## Narrow proposed contribution

TutorPolicyBench focuses on a different experimental unit: **longitudinal tutoring policy decisions under a fixed interaction-cost budget**, with delayed retention, noisy learner observations, and controlled learner-model mismatch. It preserves seed-level counterfactual comparability by replaying the same generated learner conditions across policy variants.

The intended contribution is a reproducible policy-evaluation harness and sensitivity analysis, not a new knowledge-tracing algorithm or a claim of real-world learning improvement.

## Novelty status

**Provisional; not established.** The literature scan performed for this release is not a systematic review. Before making a novelty claim, search IEEE Xplore, ACM Digital Library, Scopus, Web of Science, ERIC, and the International Educational Data Mining proceedings using combinations of:

- "longitudinal tutoring policy evaluation"
- "delayed retention" AND "AI tutor" / "intelligent tutoring system"
- "hint budget" AND "knowledge tracing"
- "learner model misspecification" AND "pedagogical policy"
- "multi-agent tutoring" AND "retention"

Record inclusion criteria, publication dates, dataset overlap, evaluation horizons, and whether existing benchmarks already evaluate delayed retention under matched interaction budgets.
