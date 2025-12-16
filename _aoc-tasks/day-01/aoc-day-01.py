"""
Advent of Code 2025 - Day 1: Secret Entrance
Solve the safe dial puzzle by counting how many times the dial points at 0.

Usage: python aoc-day-01.py <input_file>
"""
import sys
from typing import List, Tuple


def parse_rotation(rotation: str) -> Tuple[str, int]:
    """Parse a rotation string like 'L68' into direction and distance."""
    direction = rotation[0]
    distance = int(rotation[1:])
    return direction, distance


def simulate_dial(rotations: List[str], start_position: int = 50) -> int:
    """
    Part 1: Simulate the dial rotations and count how many times it lands on 0.
    
    Args:
        rotations: List of rotation strings (e.g., ['L68', 'R48', ...])
        start_position: Initial position of the dial (default 50)
    
    Returns:
        Number of times the dial points at 0 after a rotation
    """
    position = start_position
    zero_count = 0
    
    for rotation in rotations:
        direction, distance = parse_rotation(rotation)
        
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100
        
        if position == 0:
            zero_count += 1
    
    return zero_count


def count_zeros_in_rotation(start: int, direction: str, distance: int) -> int:
    """
    Count how many times the dial passes through or lands on 0 during a single rotation.
    
    Args:
        start: Starting position (0-99)
        direction: 'L' for left, 'R' for right
        distance: Number of clicks to rotate
    
    Returns:
        Number of times the dial points at 0 during this rotation
    """
    if distance == 0:
        return 0
    
    # Calculate end position
    if direction == 'R':
        end = (start + distance) % 100
    else:
        end = (start - distance) % 100
    
    # Full revolutions (each full 100 clicks passes through 0 once)
    full_revolutions = distance // 100
    remaining = distance % 100
    
    # Count zeros from full revolutions
    zero_count = full_revolutions
    
    # Check if 0 is crossed in the partial revolution (remaining clicks)
    if remaining > 0:
        if direction == 'R':
            # Going right from start for 'remaining' clicks
            # We hit 0 if we wrap around: i.e., (100 - start) <= remaining
            # That means we need to go past position 99 to reach 0
            steps_to_zero = (100 - start) % 100
            if steps_to_zero == 0:
                steps_to_zero = 100  # If at 0, need full revolution to return
            if steps_to_zero <= remaining:
                zero_count += 1
        else:  # direction == 'L'
            # Going left from start for 'remaining' clicks
            # We hit 0 if start < remaining (we go below 0)
            # OR if start == 0, we leave and don't come back unless remaining >= 100
            steps_to_zero = start
            if steps_to_zero == 0:
                steps_to_zero = 100  # If at 0, need full revolution to return
            if steps_to_zero <= remaining:
                zero_count += 1
    
    return zero_count


def simulate_dial_part2(rotations: List[str], start_position: int = 50) -> int:
    """
    Part 2: Simulate the dial rotations and count every click where dial points at 0.
    
    This counts all times the dial passes through or lands on 0, not just final positions.
    
    Args:
        rotations: List of rotation strings (e.g., ['L68', 'R48', ...])
        start_position: Initial position of the dial (default 50)
    
    Returns:
        Total number of times the dial points at 0 during all rotations
    """
    position = start_position
    zero_count = 0
    
    for rotation in rotations:
        direction, distance = parse_rotation(rotation)
        
        # Count zeros during this rotation
        zero_count += count_zeros_in_rotation(position, direction, distance)
        
        # Update position
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100
    
    return zero_count


def read_input(filename: str) -> List[str]:
    """Read rotations from input file, one per line."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def main():
    # Example from the puzzle description
    example_rotations = [
        "L68", "L30", "R48", "L5", "R60",
        "L55", "L1", "L99", "R14", "L82"
    ]
    
    # Verify Part 1 with the example (expected: 3)
    example_result_p1 = simulate_dial(example_rotations)
    print(f"Part 1 - Example result: {example_result_p1} (expected: 3)")
    
    # Verify Part 2 with the example (expected: 6)
    example_result_p2 = simulate_dial_part2(example_rotations)
    print(f"Part 2 - Example result: {example_result_p2} (expected: 6)")
    
    # Solve with actual puzzle input from command line argument
    if len(sys.argv) < 2:
        print("Usage: python aoc-day-01.py <input_file>")
        return
    
    input_file = sys.argv[1]
    try:
        puzzle_rotations = read_input(input_file)
        puzzle_result_p1 = simulate_dial(puzzle_rotations)
        puzzle_result_p2 = simulate_dial_part2(puzzle_rotations)
        print(f"Part 1 - Puzzle answer: {puzzle_result_p1}")
        print(f"Part 2 - Puzzle answer: {puzzle_result_p2}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")


if __name__ == "__main__":
    main()
