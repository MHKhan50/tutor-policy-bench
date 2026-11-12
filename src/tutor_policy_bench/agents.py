from .model import ACTIONS, ACTION_COST, Observation

def diagnostic_agent(observation):
    """Estimate mastery from a smoothed tutor prior and recent observed outcomes."""
    base = max(0.05, min(0.95, observation.estimated_mastery))
    history = observation.recent_correctness[-5:]
    if history:
        empirical = sum(history) / float(len(history))
        return max(0.05, min(0.95, 0.65 * base + 0.35 * empirical))
    return base

def misconception_agent(observation):
    """Flag a repeated-error pattern; this is a simulator heuristic, not a diagnosis."""
    return observation.recent_errors >= 2 or (
        len(observation.recent_correctness) >= 3 and sum(observation.recent_correctness[-3:]) == 0
    )

def pedagogical_planner(observation):
    mastery = diagnostic_agent(observation)
    if misconception_agent(observation) and mastery < 0.62:
        return "prerequisite_review"
    if mastery < 0.38:
        return "worked_example"
    if mastery < 0.68:
        return "hint"
    return "retrieval_practice"

def progress_evaluator(observation, proposed_action):
    """Validate the proposed action against the allowed action set and budget."""
    if proposed_action not in ACTIONS:
        return "hint"
    if ACTION_COST[proposed_action] > observation.remaining_budget:
        return "retrieval_practice" if observation.remaining_budget >= 1 else "hint"
    if observation.last_correct == 0 and proposed_action == "retrieval_practice":
        return "hint"
    return proposed_action
