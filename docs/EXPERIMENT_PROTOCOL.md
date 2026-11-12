# Experiment protocol

1. Record Python version, operating system, benchmark version, and Git commit.
2. Run `python -m unittest discover -s tests -v`.
3. Run the default experiment with 10 seeds as a smoke/reproducibility check.
4. For main experiments, use at least 30 seeds and the same seed set across all policies.
5. Run a factorial sensitivity study across learner profile (novice/intermediate/advanced), observation noise (0.00/0.10/0.25), and model mismatch (0.00/0.15/0.30).
6. Keep policy parameters fixed before held-out evaluation.
7. Report immediate correctness, delayed transfer, mastery gain, answer-reveal rate, hint count, interaction cost, and budget rejections.
8. Use paired seed-level differences for policy comparisons. Include effect sizes and confidence intervals.
9. Run ablations for misconception detection, retention decay, and learner-state estimation.
10. Do not interpret simulator results as evidence of efficacy with real learners. A later human-subject study requires ethics approval and educator involvement.
