# Data dictionary

## Episode-level output (`episode_results.csv`)
- `seed`: deterministic random seed.
- `profile`: synthetic learner profile (novice/intermediate/advanced).
- `policy`: tutoring policy identifier.
- `observation_noise`: probability of an observed correctness label being flipped.
- `model_mismatch`: deviation between tutor prior and simulated learner initial mastery.
- `immediate_accuracy`: fraction of in-session responses answered correctly.
- `delayed_transfer_accuracy`: simulated no-hint transfer-probe accuracy after retention decay.
- `mastery_gain`: final post-decay mean latent mastery minus initial mean mastery.
- `hint_count`: number of hint actions.
- `answer_reveal_count`: number of answer-reveal actions.
- `interaction_cost`: total action cost.
- `budget_rejections`: proposed actions blocked by the interaction-budget gate.
- `turns`: number of scored tutoring turns.

## Policy summary (`policy_summary.csv`)
Grouped by profile, policy, observation noise, and model mismatch. Each metric includes mean, standard deviation, and a descriptive 95% normal-approximation interval.

## ASSISTments calibration output
- `skill_id`: source skill identifier.
- `n_interactions`: number of valid records used.
- `correct_rate`: aggregate first-attempt correctness rate.
- `mean_hint_count`: mean reported hint count.
- `mean_attempt_count`: mean reported attempts.
- `median_response_ms`: median first-response time in milliseconds.

No student identifier or free-text response is written to the derived calibration file.
