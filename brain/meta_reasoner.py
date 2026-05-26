class MetaReasoner:
    def analyze_evolution(self, evolution_history):
        if not evolution_history:
            return ["No evolution history to analyze."]

        insights = []
        
        # Calculate trend
        scores = [step["benchmark_score"] for step in evolution_history]
        trend = scores[-1] - scores[0]
        
        if trend > 0:
            insights.append(f"Overall evolution trend is positive (+{trend:.2f}). System is improving.")
        elif trend < 0:
            insights.append(f"Overall evolution trend is negative ({trend:.2f}). System is degrading.")
        else:
            insights.append("Evolution trend is flat. No significant change in performance.")

        # Find best mutation
        best_step = max(evolution_history, key=lambda x: x["benchmark_score"])
        insights.append(f"Most successful mutation: '{best_step['mutation']}' with score {best_step['benchmark_score']:.2f}")

        # Count accepted/rejected
        rejected = sum(1 for step in evolution_history if step["benchmark_score"] < 0.5)
        accepted = len(evolution_history) - rejected
        insights.append(f"Generations: {len(evolution_history)} total. {accepted} accepted, {rejected} rejected.")

        return insights
