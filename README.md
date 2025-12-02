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
puzzle = Puzzle.today()

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
char_grid = data.char_grid()           # Character grid with complex coordinates
sections = data.sections()             # Split on double newlines
words = data.words()                   # Split into words
chars = data.chars()                   # All characters as list
```

### Grid Operations

For 2D grid puzzles, use complex numbers as coordinates:

```python
grid = data.char_grid()  # Returns Dict[complex, str]

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

### Complete Workflow

Use the integrated solve-and-submit workflow:

```python
# This will:
# 1. Test against examples first
# 2. Run on real input
# 3. Ask for confirmation before submitting
puzzle.solve_and_submit(
    part_a=part1, 
    part_b=part2,
    test_first=True  # Default: True
)
```

### Manual Submission

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
puzzle.url()             # Direct link to puzzle
puzzle.stats()           # Comprehensive stats

# Check availability
if puzzle.available():
    print("Puzzle is available!")
else:
    time_left = puzzle.time_until_unlock()
    print(f"Unlocks in: {time_left}")

# Get latest available puzzle
latest = Puzzle.latest_available()
```

### Working with Examples

The system automatically loads and manages example data:

```python
# Check number of examples
print(f"Examples available: {puzzle.examples.count()}")

# Access specific example
example = puzzle.examples.data(1)  # 1-indexed

# Test all examples manually
for i in range(1, puzzle.examples.count() + 1):
    example_data = puzzle.data(example=i)
    result = solve_part1(example_data)
    print(f"Example {i}: {result}")
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
puzzle.solve_and_submit(part_a=part1, part_b=part2)
```

[Advent of Code 2025]: https://adventofcode.com/2025
[setup your session ID]: https://github.com/wimglenn/advent-of-code-data/tree/main#quickstart
[`advent-of-code-data`]: https://github.com/wimglenn/advent-of-code-data/
