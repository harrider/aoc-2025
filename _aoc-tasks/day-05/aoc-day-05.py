"""Advent of Code 2025 - Day 5: Cafeteria"""
from __future__ import annotations
import sys
from typing import List, Tuple, Optional, Set


def parse_input(filepath: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    """Parse the database file into ranges and ingredient IDs."""
    with open(filepath, 'r') as f:
        content = f.read().strip()
    
    parts = content.split('\n\n')
    
    # Parse ranges
    ranges = []
    for line in parts[0].strip().split('\n'):
        start, end = map(int, line.split('-'))
        ranges.append((start, end))
    
    # Parse ingredient IDs
    ingredients = [int(line) for line in parts[1].strip().split('\n')]
    
    return ranges, ingredients


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Merge overlapping ranges into sorted non-overlapping intervals."""
    if not ranges:
        return []
    
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    
    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:  # Overlapping or adjacent
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    
    return merged


def is_fresh(ingredient_id: int, merged_ranges: List[Tuple[int, int]]) -> bool:
    """Binary search to check if ingredient_id falls within any merged range."""
    lo, hi = 0, len(merged_ranges) - 1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        start, end = merged_ranges[mid]
        
        if start <= ingredient_id <= end:
            return True
        elif ingredient_id < start:
            hi = mid - 1
        else:
            lo = mid + 1
    
    return False


def count_fresh(merged: List[Tuple[int, int]], ingredients: List[int]) -> int:
    """Count how many ingredients are fresh (fall within any merged range)."""
    return sum(1 for ing in ingredients if is_fresh(ing, merged))


def count_total_fresh(merged: List[Tuple[int, int]]) -> int:
    """Count total unique fresh IDs across all merged ranges."""
    return sum(end - start + 1 for start, end in merged)


def test_example(parts: Set[int]) -> None:
    """Verify against the puzzle example for specified parts."""
    ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
    ingredients = [1, 5, 8, 11, 17, 32]
    merged = merge_ranges(ranges)
    
    if 1 in parts:
        result = count_fresh(merged, ingredients)
        assert result == 3, f"Part 1 example failed: got {result}, expected 3"
    
    if 2 in parts:
        result = count_total_fresh(merged)
        assert result == 14, f"Part 2 example failed: got {result}, expected 14"


def solve(filepath: str, parts: Set[int]) -> Tuple[Optional[int], Optional[int]]:
    """Solve requested parts. Returns (part1_answer, part2_answer)."""
    ranges, ingredients = parse_input(filepath)
    merged = merge_ranges(ranges)
    
    ans1 = count_fresh(merged, ingredients) if 1 in parts else None
    ans2 = count_total_fresh(merged) if 2 in parts else None
    
    return ans1, ans2


def parse_args() -> Tuple[str, Set[int]]:
    """Parse command-line arguments. Returns (filepath, parts_to_run)."""
    if len(sys.argv) < 2:
        print("Usage: python aoc-day-05.py <input_file> [--part N]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Default: run all parts
    all_parts = {1, 2}
    
    if '--part' in sys.argv:
        idx = sys.argv.index('--part')
        if idx + 1 < len(sys.argv):
            return filepath, {int(sys.argv[idx + 1])}
    
    return filepath, all_parts


def main():
    filepath, parts = parse_args()
    
    # Run example tests for requested parts
    test_example(parts)
    
    # Solve and output requested parts
    ans1, ans2 = solve(filepath, parts)
    
    if ans1 is not None:
        print(f"Part 1: {ans1}")
    
    if ans2 is not None:
        print(f"Part 2: {ans2}")


if __name__ == "__main__":
    main()
