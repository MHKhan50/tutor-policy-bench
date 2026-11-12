from dataclasses import dataclass, field
from typing import List

ACTIONS = ("hint", "worked_example", "retrieval_practice", "prerequisite_review", "answer_reveal")
ACTION_COST = {"hint": 1, "worked_example": 2, "retrieval_practice": 1, "prerequisite_review": 2, "answer_reveal": 1}

@dataclass
class LearnerState:
    profile: str
    mastery: List[float]
    initial_mastery: List[float]
    learning_rate: float
    retention_decay: float
    misconception: List[bool]
    observed_history: List[List[int]] = field(default_factory=list)
    interaction_cost: int = 0
    hint_count: int = 0
    answer_reveal_count: int = 0
    immediate_correct: int = 0
    scored_turns: int = 0

@dataclass
class Observation:
    turn: int
    skill_id: int
    estimated_mastery: float
    recent_correctness: List[int]
    recent_errors: int
    observation_noise: float
    model_mismatch: float
    remaining_budget: int
    last_action: str
    last_correct: int
    session_boundary: bool
