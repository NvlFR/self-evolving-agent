class Evaluator:
    def evaluate(self, success: bool, runtime: float, errors: int):
        score = 0

        if success:
            score += 1.0

        score -= runtime * 0.2
        score -= errors * 0.5

        return {
            "success": success,
            "score": score
        }
