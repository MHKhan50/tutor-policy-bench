import random
from .agents import pedagogical_planner, progress_evaluator
from .model import Observation

def choose_action(name, observation, rng=None):
    rng = rng or random.Random(0)
    if name == "direct_answer":
        return "answer_reveal"
    if name == "fixed_hint":
        return "worked_example" if observation.last_correct == 0 and observation.recent_errors >= 2 else "hint"
    if name == "bkt_threshold":
        if observation.estimated_mastery < 0.35:
            return "worked_example"
        if observation.estimated_mastery < 0.70:
            return "hint"
        return "retrieval_practice"
    if name == "multi_agent":
        return progress_evaluator(observation, pedagogical_planner(observation))
    if name == "random":
        return rng.choice(["hint", "worked_example", "retrieval_practice", "prerequisite_review", "answer_reveal"])
    raise ValueError("Unknown policy: " + name)
