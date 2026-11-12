import json
import urllib.error
import urllib.request
from .model import ACTIONS

def parse_action_response(raw_text):
    try:
        data = json.loads(raw_text)
    except (TypeError, ValueError):
        return None
    action = data.get("action") if isinstance(data, dict) else None
    return action if action in ACTIONS else None

class OllamaPolicy:
    """Optional local Ollama action selector. No remote API or extra package is used."""
    def __init__(self, model="qwen2.5:3b", host="http://localhost:11434", timeout=45):
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def choose(self, observation):
        context = {
            "turn": observation.turn,
            "estimated_mastery": round(observation.estimated_mastery, 3),
            "recent_correctness": observation.recent_correctness[-5:],
            "recent_errors": observation.recent_errors,
            "last_correct": observation.last_correct,
            "remaining_budget": observation.remaining_budget,
            "session_boundary": observation.session_boundary,
        }
        prompt = (
            "Choose one tutoring action: hint, worked_example, retrieval_practice, "
            "prerequisite_review, answer_reveal. Prefer scaffolding over revealing the answer. "
            "Respect the remaining budget. Return JSON only: {\"action\":\"...\"}.\n"
            + json.dumps(context)
        )
        payload = {"model": self.model, "stream": False, "format": "json", "prompt": prompt}
        request = urllib.request.Request(
            self.host + "/api/generate", data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            raise RuntimeError("Could not obtain a valid response from local Ollama: " + str(exc))
        action = parse_action_response(body.get("response", ""))
        return action if action is not None else "hint"
