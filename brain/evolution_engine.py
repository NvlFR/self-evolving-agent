class EvolutionEngine:
    def __init__(self):
        self.structural_mutation_enabled = False  # DISABLED permanen
        self.hyperparameter_mutation_enabled = True
        self.novelty_weight = 0  # DISABLED - noise source
        self.stagnation_threshold = 50  # epochs without improvement
        self.stagnation_counter = 0
        self.best_fitness_ever = 0.0
        self.mutation_delta_max = 0.05  # max 5% change per mutation
        self.skip_mutation_fitness_threshold = 1.0
        self.exploration_engine_available = False
        self._check_exploration_engine()

    def _check_exploration_engine(self):
        try:
            from brain.exploration_engine import ExplorationEngine
            self.exploration_engine_available = True
        except ImportError:
            self.exploration_engine_available = False

    def should_mutate(self, current_fitness):
        if current_fitness >= self.skip_mutation_fitness_threshold:
            self.stagnation_counter += 1
            if self.stagnation_counter >= self.stagnation_threshold:
                self.stagnation_counter = 0
                return True  # allow mutation only on stagnation
            return False
        return True

    def mutate(self, config):
        if not self.should_mutate(config.get('fitness', 0)):
            return config

        mutated = config.copy()

        # ONLY hyperparameter mutation - NO structural changes
        if self.hyperparameter_mutation_enabled:
            if 'learning_rate' in mutated:
                delta = 1 + (random.random() * 2 - 1) * self.mutation_delta_max
                mutated['learning_rate'] *= delta
                mutated['learning_rate'] = max(1e-6, min(0.1, mutated['learning_rate']))

            if 'batch_size' in mutated:
                choices = [16, 32, 64, 128]
                current = mutated['batch_size']
                nearby = [c for c in choices if abs(c - current) <= 32]
                mutated['batch_size'] = random.choice(nearby) if nearby else current

        # ExplorationEngine guard
        if self.exploration_engine_available:
            try:
                from brain.exploration_engine import ExplorationEngine
                mutated = ExplorationEngine.apply(mutated)
            except Exception:
                pass  # silent fail, use config as-is

        return mutated

    def compute_fitness(self, raw_fitness, novelty_score=0):
        # novelty_weight = 0, ignore novelty completely
        return raw_fitness  # pure fitness, no noise