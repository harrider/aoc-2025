# Day 01 - Development Bridge Document

## Environment Details
- **OS:** Windows
- **Shell:** PowerShell 5.1
- **Python Version:** 3.8.5
- **Workspace Root:** `f:\CodeRepo\_AI\_AdventOfCode\aoc2025\`
- **Tasks Directory:** `f:\CodeRepo\_AI\_AdventOfCode\aoc2025\_aoc-tasks\`

## Python Compatibility Notes
- Python 3.8 does **NOT** support built-in generic types like `tuple[str, int]` or `list[str]`
- Must use `from typing import Tuple, List` for type hints
- Or use `from __future__ import annotations` at the top of the file

## Code Design Patterns (Use for ALL future problems)
1. **Command-line arguments for input files** - Use `sys.argv` to accept input file path
   - Never hardcode input file paths
   - Usage pattern: `python solution.py <input_file>`
2. **Include example test case** - Verify algorithm against puzzle examples first
3. **Modular functions** - Separate parsing, logic, and I/O
4. **Docstrings** - Document function purpose concisely (avoid restating obvious parameters)
5. **Preserve Part 1 when adding Part 2** - Each day has two parts; keep both working
   - Use separate functions for Part 1 and Part 2 logic
   - Output both answers when running the solution

## Code Quality Standards
1. **Eliminate redundancy** - Don't create helper functions for trivial one-liners (e.g., arithmetic series formula)
2. **Use list/generator comprehensions** - Prefer `sum(f(x) for x in items)` over manual loops
3. **Consolidate shared logic** - Extract common patterns into reusable helpers (e.g., `get_base_bounds`)
4. **Keep tests focused** - Test outputs, not intermediate representations; avoid redundant assertions
5. **Prefer concise idioms** - Use unpacking, ternary expressions, and Python's expressive syntax
6. **Type hints** - Use `from typing import List, Tuple, Optional` (Python 3.8 compatibility)
7. **Avoid duplicate work** - Parse input and precompute (e.g., merge ranges) once, pass results to functions
8. **Evaluate unification vs separation** - When Part 1 and Part 2 share structure, ask:
   - Do they share preprocessing that shouldn't be repeated? → Unify parsing
   - Do they have the same semantics with minor variations? → Unify logic
   - Do they have meaningfully different semantics (e.g., "count events" vs "count paths")? → Keep separate for clarity
   - Would unifying require conditionals that obscure intent? → Keep separate

## Performance Guidelines
1. **Never settle for "good enough"** - Always aim for the most efficient solution possible; O(n²) is unacceptable when O(n) or better exists
2. **Think mathematically first** - Before coding, ask: "Is there a closed-form solution?"
3. **Optimize both time AND space** - Prefer O(1) space over O(n) space when achievable
4. **Avoid O(n) iteration over large ranges** - AoC inputs often have billion+ element ranges
5. **Generate, don't enumerate** - If valid values are sparse, generate candidates directly
6. **Target optimal complexity** - Aim for O(log n), O(n), or O(output size); never assume input size is small
7. **Precompute patterns** - Use suffix/prefix arrays, cumulative sums, or other precomputation to avoid redundant work
8. **Single-pass when possible** - Many problems can be solved in one traversal with careful state tracking

## File Naming Conventions
| File Type | Pattern | Example |
|-----------|---------|---------|
| Solution code | `aoc-day-XX.py` | `aoc-day-01.py` |
| Puzzle input | `aoc-day-XX-part-01-input.txt` | `aoc-day-01-part-01-input.txt` |
| Part 1 tasking | `aoc-tasking-day-XX-part-1.md` | `aoc-tasking-day-01-part-1.md` |
| Part 2 tasking | `aoc-tasking-day-XX-part-2.md` | `aoc-tasking-day-01-part-2.md` |
| Bridge doc | `aoc-tasking-day-XX-bridge.md` | `aoc-tasking-day-01-bridge.md` |

## Lessons Learned
1. **Always verify examples first** - Run against puzzle examples before trying puzzle input
2. **Watch for edge cases in Part 2** - Part 2 often introduces wrapping, overflow, or counting nuances
3. **Read carefully** - The puzzle text contains critical details (e.g., "method 0x434C49434B" = count all clicks)
4. **Refactor after initial solution** - First make it work, then make it clean and fast
5. **Keep output minimal and ASCII-only** - Avoid Unicode symbols (e.g., ✓); just print the answer
6. **Use `--part N` flag** - Run only the specific part needed
   - Usage: `python aoc-day-XX.py <input_file> --part 1` or `--part 2`
7. **Filter terminal output** - When running solutions, pipe to `Select-String` to capture only the answer line
   - Example: `python aoc-day-XX.py input.txt --part 1 2>&1 | Select-String "Part"`
   - This avoids test output cluttering the response
8. **Minimize output when using `--part N`** - Only run example tests and print answers for the requested part
   - Don't run/print Part 1 example when `--part 2` is specified
   - This prevents terminal output truncation issues
9. **Make `input_file` optional** - Use `nargs='?'` so example tests can run without any input file
   - `python aoc-day-XX.py` runs examples only; `python aoc-day-XX.py input.txt` runs both
10. **No extra test files** - Embed examples directly in code; don't create `test-example.txt` artifacts
11. **Name functions by behavior, not usage** - Use `extract_numbers_by_column` not `extract_numbers_part2`
   - Names should describe *what* the function does, not *where* it's used

## Optimization Patterns
| Pattern | When to Use | Example |
|---------|------------|---------|
| Generate candidates | When valid values are sparse in a range | Day 2: Generate repeated patterns instead of checking all numbers |
| Closed-form arithmetic | When summing a sequence | Sum of `a` to `b` = `(b-a+1) * (a+b) / 2` |
| Mathematical constraints | When filtering by properties | `b * M` form lets us compute valid base range directly |
| Primitive base filtering | When same value can be generated multiple ways | Day 2 Part 2: Only count via the smallest repeating unit |
| Suffix maximum tracking | When optimizing a pair (i, j) where i < j | Day 3 Part 1: Track max digit after current position |
| Monotonic stack | When selecting k elements in order to maximize/minimize | Day 3 Part 2: Greedily remove (n-k) smallest digits |
| BFS with neighbor propagation | When removing elements enables new removals | Day 4 Part 2: Only check neighbors of removed cells |
| Set for merging states | When multiple paths lead to equivalent states | Day 7 Part 1: Beams at same column are indistinguishable |
| Dict/Counter for distinct paths | When paths remain distinct even at same position | Day 7 Part 2: Each timeline is unique regardless of column |

---

## Day 01 Summary: COMPLETE ⭐⭐

| Part | Answer | Description |
|------|--------|-------------|
| Part 1 | `1036` | Count final positions at 0 |
| Part 2 | `6228` | Count every click at 0 |

---

## Day 02 Summary: COMPLETE ⭐⭐

**Problem:** Find all "invalid IDs" (numbers that are a digit pattern repeated at least twice) within given ranges, and sum them.

**Key Insights:**
- Part 1: Invalid ID of length 2k equals `base * (10^k + 1)` → O(log₁₀ n) per range
- Part 2: Pattern repeated r times equals `base * ((10^(k*r) - 1) / (10^k - 1))`
- Use "primitive base" filtering to avoid double-counting (e.g., 111111 counted only via base=1, not base=11 or base=111)

| Part | Answer | Status |
|------|--------|--------|
| Part 1 | `52316131093` | VERIFIED ⭐ |
| Part 2 | `69564213293` | VERIFIED ⭐ |

---

## Day 03 Summary: COMPLETE ⭐⭐

**Problem:** Find maximum k-digit joltage from each battery bank (select k digits in order), sum all banks.

**Key Insight:**
- Selecting k digits to maximize = removing (n-k) digits optimally
- **Monotonic stack:** pop smaller digits when a larger one arrives (if removals remain)
- **O(n) time, O(k) space** — each digit pushed/popped at most once

**Algorithm Pattern Added:**
| Pattern | When to Use | Example |
|---------|------------|---------|
| Monotonic stack for "select k from n" | When picking k elements in order to maximize/minimize result | Day 3 Part 2: Remove n-k smallest digits greedily |

| Part | Answer | Status |
|------|--------|--------|
| Part 1 | `17166` | VERIFIED ⭐ |
| Part 2 | `169077317650774` | VERIFIED ⭐ |

---

## Day 04 Summary: COMPLETE ⭐⭐

**Problem:** Grid of paper rolls (`@`). A roll is "accessible" if it has fewer than 4 adjacent rolls (8-neighbor check).

**Part 1:** Count accessible rolls. Simple O(n) grid scan.

**Part 2:** Repeatedly remove accessible rolls until none remain. Count total removed.

**Key Insight:**
- Naive approach: O(n) per iteration × O(n) iterations = O(n²) — too slow
- **Optimized:** BFS with neighbor propagation — when a roll is removed, only its 8 neighbors could become newly accessible
- Track `in_queue` to avoid duplicate queue entries
- **O(n) time** — each cell queued/processed at most once

| Part | Answer | Status |
|------|--------|--------|
| Part 1 | `1457` | VERIFIED ⭐ |
| Part 2 | `8310` | VERIFIED ⭐ |

---

## Day 05 Summary: COMPLETE ⭐⭐

**Problem:** Determine which ingredient IDs are "fresh" based on overlapping ranges.

**Part 1:** Count how many available ingredient IDs fall within any fresh range.

**Part 2:** Count total unique fresh IDs across all ranges (ignore the ingredient list).

**Key Insight:**
- Merge overlapping ranges into non-overlapping intervals → O(n log n)
- Part 1: Binary search each query in merged ranges → O(log n) per query
- Part 2: Sum `(end - start + 1)` for each merged interval → O(n)

**Algorithm Pattern Added:**
| Pattern | When to Use | Example |
|---------|------------|---------|
| Merge intervals + binary search | When checking membership across overlapping ranges | Day 5 Part 1: Merge ranges, then binary search for each ID |
| Merge intervals + sum lengths | When counting total unique values in overlapping ranges | Day 5 Part 2: Sum merged interval sizes directly |

| Part | Answer | Status |
|------|--------|--------|
| Part 1 | `601` | VERIFIED ⭐ |
| Part 2 | `367899984917516` | VERIFIED ⭐ |

---

## Day 06 Summary: COMPLETE ⭐⭐

**Problem:** Parse a horizontal worksheet of vertical math problems. Each problem has numbers and an operator (`+` or `*`).

**Part 1:** Read numbers row-by-row (horizontally), solve each problem, sum all answers.

**Part 2:** Read numbers column-by-column (vertically, right-to-left), solve each problem, sum all answers.

**Key Insight:**
- Use strategy pattern: pass number extraction function to shared parsing logic
- `extract_numbers_by_row` vs `extract_numbers_by_column` — same interface, different behavior
- O(rows × cols) single-pass parsing

**Algorithm Pattern Added:**
| Pattern | When to Use | Example |
|---------|------------|---------|
| Strategy pattern for parsing | When same structure needs different extraction logic | Day 6: Row vs column number extraction |

| Part | Answer | Status |
|------|--------|--------|
| Part 1 | `5171061464548` | VERIFIED ⭐ |
| Part 2 | `10189959087258` | VERIFIED ⭐ |

---

## Day 07 Summary: COMPLETE ⭐⭐

**Problem:** Tachyon beam manifold simulation. A beam enters at `S`, moves downward. When it hits a splitter (`^`), it splits into two beams (left and right).

**Part 1:** Count total number of beam splits.

**Part 2:** Count total timelines (many-worlds interpretation — each split creates a new timeline).

**Key Insight:**
- Part 1: Track active columns with a **set** (beams merge when converging)
- Part 2: Track timeline counts with a **dict** (timelines stay distinct, counts accumulate)
- Both are **O(rows × cols)** time, **O(cols)** space

**Algorithm Pattern:**
| Pattern | When to Use | Example |
|---------|------------|---------|
| Set-based state tracking | When multiple paths merge into equivalent state | Day 7 Part 1: Beams merging |
| Counter-based state tracking | When paths remain distinct (count multiplicities) | Day 7 Part 2: Timeline counting |

| Part | Answer | Status |
|------|--------|--------|
| Part 1 | `1649` | VERIFIED ⭐ |
| Part 2 | `16937871060075` | VERIFIED ⭐ |
