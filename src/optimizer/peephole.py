"""Peephole Optimizer Implementation

This module implements peephole optimization techniques for MIPS assembly code.
It identifies and replaces inefficient instruction sequences with more optimal ones.
"""

from typing import List, Dict, Tuple, Optional
from ..parser.mips_parser import Instruction, Label

class PeepholeOptimizer:
    """Implements peephole optimization techniques for MIPS code."""

    def __init__(self):
        self._initialize_patterns()

    def _initialize_patterns(self) -> None:
        """Initialize optimization patterns.

        Each pattern is a tuple of (match_function, transform_function)
        where match_function checks if a sequence of instructions matches
        a pattern and transform_function generates the optimized sequence.
        """
        self.patterns = [
            (self._match_add_zero, self._transform_add_zero),
            (self._match_redundant_move, self._transform_redundant_move),
            (self._match_redundant_load_store, self._transform_redundant_load_store)
        ]

    def optimize(self, instructions: List[Instruction | Label]) -> List[Instruction | Label]:
        """Apply peephole optimizations to a sequence of instructions.

        Args:
            instructions: List of Instructions and Labels to optimize.

        Returns:
            Optimized list of Instructions and Labels.
        """
        optimized = []
        i = 0
        while i < len(instructions):
            matched = False
            # Try each pattern on the current instruction sequence
            for match_fn, transform_fn in self.patterns:
                match_length = match_fn(instructions[i:])
                if match_length > 0:
                    # Pattern matched, apply transformation
                    transformed = transform_fn(instructions[i:i + match_length])
                    optimized.extend(transformed)
                    i += match_length
                    matched = True
                    break
            if not matched:
                # No pattern matched, keep original instruction
                optimized.append(instructions[i])
                i += 1
        return optimized

    def _match_add_zero(self, instructions: List[Instruction | Label]) -> int:
        """Match pattern: add rd, rs, $zero → move rd, rs"""
        if len(instructions) < 1:
            return 0
        if not isinstance(instructions[0], Instruction):
            return 0

        instr = instructions[0]
        if (instr.opcode == 'add' and 
            len(instr.args) == 3 and 
            instr.args[2] == '$zero'):
            return 1
        return 0

    def _transform_add_zero(self, instructions: List[Instruction]) -> List[Instruction]:
        """Transform add rd, rs, $zero to move rd, rs"""
        instr = instructions[0]
        return [Instruction(
            opcode='move',
            args=[instr.args[0], instr.args[1]],
            comment=f'Optimized from: {instr.original_text}'
        )]

    def _match_redundant_move(self, instructions: List[Instruction | Label]) -> int:
        """Match pattern: move rd, rs followed by add rd, rs, $zero"""
        if len(instructions) < 2:
            return 0
        if not isinstance(instructions[0], Instruction) or not isinstance(instructions[1], Instruction):
            return 0

        first = instructions[0]
        second = instructions[1]

        # Check if it's a move followed by an add with $zero
        if (first.opcode == 'move' and
            second.opcode == 'add' and
            len(second.args) == 3 and
            second.args[2] == '$zero' and
            first.args[0] == second.args[1]):  # The moved value is used in the add
            return 2
        return 0

    def _transform_redundant_move(self, instructions: List[Instruction]) -> List[Instruction]:
        """Transform redundant move sequence to a single move"""
        # Directly move from the original source to the final destination
        return [Instruction(
            opcode='move',
            args=[instructions[1].args[0], instructions[0].args[1]],
            comment=f'Optimized from: {instructions[0].original_text} and {instructions[1].original_text}'
        )]

    def _match_redundant_load_store(self, instructions: List[Instruction | Label]) -> int:
        """Match pattern: sw reg, offset(base) immediately followed by lw other_reg, offset(base)"""
        if len(instructions) < 2:
            return 0
        if not isinstance(instructions[0], Instruction) or not isinstance(instructions[1], Instruction):
            return 0

        store = instructions[0]
        load = instructions[1]

        if (store.opcode == 'sw' and load.opcode == 'lw' and
            store.args[1] == load.args[1]):  # Same memory location
            return 2
        return 0

    def _transform_redundant_load_store(self, instructions: List[Instruction]) -> List[Instruction]:
        """Transform store followed by load from same location to store + move"""
        store = instructions[0]
        load = instructions[1]
        return [
            store,
            Instruction(
                opcode='move',
                args=[load.args[0], store.args[0]],
                comment=f'Optimized from: {load.original_text}'
            )
        ]