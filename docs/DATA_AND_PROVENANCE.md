# Data sources and provenance

## Default benchmark data
All default learner profiles, skill sequences, observations, and outcomes are generated synthetically from deterministic random seeds. No real student records are included.

## Optional real-data calibration: ASSISTments 2009–2010 Skill Builder
- Official data page: https://sites.google.com/site/assistmentsdata/home/2009-2010-assistment-data/skill-builder-data-2009-2010
- Main dataset description: https://sites.google.com/site/assistmentsdata/home/2009-2010-assistment-data
- The provider states that the data are free to use and asks researchers to cite the exact dataset page.
- The dataset includes correctness, attempts, hint counts, response times, and skill labels. The provider notes that the release does not contain the exact action-level sequence of hints and attempts.
- The calibration script reads aggregateable columns and emits per-skill summary statistics. It does not export user IDs, answer text, or row-level records.

Suggested dataset citation:
Feng, M., Heffernan, N. T., & Koedinger, K. R. (2009). Addressing the assessment challenge in an Intelligent Tutoring System that tutors as it assesses. *User Modeling and User-Adapted Interaction*, 19, 243–266. https://doi.org/10.1007/s11257-009-9066-1

## Optional newer resource for future work
FoundationalASSIST (2026) contains student interactions, problem text, and answer text and is released under CC-BY-NC-4.0. Its documentation warns that accidental PII may remain in free-text responses despite filtering. It is not consumed by this v0.1.0 release. See https://huggingface.co/datasets/ASSISTments/FoundationalASSIST and https://arxiv.org/abs/2602.00070.
