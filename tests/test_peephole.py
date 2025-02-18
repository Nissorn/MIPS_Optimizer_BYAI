import pytest
from src.parser.mips_parser import MIPSParser, Instruction
from src.optimizer.peephole import PeepholeOptimizer

@pytest.fixture
def parser():
    return MIPSParser()

@pytest.fixture
def optimizer():
    return PeepholeOptimizer()

def test_add_zero_optimization(parser, optimizer):
    # Test converting 'add rd, rs, $zero' to 'move rd, rs'
    code = """
    add $t0, $s0, $zero
    """
    instructions = parser.parse_text(code)
    optimized = optimizer.optimize(instructions)
    
    assert len(optimized) == 1
    assert optimized[0].opcode == 'move'
    assert optimized[0].args == ['$t0', '$s0']

def test_redundant_move_elimination(parser, optimizer):
    # Test eliminating redundant move instructions
    code = """
    move $t1, $t0
    add $t2, $t1, $zero
    """
    instructions = parser.parse_text(code)
    optimized = optimizer.optimize(instructions)
    
    assert len(optimized) == 1
    assert optimized[0].opcode == 'move'
    assert optimized[0].args == ['$t2', '$t0']

def test_redundant_load_store(parser, optimizer):
    # Test eliminating redundant load after store
    code = """
    sw $t1, 0($sp)
    lw $t2, 0($sp)
    """
    instructions = parser.parse_text(code)
    optimized = optimizer.optimize(instructions)
    
    assert len(optimized) == 2  # Keep store, replace load with move
    assert optimized[0].opcode == 'sw'
    assert optimized[1].opcode == 'move'
    assert optimized[1].args == ['$t2', '$t1']