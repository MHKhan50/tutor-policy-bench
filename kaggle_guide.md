# Kaggle publication guide

1. Run the benchmark with at least 30 seeds and preserve `outputs/episode_results.csv`, `outputs/policy_summary.csv`, and `outputs/summary.json`.
2. Review the CSV files for correctness and ensure the dataset description explicitly labels every default record as synthetic.
3. If publishing the optional ASSISTments-derived summaries, cite the exact dataset page, explain that it is historical secondary data, and do not upload raw student-level data unless the provider's current terms and privacy requirements explicitly permit it.
4. Create a Kaggle dataset with the generated CSVs, `dataset_card.md`, and the relevant methodology and limitations documents.
5. Include benchmark version, seed count, policy configuration, Python version, and Git commit in the dataset metadata.
6. Do not upload output tables from an incomplete or failed experiment, and do not present simulator results as field validation.
