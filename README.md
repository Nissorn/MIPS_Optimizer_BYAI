# MIPS Code Optimizer

A Python-based MIPS assembly code optimizer that implements various optimization techniques to improve code performance.

## Features

- Peephole Optimization
  - Identifies and replaces inefficient instruction sequences
  - Optimizes common patterns (e.g., add with zero, redundant moves)

- Pipeline Optimization
  - Reorders instructions to minimize pipeline stalls
  - Handles load-use delays and data hazards

- Dead-Code Elimination
  - Removes unused assignments
  - Eliminates unreachable code

- Loop Optimization
  - Basic loop unrolling
  - Branch optimization

- Performance Benchmarking
  - Integration with MARS/SPIM simulators
  - Cycle count measurement and comparison

## Project Structure

```
.
├── src/
│   ├── optimizer/
│   │   ├── __init__.py
│   │   ├── peephole.py
│   │   ├── pipeline.py
│   │   ├── dead_code.py
│   │   └── loop.py
│   ├── parser/
│   │   ├── __init__.py
│   │   └── mips_parser.py
│   └── utils/
│       ├── __init__.py
│       └── instruction_patterns.py
├── tests/
│   ├── __init__.py
│   ├── test_peephole.py
│   ├── test_pipeline.py
│   └── test_dead_code.py
├── examples/
│   ├── simple.s
│   └── loop.s
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- MARS (MIPS Assembler and Runtime Simulator)
- SPIM (Optional)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
# Run optimizer on a MIPS assembly file
python -m src.optimizer input.s -o output.s

# Run tests
python -m pytest tests/
```

## Development Timeline

### Week 1: Basic Framework
- Parse MIPS assembly files
- Implement peephole optimizer

### Week 2: Pipeline Optimization
- Identify and reduce pipeline stalls
- Implement instruction scheduling

### Week 3: Code Reduction
- Implement dead-code elimination
- Optimize branch instructions
- Basic loop unrolling

### Week 4: Testing & Performance
- Run benchmarks
- Measure execution cycles
- Optimize based on results

## Resources

- MIPS Green Sheet
- Computer Organization and Design (Patterson & Hennessy)
- MIPS Assembly Language Programming (Britton)

## License

MIT