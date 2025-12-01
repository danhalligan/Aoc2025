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


[Advent of Code 2025]: https://adventofcode.com/2025
[setup your session ID]: https://github.com/wimglenn/advent-of-code-data/tree/main#quickstart
[`advent-of-code-data`]: https://github.com/wimglenn/advent-of-code-data/
