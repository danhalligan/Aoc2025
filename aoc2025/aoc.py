from aocd import models
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any, Union, Callable
import yaml
import re
import functools


class DateException(Exception):
    pass


class Data:
    """
    Access to various input data formats
    """

    def __init__(self, raw: str) -> None:
        self.raw = raw.strip()

    def __str__(self) -> str:
        return self.raw

    def __repr__(self) -> str:
        preview = self.raw[:50] + "..." if len(self.raw) > 50 else self.raw
        return f"Data('{preview}')"

    def lines(self, strip: bool = True) -> List[str]:
        """Get lines from input, optionally stripping whitespace"""
        lines = self.raw.splitlines()
        return [line.strip() if strip else line for line in lines]

    def grep_ints(
        self, per_line: bool = False, signed: bool = True
    ) -> Union[List[int], List[List[int]]]:
        """Extract integers from input, optionally per line"""
        pattern = r"-?\d+" if signed else r"\d+"

        def ints(x: str) -> List[int]:
            return [int(i) for i in re.findall(pattern, x)]

        if per_line:
            return [ints(line) for line in self.lines()]
        else:
            return ints(self.raw)

    def int_array(self, separator=None) -> List[List[int]]:
        """Parse input as 2D array of integers"""
        return [[*map(int, line.split(separator))] for line in self.lines()]

    def char_array(self) -> List[List[str]]:
        """Parse input as 2D array of characters (useful if you need mutability)"""
        return [list(line) for line in self.lines()]

    def grid(self, vtype: Callable[[str], Any] = str) -> Dict[complex, Any]:
        """
        Grid of values with complex number coordinates as dict
        """
        return {
            complex(i, j): vtype(v)
            for j, line in enumerate(self.lines())
            for i, v in enumerate(line)
        }

    def char_grid(self) -> Dict[complex, str]:
        """Convenience method for character grids"""
        return self.grid(str)

    def int_grid(self) -> Dict[complex, int]:
        """Convenience method for integer grids"""
        return self.grid(int)

    def sections(self) -> List["Data"]:
        """Split input on double newlines"""
        return [Data(section) for section in self.raw.split("\n\n")]

    def words(self) -> List[str]:
        """Split input into words"""
        return self.raw.split()

    def chars(self) -> List[str]:
        """Get all characters as a list"""
        return list(self.raw)

    def strip(self) -> "Data":
        """Return new Data with stripped content"""
        return Data(self.raw.strip())


class Example:
    def __init__(
        self,
        data: str,
        a: Any = None,
        b: Any = None,
        args: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.data = Data(data)
        self.val = {"a": a, "b": b}
        self.args = args or {}

    def _test_part(self, part: str, fn: Optional[Callable]) -> bool:
        if fn is not None and self.val[part] is not None:
            try:
                result = fn(self.data, **self.args)
                return str(result) == str(self.val[part])
            except Exception as e:
                print(f"Error running test for part {part}: {e}")
                return False
        return True

    def test_part(self, part: str, fn: Optional[Callable]) -> None:
        """Test a specific part with assertion"""
        if not self._test_part(part, fn):
            expected = self.val[part]
            try:
                actual = fn(self.data, **self.args) if fn else None
                raise AssertionError(
                    f"Part {part} failed: expected {expected}, got {actual}"
                )
            except Exception as e:
                raise AssertionError(f"Part {part} failed with error: {e}")

    def test(self, a: Optional[Callable] = None, b: Optional[Callable] = None) -> None:
        """Test both parts"""
        if a is not None:
            self.test_part("a", a)
        if b is not None:
            self.test_part("b", b)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data.raw,
            "a": self.val["a"],
            "b": self.val["b"],
            "args": self.args,
        }

    @classmethod
    def from_class(cls, x) -> "Example":
        return cls(data=x.input_data, a=x.answer_a, b=x.answer_b)


