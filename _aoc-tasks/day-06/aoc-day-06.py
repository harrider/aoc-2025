"""
Advent of Code 2025 - Day 6: Trash Compactor
Parse a horizontal worksheet of vertical math problems and compute the grand total.
"""
from __future__ import annotations
import argparse
from functools import reduce
from operator import mul
from typing import Callable, List


# Type alias for number extraction functions
NumberExtractor = Callable[[List[str], int, int, int], List[int]]


def parse_worksheet(lines: list[str], extract_numbers: NumberExtractor) -> list[tuple[list[int], str]]:
    """Parse the worksheet into a list of (numbers, operator) tuples."""
    if not lines:
        return []
    
    max_len = max(len(line) for line in lines)
    grid = [line.ljust(max_len) for line in lines]
    num_rows = len(grid)
    
    is_separator = [all(grid[row][col] == ' ' for row in range(num_rows)) 
                    for col in range(max_len)]
    
    problems = []
    col = 0
    
    while col < max_len:
        while col < max_len and is_separator[col]:
            col += 1
        if col >= max_len:
            break
        
        start_col = col
        while col < max_len and not is_separator[col]:
            col += 1
        
        operator = '+' if '+' in grid[-1][start_col:col] else '*'
        numbers = extract_numbers(grid, num_rows, start_col, col)
        
        if numbers:
            problems.append((numbers, operator))
    
    return problems


def extract_numbers_by_row(grid: list[str], num_rows: int, start_col: int, end_col: int) -> list[int]:
    """Extract numbers by reading each row horizontally (left-to-right)."""
    return [int(grid[row][start_col:end_col].strip()) 
            for row in range(num_rows - 1) 
            if grid[row][start_col:end_col].strip().isdigit()]


def extract_numbers_by_column(grid: list[str], num_rows: int, start_col: int, end_col: int) -> list[int]:
    """Extract numbers by reading each column vertically (top-to-bottom), columns processed right-to-left."""
    numbers = []    
    for c in range(end_col - 1, start_col - 1, -1):
        digits = ''.join(grid[row][c] for row in range(num_rows - 1) if grid[row][c].isdigit())
        if digits:
            numbers.append(int(digits))
    return numbers


def solve(lines: list[str], extract_fn: NumberExtractor) -> int:
    """Solve puzzle: parse worksheet and compute grand total."""
    problems = parse_worksheet(lines, extract_fn)
    return sum(sum(nums) if op == '+' else reduce(mul, nums) for nums, op in problems)


def solve_part1(lines: list[str]) -> int:
    return solve(lines, extract_numbers_by_row)


def solve_part2(lines: list[str]) -> int:
    return solve(lines, extract_numbers_by_column)


def run_example_tests(part: int) -> bool:
    """Run example tests from the problem description."""
    example = [
        "123 328  51 64 ",
        " 45 64  387 23 ",
        "  6 98  215 314",
        "*   +   *   +  "
    ]
    
    if part == 1:
        expected = 4277556
        result = solve_part1(example)
        status = "PASS" if result == expected else "FAIL"
        print(f"Example Part 1: {result} (expected {expected}) [{status}]")
        return result == expected
    
    if part == 2:
        expected = 3263827
        result = solve_part2(example)
        status = "PASS" if result == expected else "FAIL"
        print(f"Example Part 2: {result} (expected {expected}) [{status}]")
        return result == expected
    
    return True


def main():
    parser = argparse.ArgumentParser(description="AoC 2025 Day 6: Trash Compactor")
    parser.add_argument("input_file", nargs='?', help="Path to the input file")
    parser.add_argument("--part", type=int, choices=[1, 2], help="Run only the specified part")
    args = parser.parse_args()
    
    if args.part is None or args.part == 1:
        run_example_tests(1)
    if args.part is None or args.part == 2:
        run_example_tests(2)
    
    if not args.input_file:
        return
    
    with open(args.input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    
    if args.part is None or args.part == 1:
        answer1 = solve_part1(lines)
        print(f"Part 1: {answer1}")
    
    if args.part is None or args.part == 2:
        answer2 = solve_part2(lines)
        print(f"Part 2: {answer2}")


if __name__ == "__main__":
    main()
