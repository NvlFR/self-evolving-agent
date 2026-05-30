class AdaptiveMutator:
    def __init__(self):
        self.stagnation_window = 20
        self.improvement_threshold = 0.01
        self.structural_mutation_enabled = False
        self.fitness_novelty_weight = 0.0
    
    def compute_fitness(self, base_score, novelty=0.0):
        return base_score + (novelty * self.fitness_novelty_weight)

    def select_mutation(self, history):
        if len(history) < self.stagnation_window:
            return None
        recent = history[-self.stagnation_window:]
        if max(recent) - min(recent) < self.improvement_threshold:
            return self._hyperparameter_mutation()
        return None
    
    def _hyperparameter_mutation(self):
        return {"type": "modify_file", "scope": "hyperparameters", "structural": False}