class Examples:
    def __init__(self, day: int) -> None:
        self.day = day
        self.file = Path(f"tests/data/{day:02d}.yaml")
        self.examples: Optional[List[Example]] = None

    def cached(self) -> bool:
        return self.file.exists()

    def data(self, number: int) -> Data:
        """Get example data by number (1-indexed)"""
        if self.examples is None:
            raise ValueError("Examples not loaded")
        if not (1 <= number <= len(self.examples)):
            raise IndexError(
                f"Example {number} not found (available: 1-{len(self.examples)})"
            )
        return self.examples[number - 1].data

    def count(self) -> int:
        """Get number of examples"""
        return len(self.examples) if self.examples else 0

    def dump(self) -> None:
        """Save examples to YAML file"""
        if self.examples is None:
            return

        # Ensure directory exists
        self.file.parent.mkdir(parents=True, exist_ok=True)

        data = [x.as_dict() for x in self.examples]
        with open(self.file, "w") as yaml_file:
            yaml_file.write(yaml.dump(data, default_style="|"))

    def read(self) -> None:
        """Load examples from YAML file"""
        try:
            with open(self.file) as stream:
                data = yaml.safe_load(stream)
            self.examples = [Example(**x) for x in data or []]
        except Exception as e:
            raise Exception(f"Failed to read examples from {self.file}: {e}")

    def test_part(self, part: str, fn: Callable) -> None:
        """Test all examples for a specific part"""
        if self.examples is None:
            raise ValueError("Examples not loaded")

        for i, example in enumerate(self.examples, 1):
            try:
                example.test_part(part, fn)
                print(f"✓ Example {i} part {part} passed")
            except AssertionError as e:
                print(f"✗ Example {i} part {part} failed: {e}")
                raise

    def test(self, a: Optional[Callable] = None, b: Optional[Callable] = None) -> None:
        """Test all examples for both parts"""
        if self.examples is None:
            raise ValueError("Examples not loaded")

        for i, example in enumerate(self.examples, 1):
            try:
                example.test(a=a, b=b)
                print(f"✓ Example {i} passed")
            except AssertionError as e:
                print(f"✗ Example {i} failed: {e}")
                raise

    def from_class(self, data: List[Any], overwrite: bool = False) -> None:
        """Create examples from aocd puzzle data"""
        self.examples = [Example.from_class(x) for x in data]
        if not self.cached() or overwrite:
            self.dump()

    def load(self, puzzle: Optional["Puzzle"] = None) -> None:
        """Load examples from cache or puzzle"""
        if self.cached():
            self.read()
        elif puzzle is not None:
            try:
                self.from_class(puzzle.puzzle().examples)
            except Exception as e:
                print(f"Warning: Could not load examples from puzzle: {e}")
                self.examples = []
        else:
            raise Exception(
                "Failed to load examples - no cache file and no puzzle provided"
            )


