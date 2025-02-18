from src.parser.mips_parser import MIPSParser
from src.optimizer.peephole import PeepholeOptimizer

def main():
    # Initialize the parser and optimizer
    parser = MIPSParser()
    optimizer = PeepholeOptimizer()
    
    # Read the MIPS assembly file
    with open('examples/simple.s', 'r') as f:
        mips_code = f.read()
    
    # Parse the MIPS code
    instructions = parser.parse_text(mips_code)
    
    # Apply optimizations
    optimized_instructions = optimizer.optimize(instructions)
    
    # Print original code
    print('Original MIPS code:')
    print(mips_code)
    print('\nOptimized MIPS code:')
    for instruction in optimized_instructions:
        if hasattr(instruction, 'original_text'):
            print(f'{str(instruction)}  # Original: {instruction.original_text}')
        else:
            print(str(instruction))

if __name__ == '__main__':
    main()