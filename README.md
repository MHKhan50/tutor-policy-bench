# TutorPolicyBench

A small simulator for one question: when a tutor (human or AI) has a fixed number of moves, which move should it make next? Give a hint, show a worked example, ask a retrieval question, go back to a prerequisite, or just give the answer?

Most tutoring evaluations score a single reply. This one follows a simulated learner across three sessions with forgetting in between, and scores what they can still do at the end without help.

Everything here is synthetic. The learners, their mastery and their answers come from the assumptions in `src/tutor_policy_bench/simulator.py`. The results say what those assumptions imply, not how real students learn.

## What I found (v0.1.0, 30 seeds)

30 seeds × 3 learner profiles × 3 noise levels × 3 mismatch levels = 810 matched learners per policy. Every policy spends the same budget of 24 cost units and sees the same random draws, so differences come from the moves it picks.

| Policy | Correct during sessions | Correct on delayed test | Mastery gain |
|---|---|---|---|
| direct_answer | 1.000 | 0.425 | −0.022 |
| fixed_hint | 0.679 | 0.667 | 0.219 |
| bkt_threshold | 0.674 | 0.663 | 0.214 |
| multi_agent | 0.647 | 0.671 | 0.224 |
| random | 0.716 | 0.630 | 0.183 |

- Giving the answer every time gets every question right during sessions and the lowest delayed score: 24.6 points below the multi-agent policy (paired 95% interval 23.8 to 25.4). This is built into the simulator, which assumes revealing an answer teaches little, so treat it as a sanity check, not a discovery.
- The adaptive policies did not clearly beat a simple hint rule. Multi-agent minus fixed hint on the delayed test was +0.4 points (−0.1 to +0.9). For novice learners the fixed hint rule was the best of the three.
- Noise and model mismatch hardly moved the ranking. With 25% of answers misread, the three adaptive and hint policies stayed within about 1 point of each other.
- Turning forgetting off raised every delayed score by 8 to 11 points and put `bkt_threshold` first (0.766 against 0.752 for multi-agent). The ranking at the top depends on the decay assumption.

The intervals treat the 810 matched cells as independent even though cells share seeds, so they are descriptive. `outputs/paired_differences.csv` has every comparison.

## Policies

- `direct_answer`: always reveals the answer.
- `fixed_hint`: a hint, or a worked example when the last answer was wrong and at least two of the last five were. Ignores the mastery estimate.
- `bkt_threshold`: Beta-Binomial mastery estimate with thresholds at 0.35 and 0.70.
- `multi_agent`: four rule-based roles (diagnosis, misconception check, planner, budget check). No language model is involved.
- `random`: uniform over the five actions.
- `ollama`: optional, a local model picks the action each turn. Not part of the results above.

## The simulator in short

- 3 maths skills, 3 sessions of 8 turns, budget of 24. Worked examples and prerequisite reviews cost 2, everything else 1.
- Profiles differ in starting mastery (0.25, 0.45, 0.65), learning rate and forgetting per session break.
- Some learners start with a misconception on a skill. It halves learning until a prerequisite review clears it.
- The tutor sees each answer flipped with probability `noise` and starts with a prior that is too optimistic by `mismatch`.
- After the last session the learner forgets once more and answers 5 unaided questions per skill.

Every number is in one block at the top of `simulator.py`, so you can change it and rerun.

## Run it

Python 3.9 or newer, no other packages.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -v
python -m tutor_policy_bench.cli --seeds 30 --policies direct_answer fixed_hint bkt_threshold multi_agent random
python scripts/paired_analysis.py
```

On Windows, activate with `.venv\Scripts\Activate.ps1`.

To let a local model choose the moves (needs Ollama running and the model already pulled):

```bash
python -m tutor_policy_bench.cli --seeds 3 --policies ollama --model qwen2.5:3b
```

## Optional ASSISTments statistics

`scripts/calibrate_assistments.py` reads the public ASSISTments 2009–2010 Skill Builder CSV and writes per-skill averages (correct rate, hints, attempts, response time). It does not set the simulator's parameters and does not measure the effect of hints. Download link and licence notes are in `docs/DATA_AND_PROVENANCE.md`; keep the raw file out of git.

```bash
python scripts/calibrate_assistments.py --input data/raw/skill_builder_data.csv --output data/derived/assistments_skill_priors.csv
```

## Limits

- The simulator is not a validated model of learning. The effect of each action is my assumption.
- The multi-agent policy is rules, not an LLM system.
- Nothing here shows that any tutor helps real students. That needs a study with learners and teachers.
- This is a general benchmark, not mapped to the Pakistani curriculum or to Urdu or Roman Urdu material.

More detail in `docs/`.

## Citation

See `CITATION.cff`. Code is MIT licensed.
