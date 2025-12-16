"""Advent of Code 2025 - Day 07: Laboratories (Tachyon Manifold)"""
from __future__ import annotations
import argparse
from collections import defaultdict


def parse_grid(lines: list[str]) -> tuple[list[str], int, int]:
    """Parse input grid and locate the beam source (S)."""
    grid = [line.rstrip('\n') for line in lines if line.strip()]
    for row, line in enumerate(grid):
        col = line.find('S')
        if col != -1:
            return grid, row, col
    return grid, 0, -1


def count_splits(grid: list[str], start_row: int, start_col: int) -> int:
    """Count total beam splits as beams travel downward through the manifold."""
    if not grid or start_col < 0:
        return 0
    
    cols = len(grid[0])
    active = {start_col}
    splits = 0
    
    for row in grid[start_row + 1:]:
        next_active = set()
        for col in active:
            if row[col] == '^':
                splits += 1
                if col > 0:
                    next_active.add(col - 1)
                if col < cols - 1:
                    next_active.add(col + 1)
            else:
                next_active.add(col)
        active = next_active
        if not active:
            break
    
    return splits


def count_timelines(grid: list[str], start_row: int, start_col: int) -> int:
    """Count total timelines after particle completes all journeys (many-worlds)."""
    if not grid or start_col < 0:
        return 0
    
    cols = len(grid[0])
    # Map column -> number of timelines at that column
    timelines: dict[int, int] = {start_col: 1}
    
    for row in grid[start_row + 1:]:
        next_timelines: dict[int, int] = defaultdict(int)
        for col, count in timelines.items():
            if row[col] == '^':
                # Each timeline splits into 2: one goes left, one goes right
                if col > 0:
                    next_timelines[col - 1] += count
                if col < cols - 1:
                    next_timelines[col + 1] += count
            else:
                # Timeline continues downward
                next_timelines[col] += count
        timelines = next_timelines
        if not timelines:
            break
    
    return sum(timelines.values())


def solve_part1(lines: list[str]) -> int:
    """Solve Part 1: Count total beam splits."""
    grid, start_row, start_col = parse_grid(lines)
    return count_splits(grid, start_row, start_col)


def solve_part2(lines: list[str]) -> int:
    """Solve Part 2: Count total timelines (many-worlds interpretation)."""
    grid, start_row, start_col = parse_grid(lines)
    return count_timelines(grid, start_row, start_col)


def run_example_tests(part: int | None) -> bool:
    """Run example test cases. Returns True if all pass."""
    example = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    
    lines = example.strip().split('\n')
    all_passed = True
    
    if part is None or part == 1:
        result1 = solve_part1(lines)
        expected1 = 21
        status1 = "PASS" if result1 == expected1 else "FAIL"
        print(f"Example Part 1: {result1} (expected {expected1}) [{status1}]")
        if result1 != expected1:
            all_passed = False
    
    if part is None or part == 2:
        result2 = solve_part2(lines)
        expected2 = 40
        status2 = "PASS" if result2 == expected2 else "FAIL"
        print(f"Example Part 2: {result2} (expected {expected2}) [{status2}]")
        if result2 != expected2:
            all_passed = False
    
    return all_passed


def main():
    parser = argparse.ArgumentParser(description="AoC 2025 Day 07: Laboratories")
    parser.add_argument('input_file', nargs='?', help="Path to puzzle input file")
    parser.add_argument('--part', type=int, choices=[1, 2], help="Run only specified part")
    args = parser.parse_args()
    
    # Run example tests
    if not run_example_tests(args.part):
        print("Example tests failed!")
        return
    
    # If no input file, stop after examples
    if not args.input_file:
        return
    
    # Read and solve puzzle input
    with open(args.input_file, 'r') as f:
        lines = f.readlines()
    
    if args.part is None or args.part == 1:
        answer1 = solve_part1(lines)
        print(f"Part 1: {answer1}")
    
    if args.part is None or args.part == 2:
        answer2 = solve_part2(lines)
        print(f"Part 2: {answer2}")


if __name__ == "__main__":
    main()
