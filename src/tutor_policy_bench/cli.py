import argparse
from .experiment import DEFAULT_POLICIES, run_experiment
from .ollama import OllamaPolicy

def main():
    parser = argparse.ArgumentParser(description="Run TutorPolicyBench")
    parser.add_argument("--seeds", type=int, default=10)
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--policies", nargs="+", default=list(DEFAULT_POLICIES))
    parser.add_argument("--model", default="qwen2.5:3b")
    parser.add_argument("--ollama-host", default="http://localhost:11434")
    args = parser.parse_args()
    if args.seeds < 1:
        parser.error("--seeds must be >= 1")
    allowed = set(DEFAULT_POLICIES) | {"random", "ollama"}
    unknown = set(args.policies) - allowed
    if unknown:
        parser.error("Unknown policies: " + ", ".join(sorted(unknown)))
    local_policy = OllamaPolicy(args.model, args.ollama_host) if "ollama" in args.policies else None
    # Keep the optional LLM track small by default: one noise/mismatch setting
    # avoids hundreds of local model calls during a quick smoke evaluation.
    if args.policies == ["ollama"]:
        result = run_experiment(args.seeds, args.output_dir, args.policies,
                                noise_levels=(0.10,), mismatch_levels=(0.10,),
                                ollama_policy=local_policy)
    else:
        result = run_experiment(args.seeds, args.output_dir, args.policies,
                                ollama_policy=local_policy)
    print(result)

if __name__ == "__main__":
    main()
