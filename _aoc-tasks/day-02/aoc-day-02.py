"""
Advent of Code 2025 - Day 2: Gift Shop

Part 1: Invalid IDs are patterns repeated exactly twice (e.g., 123123).
Part 2: Invalid IDs are patterns repeated at least twice (e.g., 123123, 111, 121212).

Key insight: A number with n digits formed by repeating a k-digit base r times
(where r = n/k >= 2) equals base * M where M = (10^n - 1) / (10^k - 1).
"""
from __future__ import annotations
import sys
from math import ceil
from typing import List, Tuple, Optional, Set


def get_repetition_multiplier(k: int, r: int) -> int:
    """
    Get the multiplier M for a k-digit base repeated r times.
    M = 10^(k*(r-1)) + 10^(k*(r-2)) + ... + 10^k + 1 = (10^(k*r) - 1) / (10^k - 1)
    """
    return (10 ** (k * r) - 1) // (10 ** k - 1)


def get_base_bounds_for_repetition(k: int, r: int, start: int, end: int) -> Optional[Tuple[int, int, int]]:
    """
    Get range of k-digit bases that, when repeated r times, fall within [start, end].
    Returns (base_min, base_max, multiplier) or None if no valid bases exist.
    """
    M = get_repetition_multiplier(k, r)
    
    # k-digit bases: 10^(k-1) to 10^k - 1 (or 1-9 for k=1)
    base_lo = 1 if k == 1 else 10 ** (k - 1)
    base_hi = 10 ** k - 1
    
    # Clamp to bases whose repeated form falls in [start, end]
    base_min = max(base_lo, ceil(start / M))
    base_max = min(base_hi, end // M)
    
    return (base_min, base_max, M) if base_min <= base_max else None


# ============ Part 1: Pattern repeated exactly twice ============

def sum_invalid_ids_in_range(start: int, end: int) -> int:
    """Sum all invalid IDs (pattern repeated exactly twice) within [start, end]."""
    total = 0
    max_k = (len(str(end)) + 1) // 2
    
    for k in range(1, max_k + 1):
        bounds = get_base_bounds_for_repetition(k, 2, start, end)
        if bounds:
            base_min, base_max, M = bounds
            count = base_max - base_min + 1
            total += M * count * (base_min + base_max) // 2
    
    return total


def find_invalid_ids_in_range(start: int, end: int) -> List[int]:
    """List all Part 1 invalid IDs within [start, end]. Used for testing."""
    ids = []
    max_k = (len(str(end)) + 1) // 2
    
    for k in range(1, max_k + 1):
        bounds = get_base_bounds_for_repetition(k, 2, start, end)
        if bounds:
            base_min, base_max, M = bounds
            ids.extend(base * M for base in range(base_min, base_max + 1))
    
    return ids


# ============ Part 2: Pattern repeated at least twice ============

def is_primitive_base(base: int) -> bool:
    """
    Check if base is primitive (not itself a repeated pattern).
    A primitive base ensures we count each invalid ID exactly once.
    E.g., 123 is primitive, but 1212 is not (it's 12 repeated).
    """
    s = str(base)
    length = len(s)
    for k in range(1, length // 2 + 1):
        if length % k == 0:
            pattern = s[:k]
            if pattern * (length // k) == s:
                return False  # base is itself a repeated pattern
    return True


def is_repeated_pattern(n: int) -> bool:
    """Check if n is formed by repeating some pattern at least twice."""
    s = str(n)
    length = len(s)
    for k in range(1, length // 2 + 1):
        if length % k == 0:
            pattern = s[:k]
            r = length // k
            if r >= 2 and pattern * r == s:
                return True
    return False


def sum_invalid_ids_part2_in_range(start: int, end: int) -> int:
    """
    Sum all Part 2 invalid IDs within [start, end].
    
    Strategy: Only count numbers formed by repeating PRIMITIVE bases.
    This avoids double-counting since each invalid ID has exactly one
    primitive base (the smallest repeating unit).
    
    For each (k, r) where k is pattern length and r >= 2 is repetitions:
    - Generate candidate bases in range
    - Filter to primitive bases only
    - Use closed-form sum for the primitives
    
    Complexity: O(max_digits^2 * range_of_bases_per_combo)
    For sparse invalid IDs this is efficient; worst case still bounded.
    """
    total = 0
    max_digits = len(str(end))
    
    # For each total digit length n, try each pattern length k
    for n in range(2, max_digits + 1):
        for k in range(1, n // 2 + 1):
            if n % k != 0:
                continue
            r = n // k
            if r < 2:
                continue
            
            bounds = get_base_bounds_for_repetition(k, r, start, end)
            if bounds:
                base_min, base_max, M = bounds
                # Sum only primitive bases (can't use closed form, must filter)
                for base in range(base_min, base_max + 1):
                    if is_primitive_base(base):
                        total += base * M
    
    return total


def find_invalid_ids_part2_in_range(start: int, end: int) -> Set[int]:
    """Find all Part 2 invalid IDs within [start, end]. For testing."""
    invalid_ids = set()
    max_digits = len(str(end))
    
    for n in range(2, max_digits + 1):
        for k in range(1, n // 2 + 1):
            if n % k != 0:
                continue
            r = n // k
            if r < 2:
                continue
            
            bounds = get_base_bounds_for_repetition(k, r, start, end)
            if bounds:
                base_min, base_max, M = bounds
                for base in range(base_min, base_max + 1):
                    if is_primitive_base(base):
                        invalid_ids.add(base * M)
    
    return invalid_ids


# ============ Common ============

def parse_ranges(text: str) -> List[Tuple[int, int]]:
    """Parse 'start-end,start-end,...' into list of (start, end) tuples."""
    text = text.replace('\n', ' ').strip().rstrip(',')
    return [
        (int(a), int(b))
        for part in text.split(',')
        if part.strip()
        for a, b in [part.strip().split('-')]
    ]


def solve_part1(input_text: str) -> int:
    """Sum all Part 1 invalid IDs across all ranges."""
    return sum(sum_invalid_ids_in_range(a, b) for a, b in parse_ranges(input_text))


def solve_part2(input_text: str) -> int:
    """Sum all Part 2 invalid IDs across all ranges."""
    return sum(sum_invalid_ids_part2_in_range(a, b) for a, b in parse_ranges(input_text))


def test_example():
    """Verify against puzzle examples."""
    example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
                 1698522-1698528,446443-446449,38593856-38593862,565653-565659,
                 824824821-824824827,2121212118-2121212124"""
    
    # Part 1 tests
    assert find_invalid_ids_in_range(11, 22) == [11, 22]
    assert find_invalid_ids_in_range(95, 115) == [99]
    assert find_invalid_ids_in_range(998, 1012) == [1010]
    assert find_invalid_ids_in_range(1698522, 1698528) == []
    
    for a, b in [(11, 22), (95, 115), (998, 1012), (1188511880, 1188511890)]:
        assert sum(find_invalid_ids_in_range(a, b)) == sum_invalid_ids_in_range(a, b)
    
    result1 = solve_part1(example)
    assert result1 == 1227775554, f"Part 1: Expected 1227775554, got {result1}"
    
    # Part 2 tests
    assert is_repeated_pattern(111) == True
    assert is_repeated_pattern(999) == True
    assert is_repeated_pattern(565656) == True
    assert is_repeated_pattern(824824824) == True
    assert is_repeated_pattern(2121212121) == True
    assert is_repeated_pattern(123) == False
    
    assert find_invalid_ids_part2_in_range(11, 22) == {11, 22}
    assert find_invalid_ids_part2_in_range(95, 115) == {99, 111}
    assert find_invalid_ids_part2_in_range(998, 1012) == {999, 1010}
    
    result2 = solve_part2(example)
    assert result2 == 4174379265, f"Part 2: Expected 4174379265, got {result2}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python aoc-day-02.py <input_file> [--part 1|2]")
        print("Running example test instead...")
        test_example()
        print("Example tests passed!")
        return
    
    test_example()
    
    # Parse arguments
    input_file = sys.argv[1]
    part = None
    if "--part" in sys.argv:
        idx = sys.argv.index("--part")
        if idx + 1 < len(sys.argv):
            part = int(sys.argv[idx + 1])
    
    with open(input_file) as f:
        input_text = f.read()
    
    if part == 1 or part is None:
        print(solve_part1(input_text))
    if part == 2 or part is None:
        print(solve_part2(input_text))


if __name__ == "__main__":
    main()
