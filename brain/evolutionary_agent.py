# MODIFIKASI PADA adaptive_mutator - GANTI DENGAN EXPLORATION ENGINE

# TAMBAHKAN IMPOR BARU
from brain.exploration_engine import ExplorationEngine, ExplorationConfig

# MODIFIKASI INIT
def __init__(self, ...):
    # ... existing code ...
    
    # INISIALISASI EXPLORATION ENGINE - GANTI ADAPTIVE MUTATOR
    exploration_config = ExplorationConfig(
        enable_structural_mutation=False,  # MATI - sumber masalah
        enable_hyperparam_exploration=True,
        diversity_threshold=0.3,
        exploration_rate=0.1,
        mutation_amplitude=0.05
    )
    self.exploration_engine = ExplorationEngine(exploration_config)
    
    # THRESHOLD UNTUK AUTO-DISABLE MUTATION
    self.mutation_disable_threshold = 1.0  # Skor di atas ini = disable mutation

# MODIFIKASI adaptive_mutator
def adaptive_mutator(self, agent_config: Dict, iteration: int, current_fitness: float) -> Dict:
    """
    ADAPTIVE MUTATOR - DIMODIFIKASI TOTAL
    
    Filosofi baru: JANGAN mutate arsitektur yang sudah optimal.
    Mutation hanya dilakukan saat:
    1. Diversity population rendah
    2. Fitness stagnasi terdeteksi
    3. Exploration engine memutuskan perlu
    
    Mutation yang dilakukan: HANYA hyperparameter, BUKAN structural.
    """
    
    # GUARD: Jika sudah di atas threshold, JANGAN mutate apapun
    if current_fitness >= self.mutation_disable_threshold:
        return {
            'mutated_config': agent_config,
            'mutation_type': 'none',
            'reason': f'Score {current_fitness:.2f} >= {self.mutation_disable_threshold}. Preserve optimal architecture.',
            'blocked': True
        }
    
    # BUILD AGENT STATE UNTUK DECISION MAKING
    agent_state = {
        'architecture': agent_config.get('architecture', {}),
        'hyperparameters': agent_config.get('hyperparameters', {}),
        'generation': iteration
    }
    
    # GUNAKAN EXPLORATION ENGINE
    exploration_decision = self.exploration_engine.decide_exploration_action(
        agent_state=agent_state,
        fitness=current_fitness
    )
    
    if exploration_decision['action'] == 'no_mutation':
        return {
            'mutated_config': agent_config,
            'mutation_type': 'none',
            'reason': exploration_decision['reason'],
            'blocked': True
        }
    
    # EXECUTE HYPERPARAMETER MUTATION ONLY
    mutated_config = self.exploration_engine.execute_mutation(
        agent_config=agent_config,
        mutation_proposal=exploration_decision
    )
    
    proposed_changes = exploration_decision.get('proposed_changes', {})
    hyperparam_mutations = proposed_changes.get('hyperparam_mutations', {})
    
    return {
        'mutated_config': mutated_config,
        'mutation_type': 'hyperparameter_only',
        'hyperparam_mutations': hyperparam_mutations,
        'reason': exploration_decision['reason'],
        'diversity_score': exploration_decision.get('diversity_score', 0)
    }

# TAMBAHKAN METHOD UNTUK REPORTING
def get_exploration_report(self) -> Dict:
    """Get exploration engine status report."""
    if hasattr(self, 'exploration_engine'):
        return self.exploration_engine.report()
    return {'status': 'exploration_engine_not_initialized'}
