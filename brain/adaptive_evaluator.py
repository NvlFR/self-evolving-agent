from brain.evaluator import Evaluator

class AdaptiveEvaluator(Evaluator):
    def __init__(self):
        self.history = []
        self.instability_penalty = 0.1
        self.consistency_reward = 0.05

    def evaluate_with_context(self, success: bool, runtime: float, errors: int):
        # Base evaluation
        base_result = self.evaluate(success, runtime, errors)
        score = base_result["score"]

        # Contextual adjustments
        if len(self.history) > 0:
            previous_success = self.history[-1]["success"]
            
            # Penalize instability (success to failure)
            if previous_success and not success:
                score -= self.instability_penalty
            
            # Reward consistency (success to success)
            if previous_success and success:
                score += self.consistency_reward

        result = {
            "success": success,
            "score": max(0.0, score),
            "base_score": base_result["score"]
        }

        self.history.append(result)
        return result

    def get_evolution_trend(self):
        if not self.history:
            return 0.0
        
        scores = [h["score"] for h in self.history]
        if len(scores) < 2:
            return 0.0
            
        return scores[-1] - scores[0]