class Puzzle:
    def __init__(
        self, day: Optional[int] = None, year: int = 2025, force: bool = False
    ) -> None:
        self.day = day if day is not None else datetime.today().day
        self.year = year
        self._puzzle: Optional[models.Puzzle] = None
        self._data_cache: Optional[Data] = None

        # Initialize examples
        self.examples = Examples(self.day)

        # Check availability unless forced
        if not force and not self.available():
            raise DateException(
                f"Puzzle for day {self.day} not available until {self.unlock_time()}"
            )

        # Try to load examples
        try:
            self.examples.load(puzzle=self)
        except Exception as e:
            print(f"Warning: Could not load examples: {e}")

    def __repr__(self) -> str:
        return f"Puzzle(day={self.day}, year={self.year})"

    @functools.lru_cache(maxsize=1)
    def puzzle(self) -> models.Puzzle:
        """Get the aocd Puzzle object (cached)"""
        if self._puzzle is None:
            try:
                self._puzzle = models.Puzzle(year=self.year, day=self.day)
            except Exception as e:
                raise Exception(f"Failed to load puzzle for day {self.day}: {e}")
        return self._puzzle

    def unlock_time(self) -> datetime:
        """Get the unlock time for this puzzle"""
        tz = timezone.utc
        return datetime(self.year, 12, self.day, 5, 0, tzinfo=tz)

    def available(self) -> bool:
        """Check if puzzle is available"""
        unlock = self.unlock_time()
        now = datetime.now(timezone.utc)
        return now >= unlock

    def time_until_unlock(self) -> Optional[timedelta]:
        """Get time remaining until puzzle unlocks"""
        if self.available():
            return None
        unlock = self.unlock_time()
        now = datetime.now(timezone.utc)
        return unlock - now

    def data(self, example: Optional[int] = None) -> Data:
        """Get puzzle input data or example data"""
        if example is not None:
            return self.examples.data(example)

        # Cache the main puzzle data
        if self._data_cache is None:
            self._data_cache = Data(self.puzzle().input_data)
        return self._data_cache

    def title(self) -> str:
        """Get puzzle title"""
        return self.puzzle().title

    def url(self) -> str:
        """Get puzzle URL"""
        return f"https://adventofcode.com/{self.year}/day/{self.day}"

    def stats(self) -> Dict[str, Any]:
        """Get puzzle statistics"""
        p = self.puzzle()
        return {
            "title": p.title,
            "day": self.day,
            "year": self.year,
            "url": self.url(),
            "answered_a": p.answered_a,
            "answered_b": p.answered_b,
            "examples_count": self.examples.count(),
        }

    def test(self, a: Optional[Callable] = None, b: Optional[Callable] = None) -> None:
        """Test solutions against examples"""
        print(f"Testing Day {self.day}: {self.title()}")
        self.examples.test(a=a, b=b)
        print("All tests passed! ✓")

    def test_part(self, part: str, fn: Callable) -> None:
        """Test specific part against examples"""
        print(f"Testing Day {self.day} Part {part.upper()}: {self.title()}")
        self.examples.test_part(part, fn)
        print(f"Part {part.upper()} tests passed! ✓")

    def solve_and_submit(
        self,
        part_a: Optional[Callable] = None,
        part_b: Optional[Callable] = None,
        test_first: bool = True,
    ) -> None:
        """Solve and submit answers, optionally testing first"""
        if test_first:
            self.test(a=part_a, b=part_b)

        main_data = self.data()

        if part_a is not None:
            answer_a = part_a(main_data)
            print(f"Part A answer: {answer_a}")
            if input(f"Submit Part A answer '{answer_a}'? (y/N): ").lower() == "y":
                self.submit(a=answer_a)

        if part_b is not None:
            answer_b = part_b(main_data)
            print(f"Part B answer: {answer_b}")
            if input(f"Submit Part B answer '{answer_b}'? (y/N): ").lower() == "y":
                self.submit(b=answer_b)

    def submit(self, a: Any = None, b: Any = None) -> None:
        """Submit answers to AoC"""
        p = self.puzzle()
        if a is not None:
            print(f"Submitting Part A: {a}")
            p.answer_a = a
            print(f"Part A result: {p.answered_a}")
        if b is not None:
            print(f"Submitting Part B: {b}")
            p.answer_b = b
            print(f"Part B result: {p.answered_b}")

    @classmethod
    def today(cls, year: int = 2025) -> "Puzzle":
        """Create puzzle for today"""
        return cls(year=year)

    @classmethod
    def latest_available(cls, year: int = 2025) -> "Puzzle":
        """Get the latest available puzzle"""
        today = datetime.now(timezone.utc)
        dec_start = datetime(year, 12, 1, 5, 0, tzinfo=timezone.utc)

        if today < dec_start:
            raise DateException(f"No puzzles available yet for {year}")

        # Calculate latest available day (max 25)
        days_since_start = (today - dec_start).days
        latest_day = min(days_since_start + 1, 25)

        return cls(day=latest_day, year=year)
