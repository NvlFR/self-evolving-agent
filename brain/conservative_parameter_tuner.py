"""
ConservativeParameterTuner - SEED Evolution System

A minimal mutation approach that focuses exclusively on fine-tuning
hyperparameters within safe bounds, avoiding structural changes that
may destabilize well-performing architectures.

This tool is based on the observation that the system performs optimally
with no mutations, suggesting the architecture is already well-suited.
Any mutations should be small parameter perturbations only.
"""

import numpy as np
import json
from typing import Dict, List, Any, Optional

class ConservativeParameterTuner:
    """
    A conservative mutation engine that:
    1. NEVER performs structural changes (no layer add/remove/swap)
    2. ONLY adjusts hyperparameters by small amounts
    3. Uses very high thresholds to avoid false-positive stagnation detection
    4. Prioritizes stability over exploration
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # Hyperparameter adjustment bounds (very conservative)
        self.lr_bounds = (0.0001, 0.01)  # Learning rate bounds
        self.lr_perturbation_scale = 0.05  # Only ±5% max change
        
        # Stagnation detection thresholds (high to avoid false positives)
        self.stagnation_window = 50  # Much larger window
        self.stagnation_threshold = 0.001  # Very small threshold
        self.min_improvement_rate = 0.0005  # Minimum improvement rate
        
        # Performance tracking
        self.performance_history: List[float] = []
        self.mutation_history: List[Dict] = []
        
        # Control flags
        self.structural_mutation_enabled = False  # Always disabled
        
    def generate_mutation(self, current_params: Dict[str, Any], 
                        performance: float) -> Dict[str, Any]:
        """
        Generate a mutation only if genuine stagnation is detected.
        Returns empty dict if no mutation needed - this is the preferred
        outcome based on observed system behavior.
        """
        
        self.performance_history.append(performance)
        
        # Always check for stagnation first
        is_stagnant = self._detect_stagnation()
        
        if not is_stagnant:
            # System is improving or stable - no mutation needed
            return {
                'mutate': False,
                'reason': 'system_performing_well',
                'params': current_params
            }
        
        # Only apply hyperparameter mutation if truly stagnant
        mutation = self._generate_conservative_mutation(current_params)
        
        return mutation
    
    def _detect_stagnation(self) -> bool:
        """
        Detect stagnation using a conservative, high-threshold approach.
        Only triggers on sustained, clear stagnation.
        """
        
        if len(self.performance_history) < self.stagnation_window:
            return False
        
        recent_perf = self.performance_history[-self.stagnation_window:]
        
        # Calculate trend
        if len(recent_perf) < 2:
            return False
            
        # Simple linear regression slope
        x = np.arange(len(recent_perf))
        y = np.array(recent_perf)
        
        slope = np.polyfit(x, y, 1)[0]
        
        # Variance check - must have low variance for stagnation
        variance = np.var(recent_perf)
        variance_threshold = self.stagnation_threshold * 10
        
        # Both conditions must be met:
        # 1. Negligible or negative slope
        # 2. Low variance (truly stuck, not just fluctuating)
        
        slope_condition = slope < self.min_improvement_rate
        variance_condition = variance < variance_threshold
        
        return slope_condition and variance_condition
    
    def _generate_conservative_mutation(self, current_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a very conservative hyperparameter mutation.
        Only adjusts learning rate by small amounts.
        """
        
        new_params = current_params.copy()
        mutations_applied = []
        
        # Primary mutation: learning rate adjustment
        current_lr = new_params.get('learning_rate', 0.001)
        
        # Random direction, small magnitude
        direction = np.random.choice([-1, 1])
        lr_change = current_lr * self.lr_perturbation_scale * direction
        
        # Apply change with bounds checking
        new_lr = np.clip(current_lr + lr_change, 
                        self.lr_bounds[0], 
                        self.lr_bounds[1])
        
        if new_lr != current_lr:
            new_params['learning_rate'] = new_lr
            mutations_applied.append({
                'param': 'learning_rate',
                'old': current_lr,
                'new': new_lr,
                'change_pct': (new_lr - current_lr) / current_lr * 100
            })
        
        # Optional: batch size adjustment (only if it's in params)
        if 'batch_size' in current_params:
            current_bs = new_params['batch_size']
            # Small batch size changes (power of 2 adjustment)
            if np.random.random() < 0.3:  # Only 30% chance to adjust
                bs_options = [16, 32, 64, 128]
                if current_bs in bs_options:
                    idx = bs_options.index(current_bs)
                    # Small adjustment (±1 step)
                    new_idx = max(0, min(len(bs_options)-1, idx + np.random.choice([-1, 1])))
                    if bs_options[new_idx] != current_bs:
                        new_params['batch_size'] = bs_options[new_idx]
                        mutations_applied.append({
                            'param': 'batch_size',
                            'old': current_bs,
                            'new': bs_options[new_idx]
                        })
        
        # NO structural mutations - ever
        structural_mutation_attempted = False
        
        return {
            'mutate': len(mutations_applied) > 0,
            'reason': 'genuine_stagnation_detected',
            'params': new_params,
            'mutations': mutations_applied,
            'structural_mutation': structural_mutation_attempted,
            'mutation_type': 'hyperparameter_only'
        }
    
    def get_mutation_summary(self) -> Dict[str, Any]:
        """Return a summary of mutation history."""
        
        total_mutations = len([m for m in self.mutation_history if m.get('mutate', False)])
        structural_attempts = len([m for m in self.mutation_history 
                                   if m.get('structural_mutation', False)])
        
        return {
            'total_iterations': len(self.performance_history),
            'total_mutations_applied': total_mutations,
            'structural_mutations_blocked': structural_attempts,
            'mutation_rate': total_mutations / max(len(self.performance_history), 1),
            'recommendation': 'maintain_stable_config' if total_mutations < 5 else 'tune_conservatively'
        }