"""
Adaptive Mutation Controller

This module provides an adaptive mutation mechanism that adjusts mutation probability
based on performance metrics. It includes scheduled mutations to ensure continuous
exploration and prevents the system from becoming stagnant when scores are near
the target threshold.

Usage:
    controller = AdaptiveMutationController(initial_probability=0.1, schedule_interval=5)
    should_mutate = controller.should_mutate(current_score, score_history)
    mutation_prob = controller.get_mutation_probability()
"""

import random
from typing import List, Optional

class AdaptiveMutationController:
    def __init__(
        self,
        initial_probability: float = 0.1,
        min_probability: float = 0.05,
        max_probability: float = 0.5,
        variance_threshold: float = 0.01,
        schedule_interval: int = 5,
        target_score: float = 1.0,
        adaptation_window: int = 10
    ):
        """
        Initialize the Adaptive Mutation Controller.

        Args:
            initial_probability: Starting mutation probability.
            min_probability: Minimum mutation probability.
            max_probability: Maximum mutation probability.
            variance_threshold: Score variance below which mutation prob is increased.
            schedule_interval: Force a mutation every `schedule_interval` iterations.
            target_score: The target score threshold.
            adaptation_window: Number of past scores to consider for variance calculation.
        """
        self.initial_probability = initial_probability
        self.min_probability = min_probability
        self.max_probability = max_probability
        self.variance_threshold = variance_threshold
        self.schedule_interval = schedule_interval
        self.target_score = target_score
        self.adaptation_window = adaptation_window


        self.mutation_probability = initial_probability
        self.iteration_count = 0
        self.last_mutation_iteration = 0
        self.score_history: List[float] = []

    def should_mutate(
        self,
        current_score: Optional[float] = None,
        score_history: Optional[List[float]] = None
    ) -> bool:
        """
        Determine whether to trigger a mutation.

        Args:
            current_score: The latest score from the agent.
            score_history: List of past scores (if not using internal history).

        Returns:
            True if a mutation should occur, False otherwise.
        """
        self.iteration_count += 1

        # Update score history
        if current_score is not None:
            self.score_history.append(current_score)
            if len(self.score_history) > self.adaptation_window:
                self.score_history.pop(0)

        # Check for scheduled mutation
        if self.iteration_count - self.last_mutation_iteration >= self.schedule_interval:
            self.last_mutation_iteration = self.iteration_count
            self._increase_mutation_probability()
            return True

        # Adaptive mutation based on variance
        if self._should_adapt_mutation():
            # If variance is low, increase mutation probability
            self._increase_mutation_probability()
        else:
            # Otherwise, gradually decrease mutation probability
            self._decrease_mutation_probability()

        # Decide whether to mutate based on current probability
        if random.random() < self.mutation_probability:
            self.last_mutation_iteration = self.iteration_count
            return True

        return False

    def _should_adapt_mutation(self) -> bool:
        """
        Check if the score variance is below the threshold, indicating stagnation.

        Returns:
            True if variance is low (stagnation detected), False otherwise.
        """
        if len(self.score_history) < 2:
            return False

        # Calculate variance of recent scores
        mean_score = sum(self.score_history) / len(self.score_history)
        variance = sum((s - mean_score) ** 2 for s in self.score_history) / len(self.score_history)

        return variance < self.variance_threshold

    def _increase_mutation_probability(self):
        """Increase mutation probability towards maximum."""
        self.mutation_probability = min(
            self.mutation_probability * 1.5,
            self.max_probability
        )

    def _decrease_mutation_probability(self):
        """Decrease mutation probability towards minimum."""
        self.mutation_probability = max(
            self.mutation_probability * 0.9,
            self.min_probability
        )

    def get_mutation_probability(self) -> float:
        """Return the current mutation probability."""
        return self.mutation_probability

    def reset(self):
        """Reset the controller to initial state."""
        self.mutation_probability = self.initial_probability
        self.iteration_count = 0
        self.last_mutation_iteration = 0
        self.score_history = []

    def update_config(
        self,
        variance_threshold: Optional[float] = None,
        schedule_interval: Optional[int] = None
    ):
        """
        Update configuration parameters dynamically.

        Args:
            variance_threshold: New variance threshold (optional).
            schedule_interval: New schedule interval (optional).
        """
        if variance_threshold is not None:
            self.variance_threshold = variance_threshold
        if schedule_interval is not None:
            self.schedule_interval = schedule_interval
