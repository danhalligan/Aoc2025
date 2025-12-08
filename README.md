# AoC2025

![CI workflow](https://github.com/danhalligan/AoC2025/actions/workflows/ci.yaml/badge.svg)
![License](https://img.shields.io/github/license/danhalligan/AoC2025)
![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)

`AoC2025` is a python package implementing solutions python solutions for the
[Advent of Code 2025] problems.

## Example

First you need to [setup your session ID] as this package uses 
[`advent-of-code-data`] to retrieve the data input.

To solve all days (where available) run:

``` bash
poetry run aoc2025
```

Or to solve specific day(s) (e.g. days 1 and 5):

``` bash
poetry run aoc2025 1 5
```

## Using the Puzzle Class

The `Puzzle` class provides an interface for working with Advent of Code puzzles. Here's how to use it:

### Basic Usage

```python
from aoc2025.aoc import Puzzle

# Create puzzle for today's date
puzzle = Puzzle()

# Create puzzle for a specific day
puzzle = Puzzle(day=1)
```

### Working with Input Data

The `Data` class provides convenient methods for parsing input:

```python
# Get the main puzzle input
data = puzzle.data()

# Get example data (1-indexed)
example1 = puzzle.data(example=1)

# Parse input in various formats
lines = data.lines()                    # List of lines
numbers = data.grep_ints()             # Extract all integers
per_line_nums = data.grep_ints(per_line=True)  # Integers per line
int_matrix = data.int_array()          # 2D array of integers
char_matrix = data.char_array()        # 2D array of characters
grid = data.grid()                     # Grid with complex coordinates (default: str)
int_grid = data.grid(int)              # Grid with integer values
sections = data.sections()             # Split on double newlines
```

### Grid Operations

For 2D grid puzzles, use complex numbers as coordinates:

```python
grid = data.grid()  # Returns Dict[complex, str] by default

# Access grid positions
top_left = grid[0+0j]
position = grid[3+2j]  # x=3, y=2

# Iterate through grid
for pos, char in grid.items():
    x, y = int(pos.real), int(pos.imag)
    print(f"Position ({x}, {y}): {char}")
```

### Testing Solutions

Test your solutions against provided examples:

```python
def part1(data):
    # Your solution here
    return result

def part2(data):
    # Your solution here  
    return result

# Test individual parts
puzzle.test_part("a", part1)
puzzle.test_part("b", part2)

# Test both parts together
puzzle.test(a=part1, b=part2)
```

### Submission

For manual control over submission:

```python
# Run your solution
answer_a = part1(puzzle.data())
answer_b = part2(puzzle.data())

# Submit answers
puzzle.submit(a=answer_a)
puzzle.submit(b=answer_b)
# or both at once:
puzzle.submit(a=answer_a, b=answer_b)
```

### Utility Methods

```python
# Get puzzle information
puzzle.title()           # Puzzle title

# Check availability
if puzzle.available():
    print("Puzzle is available!")
else:
    unlock_time = puzzle.unlock_time()
    print(f"Unlocks at: {unlock_time}")
```

### Working with Examples

The system automatically loads and manages example data:

```python
# Access specific example
example = puzzle.examples.data(1)  # 1-indexed

# Test all examples manually
if puzzle.examples.examples:  # Check if examples are loaded
    for i in range(1, len(puzzle.examples.examples) + 1):
        example_data = puzzle.data(example=i)
        result = part1(example_data)
        print(f"Example {i}: {result}")
```

### Error Handling

The system provides helpful error messages:

```python
try:
    puzzle = Puzzle(day=15)  # Future day
except DateException as e:
    print(f"Puzzle not available: {e}")
```

### Advanced Data Parsing

```python
# Custom separator for int arrays
int_matrix = data.int_array(separator=',')

# Custom grid with integer values
int_grid = data.grid(int)

# Work with input sections
sections = data.sections()
header = sections[0]
body = sections[1]
```

### Example Complete Solution

```python
from aoc2025.aoc import Puzzle

def part1(data):
    numbers = data.grep_ints()
    return sum(numbers)

def part2(data):
    lines = data.lines()
    return len(lines)

# Create puzzle and solve
puzzle = Puzzle(day=1)

# Test with examples
puzzle.test(a=part1, b=part2)

# Run on real data
data = puzzle.data()
answer1 = part1(data)
answer2 = part2(data)

# Submit answers
puzzle.submit(a=answer1, b=answer2)
```

[Advent of Code 2025]: https://adventofcode.com/2025
[setup your session ID]: https://github.com/wimglenn/advent-of-code-data/tree/main#quickstart
[`advent-of-code-data`]: https://github.com/wimglenn/advent-of-code-data/
