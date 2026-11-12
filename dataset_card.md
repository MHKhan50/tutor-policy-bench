# Dataset Card — TutorPolicyBench v0.1.0

## Summary
TutorPolicyBench generates synthetic longitudinal tutoring episodes for comparing action-selection policies. Each episode contains a synthetic learner profile, policy identifier, observation-noise and model-mismatch settings, immediate response outcomes, delayed transfer probes, action counts, and interaction costs.

## Intended uses
- Research on policy-level tutoring evaluation and simulator sensitivity.
- Reproducible comparison of fixed and adaptive tutoring strategies.
- Software testing of local structured-action policies.

## Out-of-scope uses
- Estimating real student learning gains.
- Ranking actual students or teachers.
- Deploying an autonomous tutor for children without educator oversight.
- Making claims about Pakistani learners from the synthetic profiles.

## Data generation
All default rows are generated from deterministic random seeds by `src/tutor_policy_bench/simulator.py`. The simulator's assumptions are explicit in code and documented in `docs/METHODOLOGY.md`.

## Real-data calibration option
The optional calibration script can aggregate ASSISTments 2009–2010 Skill Builder statistics by skill. Raw data are not included or redistributed. Derived output omits student identifiers and free-text answers. This historical dataset is not used by the default benchmark.

## Limitations
The simulated learner transition model is researcher-defined. Delayed transfer is a simulator proxy, not a real assessment. See `docs/LIMITATIONS.md` and `docs/ETHICS.md`.
