#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 14:02:07 2026

"""

import numpy as np
import random

class MovementGenerator:
    """
    A class to generate synthetic trajectory data for various movement patterns.
    
    Attributes:
        seq_length (int): Number of time steps for each generated trajectory.
    """
    
    def __init__(self, seq_length=100):
        self.seq_length = seq_length
        self.patterns = ['prw', 'levy', 'confined', 'persistent']

    def _generate_prw(self):
        """Generates a Pure Random Walk (PRW) trajectory using Pareto distributed step lengths."""
        steps = self.seq_length - 1
        alpha = random.randint(27, 35) / 10
        step_lengths = (np.random.pareto(alpha, steps) + 1) * 1.5
        angles = np.random.uniform(0, 2 * np.pi, steps)
        
        dx = step_lengths * np.cos(angles)
        dy = step_lengths * np.sin(angles)
        
        traj = np.zeros((self.seq_length, 2))
        traj[1:, 0] = np.cumsum(dx)
        traj[1:, 1] = np.cumsum(dy)
        return traj

    def _generate_levy(self):
        """Generates a Levy Walk trajectory with occasional pauses."""
        alpha = random.randint(11, 15) / 10
        pause_prob = random.randint(80, 95) / 100
        
        traj = np.zeros((self.seq_length, 2))
        for i in range(1, self.seq_length):
            if np.random.random() < pause_prob:
                step_length = 0.5
            else:
                u = np.random.random()
                step_length = np.clip((1 - u) ** (-1 / (alpha - 1)), 0.1, 20)
            
            direction = np.random.uniform(0, 2 * np.pi)
            traj[i] = traj[i-1] + step_length * np.array([np.cos(direction), np.sin(direction)])
        return traj

    def _generate_confined(self):
        """Generates a confined motion trajectory oscillating around a center point."""
        traj = np.zeros((self.seq_length, 2))
        radius, persistence = 3.0, 0.2
        theta = 2 * np.pi * np.random.random()
        
        for i in range(1, self.seq_length):
            theta += (1 - persistence) * np.pi * np.random.randn()
            proposal = traj[i-1] + 1.0 * np.array([np.cos(theta), np.sin(theta)])
            
            if np.linalg.norm(proposal) <= radius:
                traj[i] = proposal
            else:
                traj[i] = traj[i-1] # Stay within boundaries
        return traj

    def _generate_persistent(self):
        """Generates a persistent motion trajectory with correlated direction changes."""
        traj = np.zeros((self.seq_length, 2))
        direction = np.random.uniform(0, 2 * np.pi)
        sigma = random.uniform(0.0, 0.3)
        
        for j in range(1, self.seq_length):
            direction += np.random.normal(0, sigma)
            # Add small random perturbation to the motion
            traj[j] = traj[j-1] + 1.0 * np.array([np.cos(direction), np.sin(direction)]) + \
                      np.random.normal(0, 0.2, 2)
        return traj

    def generate_dataset(self, num_samples):
        """
        Generates a synthetic dataset of trajectories.
        
        Returns:
            X (np.ndarray): Array of shape (num_samples, seq_length, 2)
            y (np.ndarray): Array of labels for each trajectory
        """
        X, y = [], []
        for i in range(num_samples):
            pattern = self.patterns[i % 4]
            
            if pattern == 'prw': traj = self._generate_prw()
            elif pattern == 'levy': traj = self._generate_levy()
            elif pattern == 'confined': traj = self._generate_confined()
            elif pattern == 'persistent': traj = self._generate_persistent()
            
            X.append(traj)
            y.append(pattern)
            
        return np.array(X), np.array(y)

# Example Usage:
if __name__ == "__main__":
    generator = MovementGenerator(seq_length=200)
    X, y = generator.generate_dataset(num_samples=1000)
    print(f"Generated data shape: {X.shape}")