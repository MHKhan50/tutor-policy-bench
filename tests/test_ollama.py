import unittest
from tutor_policy_bench.ollama import parse_action_response

class OllamaTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_action_response('{"action":"hint"}'), "hint")
    def test_invalid_action(self):
        self.assertIsNone(parse_action_response('{"action":"delete_student"}'))
    def test_invalid_json(self):
        self.assertIsNone(parse_action_response("not json"))

if __name__ == "__main__":
    unittest.main()
