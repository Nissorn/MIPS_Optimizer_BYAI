"""MIPS Assembly Parser Implementation

This module implements the core functionality for parsing MIPS assembly code.
It converts assembly instructions into an intermediate representation that can
be easily manipulated by the optimizer modules.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Set
import re

@dataclass
class Instruction:
    """Represents a single MIPS instruction."""
    opcode: str
    args: List[str]
    comment: Optional[str] = None
    original_text: Optional[str] = None

    def __str__(self) -> str:
        instruction = f"{self.opcode} {', '.join(self.args)}"
        if self.comment:
            instruction = f"{instruction} # {self.comment}"
        return instruction

@dataclass
class Label:
    """Represents a label in the assembly code."""
    name: str
    instruction: Optional[Instruction] = None

    def __str__(self) -> str:
        return f"{self.name}:"

class MIPSParser:
    """Parser for MIPS assembly code."""

    def __init__(self):
        self.labels: Dict[str, Label] = {}
        self.instructions: List[Instruction | Label] = []
        self._initialize_patterns()

    def _initialize_patterns(self) -> None:
        """Initialize regex patterns for parsing."""
        self.label_pattern = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$')
        self.instruction_pattern = re.compile(
            r'^\s*([a-zA-Z]+)\s*([^#]*?)(?:\s*#\s*(.*))?$'
        )
        self.comment_pattern = re.compile(r'^\s*#.*$')

    def parse_file(self, filename: str) -> List[Instruction | Label]:
        """Parse a MIPS assembly file.

        Args:
            filename: Path to the MIPS assembly file.

        Returns:
            List of Instructions and Labels in the order they appear.
        """
        with open(filename, 'r') as f:
            return self.parse_text(f.read())

    def parse_text(self, text: str) -> List[Instruction | Label]:
        """Parse MIPS assembly text.

        Args:
            text: String containing MIPS assembly code.

        Returns:
            List of Instructions and Labels in the order they appear.
        """
        self.instructions.clear()
        self.labels.clear()

        for line in text.splitlines():
            line = line.strip()
            if not line or self.comment_pattern.match(line):
                continue

            # Check for labels
            label_match = self.label_pattern.match(line)
            if label_match:
                label_name, rest = label_match.groups()
                label = Label(label_name)
                self.labels[label_name] = label
                self.instructions.append(label)

                # If there's an instruction on the same line
                if rest.strip():
                    instr = self._parse_instruction(rest)
                    if instr:
                        label.instruction = instr
                        self.instructions.append(instr)
                continue

            # Parse instruction
            instr = self._parse_instruction(line)
            if instr:
                self.instructions.append(instr)

        return self.instructions

    def _parse_instruction(self, line: str) -> Optional[Instruction]:
        """Parse a single instruction line.

        Args:
            line: String containing a single instruction.

        Returns:
            Instruction object if parsing succeeds, None otherwise.
        """
        match = self.instruction_pattern.match(line)
        if not match:
            return None

        opcode, args_str, comment = match.groups()
        args = [arg.strip() for arg in args_str.split(',') if arg.strip()]

        return Instruction(
            opcode=opcode.strip().lower(),
            args=args,
            comment=comment.strip() if comment else None,
            original_text=line
        )

    def get_label(self, name: str) -> Optional[Label]:
        """Get a label by name.

        Args:
            name: Name of the label to retrieve.

        Returns:
            Label object if found, None otherwise.
        """
        return self.labels.get(name)