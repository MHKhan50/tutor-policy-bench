# Methodology

## 1. Experimental unit

An episode is a synthetic learner completing mathematics skill interactions over multiple sessions. The learner has latent mastery per skill, a misconception state, a learning-rate parameter, and a retention-decay parameter. The tutor sees only a noisy interaction history and its own estimated learner state.

## 2. Learner profiles

Three configurable profiles are generated: `novice` (lower initial mastery/slower learning), `intermediate` (moderate mastery/learning), and `advanced` (higher mastery/faster learning). These are simulator strata, not demographic categories.

## 3. Actions

The policy chooses `hint`, `worked_example`, `retrieval_practice`, `prerequisite_review`, or `answer_reveal`. Each action has an interaction cost and a distinct assumed effect on immediate response support and latent mastery. The assumptions are explicit in `simulator.py` for sensitivity analysis.

## 4. Multi-agent policy

The `multi_agent` policy is implemented as deterministic roles:
1. Diagnostic role estimates mastery from observed correctness history.
2. Misconception role detects repeated failure patterns.
3. Pedagogical planner chooses an action based on estimated mastery and misconception evidence.
4. Progress evaluator checks recent response outcomes and applies an action/budget gate.

This is an interpretable policy baseline, not a claim that multiple LLM instances are necessary.

## 5. Observation noise and model mismatch

The simulator can flip a fraction of observed correctness outcomes. The tutor's estimated learner prior can differ from the simulated learner's initial mastery. The experiment runner varies noise and mismatch settings to measure policy robustness.

## 6. Delayed retention

At session boundaries, latent mastery decays according to a configurable retention parameter. A final no-hint transfer probe estimates delayed performance from post-decay latent mastery. This is a simulator-defined proxy, not an observed educational outcome.

## 7. Statistical analysis

The runner reports per-episode results and grouped means, standard deviations, and descriptive 95% normal-approximation intervals. For a paper, use paired seed-level comparisons, bootstrap intervals or an appropriate paired test, multiple seeds, and pre-specified hypotheses. The default interval is descriptive and should not be treated as definitive inference.
