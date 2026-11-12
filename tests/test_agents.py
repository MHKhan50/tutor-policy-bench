import unittest
from tutor_policy_bench.agents import misconception_agent, pedagogical_planner, progress_evaluator
from tutor_policy_bench.model import Observation

class AgentTests(unittest.TestCase):
    def test_planner_action(self):
        obs = Observation(3, 0, 0.2, [0, 0, 0], 3, 0.1, 0.0, 10, "hint", 0, False)
        self.assertIn(pedagogical_planner(obs), ("hint", "worked_example", "retrieval_practice", "prerequisite_review", "answer_reveal"))

    def test_misconception_heuristic(self):
        obs = Observation(3, 0, 0.3, [0, 0, 0], 3, 0.0, 0.0, 10, "hint", 0, False)
        self.assertTrue(misconception_agent(obs))

    def test_budget_gate(self):
        obs = Observation(3, 0, 0.2, [0, 0], 2, 0.0, 0.0, 1, "hint", 0, False)
        self.assertEqual(progress_evaluator(obs, "worked_example"), "retrieval_practice")

if __name__ == "__main__":
    unittest.main()
