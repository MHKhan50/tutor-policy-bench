import csv
import tempfile
import unittest
from pathlib import Path
from scripts.calibrate_assistments import calibrate

class CalibrationTests(unittest.TestCase):
    def test_aggregates_and_drops_identifiers(self):
        with tempfile.TemporaryDirectory() as temp:
            source, target = Path(temp) / "input.csv", Path(temp) / "out.csv"
            with source.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["user_id", "skill_id", "correct", "hint_count", "attempt_count", "ms_first_response"])
                writer.writeheader()
                writer.writerow({"user_id":"student-a", "skill_id":"S1", "correct":"1", "hint_count":"0", "attempt_count":"1", "ms_first_response":"1000"})
                writer.writerow({"user_id":"student-b", "skill_id":"S1", "correct":"0", "hint_count":"2", "attempt_count":"3", "ms_first_response":"3000"})
            self.assertEqual(calibrate(str(source), str(target)), 1)
            text = target.read_text(encoding="utf-8")
            self.assertNotIn("student-a", text)
            self.assertNotIn("student-b", text)
            self.assertIn("S1", text)

if __name__ == "__main__":
    unittest.main()
