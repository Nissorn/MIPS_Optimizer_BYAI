"""MIPS Assembly Parser Module

This module provides functionality for parsing MIPS assembly code into an intermediate
representation that can be used by the optimizer modules.
"""

from .mips_parser import MIPSParser, Instruction, Label

__all__ = ['MIPSParser', 'Instruction', 'Label']