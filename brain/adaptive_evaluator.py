import json
from pathlib import Path


class AdaptiveEvaluator:
    def __init__(self, memory_path="memory/scoring_memory.json"):
        self.memory_path = Path(memory_path)

        if not self.memory_path.exists():
            self.memory_path.write_text(
                json.dumps({
                    "evaluations": []
                }, indent=2)
            )

    def evaluate(self, benchmark_score, mutation_success):
        score = benchmark_score

        if mutation_success:
            score += 0.5
        else:
            score -= 0.5

        result = {
            "benchmark_score": benchmark_score,
            "mutation_success": mutation_success,
            "adaptive_score": score
        }

        self._store(result)

        return result

    def _store(self, result):
        data = json.loads(self.memory_path.read_text())
        data["evaluations"].append(result)

        self.memory_path.write_text(
            json.dumps(data, indent=2)
        )
