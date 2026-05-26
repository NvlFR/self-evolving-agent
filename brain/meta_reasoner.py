class MetaReasoner:
    def analyze_evolution(self, evolution_history):
        insights = []

        for step in evolution_history:
            if step["benchmark_score"] > 2:
                insights.append(
                    f"Mutation '{step['mutation']}' improved performance"
                )
            else:
                insights.append(
                    f"Mutation '{step['mutation']}' may be ineffective"
                )

        return insights
