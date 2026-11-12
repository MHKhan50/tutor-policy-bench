"""Synthetic multi-session learner used to compare tutoring policies.

Every number below is an assumption, not a measured property of real students.
They are kept in one place so that sensitivity runs can change them.
"""
import hashlib
import random

from .model import ACTION_COST, LearnerState, Observation
from .policies import choose_action

N_SKILLS = 3
TURNS_PER_SESSION = 8
N_SESSIONS = 3
BUDGET = 24
PROBE_ITEMS = 5          # no-hint transfer items per skill after the delay
PRIOR_STRENGTH = 4.0     # pseudo-observations behind the tutor's prior

# profile: (mean initial mastery, learning rate, decay per session break, chance of a misconception per skill)
PROFILES = {
    "novice": (0.25, 0.10, 0.12, 0.40),
    "intermediate": (0.45, 0.13, 0.09, 0.25),
    "advanced": (0.65, 0.16, 0.06, 0.10),
}

# how much an action props up the answer on the same turn (share of the remaining gap)
SUPPORT = {"hint": 0.25, "worked_example": 0.45, "retrieval_practice": 0.0,
           "prerequisite_review": 0.15, "answer_reveal": 1.0}

# how much an action moves latent mastery, relative to the learner's rate
GAIN = {"hint": 1.0, "worked_example": 1.3, "prerequisite_review": 1.2, "answer_reveal": 0.2}
RETRIEVAL_GAIN = {True: 1.6, False: 0.6}   # retrieval helps most when the learner succeeds
CLEAR_MISCONCEPTION = 0.6                  # chance a prerequisite review removes it


def _clip(x, low=0.02, high=0.98):
    return max(low, min(high, x))


def _stream_rng(seed, profile, noise, mismatch, stream, turn):
    """Separate, reproducible random stream for one kind of draw on one turn.

    Policies are compared on the same streams, so a difference between two policies
    comes from their actions, not from different luck.
    """
    key = "%s|%s|%.4f|%.4f|%s|%s" % (seed, profile, noise, mismatch, stream, turn)
    return random.Random(int(hashlib.sha256(key.encode()).hexdigest()[:16], 16))


def make_learner(seed, profile, noise=0.0, mismatch=0.0):
    if profile not in PROFILES:
        raise ValueError("Unknown profile: " + str(profile))
    mean, rate, decay, p_mis = PROFILES[profile]
    rng = _stream_rng(seed, profile, noise, mismatch, "learner", 0)
    mastery = [_clip(rng.gauss(mean, 0.08)) for _ in range(N_SKILLS)]
    return LearnerState(profile=profile, mastery=list(mastery), initial_mastery=list(mastery),
                        learning_rate=rate, retention_decay=decay,
                        misconception=[rng.random() < p_mis for _ in range(N_SKILLS)],
                        observed_history=[[] for _ in range(N_SKILLS)])


def run_episode(seed, profile, policy, noise=0.10, mismatch=0.15, ollama_policy=None,
                decay_scale=1.0):
    """Run one learner through all sessions with one policy and return its metrics."""
    s = make_learner(seed, profile, noise, mismatch)
    # the tutor believes the learner is stronger than they are by `mismatch`
    prior = [_clip(m + mismatch) for m in s.initial_mastery]
    rejections = 0
    last_action, last_correct = "none", 1

    for turn in range(N_SESSIONS * TURNS_PER_SESSION):
        remaining = BUDGET - s.interaction_cost
        if remaining < 1:
            break
        skill = turn % N_SKILLS
        seen = s.observed_history[skill]
        estimate = (prior[skill] * PRIOR_STRENGTH + sum(seen)) / (PRIOR_STRENGTH + len(seen))
        obs = Observation(turn=turn, skill_id=skill, estimated_mastery=estimate,
                          recent_correctness=seen[-5:], recent_errors=seen[-5:].count(0),
                          observation_noise=noise, model_mismatch=mismatch,
                          remaining_budget=remaining, last_action=last_action,
                          last_correct=last_correct,
                          session_boundary=turn > 0 and turn % TURNS_PER_SESSION == 0)

        if policy == "ollama":
            if ollama_policy is None:
                raise ValueError("policy 'ollama' needs an OllamaPolicy")
            action = ollama_policy.choose(obs)
        else:
            action = choose_action(policy, obs, _stream_rng(seed, profile, noise, mismatch, "policy", turn))

        if ACTION_COST[action] > remaining:
            rejections += 1
            action = "hint"   # cheapest action; remaining >= 1 here
        s.interaction_cost += ACTION_COST[action]
        s.hint_count += action == "hint"
        s.answer_reveal_count += action == "answer_reveal"

        m = s.mastery[skill]
        p_correct = m + SUPPORT[action] * (1 - m)
        correct = _stream_rng(seed, profile, noise, mismatch, "response", turn).random() < p_correct
        s.immediate_correct += correct
        s.scored_turns += 1

        if action == "retrieval_practice":
            gain = RETRIEVAL_GAIN[correct]
        else:
            gain = GAIN[action]
        if s.misconception[skill] and action != "prerequisite_review":
            gain *= 0.5
        if action == "prerequisite_review" and s.misconception[skill]:
            if _stream_rng(seed, profile, noise, mismatch, "clear", turn).random() < CLEAR_MISCONCEPTION:
                s.misconception[skill] = False
        s.mastery[skill] = _clip(m + s.learning_rate * gain * (1 - m))

        flipped = _stream_rng(seed, profile, noise, mismatch, "observation", turn).random() < noise
        seen.append(int(correct != flipped))
        last_action, last_correct = action, int(correct)

        if (turn + 1) % TURNS_PER_SESSION == 0:   # session break, including the final delay
            s.mastery = [_clip(x * (1 - s.retention_decay * decay_scale)) for x in s.mastery]

    probe = _stream_rng(seed, profile, noise, mismatch, "probe", 0)
    transfer = [probe.random() < m for m in s.mastery for _ in range(PROBE_ITEMS)]
    return {
        "seed": seed, "profile": profile, "policy": policy,
        "observation_noise": noise, "model_mismatch": mismatch,
        "immediate_accuracy": s.immediate_correct / max(1, s.scored_turns),
        "delayed_transfer_accuracy": sum(transfer) / len(transfer),
        "mastery_gain": sum(s.mastery) / N_SKILLS - sum(s.initial_mastery) / N_SKILLS,
        "hint_count": s.hint_count, "answer_reveal_count": s.answer_reveal_count,
        "interaction_cost": s.interaction_cost, "budget_rejections": rejections,
        "turns": s.scored_turns,
    }
