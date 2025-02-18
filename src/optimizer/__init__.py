"""MIPS Code Optimizer Module

This module provides various optimization techniques for MIPS assembly code:
- Peephole optimization
"""

from .peephole import PeepholeOptimizer

__all__ = [
    'PeepholeOptimizer'
]