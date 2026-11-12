
import unittest

from tutor_policy_bench.simulator import run_episode, _stream_rng


class SimulatorTests(unittest.TestCase):

    def test_metrics_and_budget(self):
        row = run_episode(4, "novice", "multi_agent")

        for key in ("immediate_accuracy", "delayed_transfer_accuracy"):
            self.assertGreaterEqual(row[key], 0.0)
            self.assertLessEqual(row[key], 1.0)

        self.assertLessEqual(row["interaction_cost"], 24)

    def test_deterministic(self):
        self.assertEqual(
            run_episode(12, "intermediate", "bkt_threshold"),
            run_episode(12, "intermediate", "bkt_threshold")
        )

    def test_all_rule_policies_run(self):
        for policy in (
            "direct_answer", "fixed_hint", "bkt_threshold",
            "multi_agent", "random"
        ):
            self.assertGreaterEqual(
                run_episode(2, "advanced", policy)["turns"], 1
            )

    def test_shared_random_streams_are_reproducible(self):
        first = _stream_rng(
            10, "novice", 0.10, 0.15, "response", 4
        )
        second = _stream_rng(
            10, "novice", 0.10, 0.15, "response", 4
        )

        self.assertEqual(
            [first.random() for _ in range(10)],
            [second.random() for _ in range(10)]
        )

    def test_different_turns_have_independent_streams(self):
        first = _stream_rng(
            10, "novice", 0.10, 0.15, "response", 4
        )
        second = _stream_rng(
            10, "novice", 0.10, 0.15, "response", 5
        )

        self.assertNotEqual(
            [first.random() for _ in range(5)],
            [second.random() for _ in range(5)]
        )

    def test_different_stream_types_are_independent(self):
        response = _stream_rng(
            10, "novice", 0.10, 0.15, "response", 4
        )
        observation = _stream_rng(
            10, "novice", 0.10, 0.15, "observation", 4
        )

        self.assertNotEqual(
            [response.random() for _ in range(5)],
            [observation.random() for _ in range(5)]
        )

    def test_unknown_profile_rejected(self):
        with self.assertRaises(ValueError):
            run_episode(1, "unknown", "fixed_hint")


if __name__ == "__main__":
    unittest.main()
