"""
Adaptive Mutation Engine for SEED Evolution System
VERSION 2.0 - Conservative Configuration

CHANGES FROM v1.0:
- Default: enabled=False (must be explicitly enabled by user)
- stagnation_window: 20 (was 5) - only mutate after prolonged stagnation
- base_mutation_rate: 0.02 (was 0.05) - gentler perturbations
- burst_scale: 1.2 (was 2.0) - less aggressive bursts
- novelty_weight: 0.05 (was 0.2) - reduced noise in fitness signals
"""

import numpy as np
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AdaptiveMutator:
    """
    Adaptive mutation engine that responds to performance stagnation.
    NOW DISABLED BY DEFAULT - Must set enabled=True to activate.
    """
    
    def __init__(
        self,
        enabled: bool = False,  # CHANGED: Default to disabled
        stagnation_window: int = 20,  # CHANGED: Was 5
        base_mutation_rate: float = 0.02,  # CHANGED: Was 0.05
        burst_scale: float = 1.2,  # CHANGED: Was 2.0
        novelty_weight: float = 0.05,  # CHANGED: Was 0.2
        min_fitness_delta: float = 0.001,
        history_size: int = 50
    ):
        self.enabled = enabled
        self.stagnation_window = stagnation_window
        self.base_mutation_rate = base_mutation_rate
        self.burst_scale = burst_scale
        self.novelty_weight = novelty_weight
        self.min_fitness_delta = min_fitness_delta
        
        self.fitness_history = []
        self.mutation_history = []
        self.epoch = 0
        self.consecutive_stagnant = 0
        
        if self.enabled:
            logger.info(
                f"AdaptiveMutator ENABLED (conservative mode): "
                f"stagnation_window={stagnation_window}, "
                f"base_mutation_rate={base_mutation_rate}, "
                f"burst_scale={burst_scale}, "
                f"novelty_weight={novelty_weight}"
            )
        else:
            logger.info(
                "AdaptiveMutator DISABLED by default. "
                "Set enabled=True in config to activate."
            )
    
    def should_mutate(self, current_fitness: float) -> bool:
        """
        Determine if mutation should be applied based on stagnation detection.
        Returns False (no mutation) if disabled.
        """
        if not self.enabled:
            return False
            
        self.epoch += 1
        self.fitness_history.append(current_fitness)
        
        if len(self.fitness_history) < 2:
            return False
        
        # Calculate recent fitness improvement
        recent_window = min(self.stagnation_window, len(self.fitness_history))
        recent_fitness = self.fitness_history[-recent_window:]
        
        if len(recent_fitness) >= 2:
            max_fitness = max(recent_fitness)
            min_fitness = min(recent_fitness[:recent_window//2 + 1])
            improvement = (max_fitness - min_fitness) / (abs(min_fitness) + 1e-8)
            
            if improvement < self.min_fitness_delta:
                self.consecutive_stagnant += 1
            else:
                self.consecutive_stagnant = 0
        
        should_mutate = self.consecutive_stagnant >= self.stagnation_window
        
        if should_mutate:
            self.consecutive_stagnant = 0
            logger.warning(
                f"Stagnation detected for {self.stagnation_window} epochs. "
                f"Mutation will be applied."
            )
        
        return should_mutate
    
    def calculate_mutation_rate(self, diversity_score: float = 0.5) -> float:
        """
        Calculate adaptive mutation rate based on diversity and stagnation.
        Returns base rate if disabled.
        """
        if not self.enabled:
            return 0.0
            
        # Lower mutation when diversity is healthy
        diversity_factor = 1.0 - (diversity_score * 0.5)
        
        # Higher mutation during stagnation
        stagnation_factor = 1.0 + (self.consecutive_stagnant / self.stagnation_window) * 0.5
        
        rate = (
            self.base_mutation_rate 
            * diversity_factor 
            * min(stagnation_factor, self.burst_scale)
        )
        
        return min(rate, 0.15)  # Cap at 15%
    
    def calculate_fitness_with_novelty(
        self, 
        base_fitness: float, 
        novelty_score: float
    ) -> float:
        """
        Blend base fitness with novelty signal.
        Returns base fitness if disabled.
        """
        if not self.enabled:
            return base_fitness
            
        return base_fitness + (novelty_score * self.novelty_weight)
    
    def get_config(self) -> Dict[str, Any]:
        """Return current configuration."""
        return {
            "enabled": self.enabled,
            "stagnation_window": self.stagnation_window,
            "base_mutation_rate": self.base_mutation_rate,
            "burst_scale": self.burst_scale,
            "novelty_weight": self.novelty_weight,
            "min_fitness_delta": self.min_fitness_delta,
            "epoch": self.epoch,
            "consecutive_stagnant": self.consecutive_stagnant
        }
    
    def reset(self):
        """Reset mutation engine state."""
        self.fitness_history = []
        self.mutation_history = []
        self.epoch = 0
        self.consecutive_stagnant = 0
