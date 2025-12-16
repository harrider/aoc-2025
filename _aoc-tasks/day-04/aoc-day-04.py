"""Advent of Code 2025 - Day 4: Printing Department"""
from typing import List
from collections import deque
import sys

# 8 neighbor directions
DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def parse_grid(lines: List[str]) -> List[str]:
    """Parse input lines into a grid."""
    return [line.strip() for line in lines if line.strip()]


def adjacent_rolls(grid: List[List[str]], r: int, c: int, rows: int, cols: int) -> int:
    """Count paper rolls (@) in the 8 adjacent positions."""
    return sum(
        1 for dr, dc in DIRS
        if 0 <= r + dr < rows and 0 <= c + dc < cols and grid[r + dr][c + dc] == '@'
    )


def is_accessible(grid: List[List[str]], r: int, c: int, rows: int, cols: int) -> bool:
    """Check if a roll at (r,c) is accessible (< 4 adjacent rolls)."""
    return grid[r][c] == '@' and adjacent_rolls(grid, r, c, rows, cols) < 4


def count_accessible_rolls(grid: List[str]) -> int:
    """Count rolls accessible by forklift (fewer than 4 adjacent rolls)."""
    rows, cols = len(grid), len(grid[0])
    mutable_grid = [list(row) for row in grid]
    return sum(
        1 for r in range(rows) for c in range(cols)
        if is_accessible(mutable_grid, r, c, rows, cols)
    )


def count_total_removable(grid: List[str]) -> int:
    """Count total rolls removable using BFS-style propagation. O(n) time."""
    rows, cols = len(grid), len(grid[0])
    mutable_grid = [list(row) for row in grid]
    
    # in_queue[r][c] = True if cell is currently in queue (not yet processed)
    in_queue = [[False] * cols for _ in range(rows)]
    queue = deque()
    
    # Find initial accessible rolls
    for r in range(rows):
        for c in range(cols):
            if mutable_grid[r][c] == '@' and adjacent_rolls(mutable_grid, r, c, rows, cols) < 4:
                queue.append((r, c))
                in_queue[r][c] = True
    
    total = 0
    while queue:
        r, c = queue.popleft()
        in_queue[r][c] = False
        
        # Skip if already removed or no longer accessible
        if mutable_grid[r][c] != '@' or adjacent_rolls(mutable_grid, r, c, rows, cols) >= 4:
            continue
        
        # Remove the roll
        mutable_grid[r][c] = '.'
        total += 1
        
        # Check neighbors - they might now be accessible
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not in_queue[nr][nc]:
                if mutable_grid[nr][nc] == '@' and adjacent_rolls(mutable_grid, nr, nc, rows, cols) < 4:
                    queue.append((nr, nc))
                    in_queue[nr][nc] = True
    
    return total


def test_example():
    """Verify algorithm against puzzle examples."""
    example = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]
    grid = parse_grid(example)
    
    # Part 1 test
    result1 = count_accessible_rolls(grid)
    assert result1 == 13, f"Part 1 example failed: got {result1}, expected 13"
    print(f"Part 1 example passed: {result1}")
    
    # Part 2 test
    result2 = count_total_removable(grid)
    assert result2 == 43, f"Part 2 example failed: got {result2}, expected 43"
    print(f"Part 2 example passed: {result2}")


def solve_part1(grid: List[str]) -> int:
    """Solve Part 1: Count accessible paper rolls."""
    return count_accessible_rolls(grid)


def main():
    if len(sys.argv) < 2:
        print("Usage: python aoc-day-04.py <input_file> [--part N]")
        sys.exit(1)

    input_file = sys.argv[1]
    
    # Parse --part flag
    part = None
    if "--part" in sys.argv:
        idx = sys.argv.index("--part")
        if idx + 1 < len(sys.argv):
            part = int(sys.argv[idx + 1])

    with open(input_file, 'r') as f:
        lines = f.readlines()

    grid = parse_grid(lines)

    # Run tests first
    test_example()

    if part is None or part == 1:
        answer1 = solve_part1(grid)
        print(f"Part 1: {answer1}")

    if part is None or part == 2:
        answer2 = count_total_removable(grid)
        print(f"Part 2: {answer2}")


if __name__ == "__main__":
    main()
