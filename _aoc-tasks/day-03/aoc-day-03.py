"""Advent of Code 2025 - Day 3: Lobby"""
from __future__ import annotations
import sys


def max_joltage(bank: str) -> int:
    """Find maximum 2-digit joltage from a bank using O(n) time, O(1) space.
    
    Right-to-left pass: track the max digit seen so far (potential ones digit),
    and at each position compute the best 2-digit number using current as tens.
    """
    max_after = 0
    best = 0
    
    for i in range(len(bank) - 1, -1, -1):
        digit = int(bank[i])
        if max_after > 0:  # Need at least one digit after current position
            candidate = 10 * digit + max_after
            best = max(best, candidate)
        max_after = max(max_after, digit)
    
    return best


def solve_part1(lines: list[str]) -> int:
    """Sum of maximum joltage from each battery bank."""
    return sum(max_joltage(line) for line in lines)


def max_joltage_k(bank: str, k: int) -> int:
    """Find maximum k-digit joltage using monotonic stack. O(n) time, O(k) space.
    
    Equivalent to removing (n-k) digits to maximize the result. Use a stack:
    pop smaller digits when a larger one arrives (if removals remain).
    """
    n = len(bank)
    to_remove = n - k
    stack = []
    
    for char in bank:
        digit = int(char)
        # Pop smaller digits if we still have removals left
        while stack and stack[-1] < digit and to_remove > 0:
            stack.pop()
            to_remove -= 1
        stack.append(digit)
    
    # If we haven't removed enough (e.g., descending sequence), truncate
    stack = stack[:k]
    
    # Convert stack to integer
    result = 0
    for d in stack:
        result = result * 10 + d
    return result


def solve_part2(lines: list[str]) -> int:
    """Sum of maximum 12-digit joltage from each battery bank."""
    return sum(max_joltage_k(line, 12) for line in lines)


def run_tests() -> bool:
    """Verify against puzzle examples."""
    example = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    
    # Individual bank tests
    assert max_joltage("987654321111111") == 98, "Bank 1 should be 98"
    assert max_joltage("811111111111119") == 89, "Bank 2 should be 89"
    assert max_joltage("234234234234278") == 78, "Bank 3 should be 78"
    assert max_joltage("818181911112111") == 92, "Bank 4 should be 92"
    
    # Total test
    assert solve_part1(example) == 357, "Total should be 357"
    
    # Part 2 tests
    assert max_joltage_k("987654321111111", 12) == 987654321111, "Bank 1 P2"
    assert max_joltage_k("811111111111119", 12) == 811111111119, "Bank 2 P2"
    assert max_joltage_k("234234234234278", 12) == 434234234278, "Bank 3 P2"
    assert max_joltage_k("818181911112111", 12) == 888911112111, "Bank 4 P2"
    assert solve_part2(example) == 3121910778619, "Part 2 total"
    
    print("All tests passed!")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python aoc-day-03.py <input_file> [--part N]")
        sys.exit(1)
    
    # Parse arguments
    input_file = sys.argv[1]
    part = None
    if "--part" in sys.argv:
        idx = sys.argv.index("--part")
        if idx + 1 < len(sys.argv):
            part = int(sys.argv[idx + 1])
    
    # Run tests first
    if not run_tests():
        sys.exit(1)
    
    # Read input
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Solve
    if part is None or part == 1:
        result1 = solve_part1(lines)
        print(f"Part 1: {result1}")
    
    if part is None or part == 2:
        result2 = solve_part2(lines)
        print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
