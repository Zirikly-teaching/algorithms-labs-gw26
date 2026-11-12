---
layout: default
title: Lab 7
nav_order: 8
---

# CSCI 3212 Lab 7: String Searching

String searching finds the starting positions of a pattern inside a longer text.
It supports tasks such as searching a document, finding a DNA sequence, and
recognizing a signature in network traffic.

This lab develops each algorithm through an explanation, a worked example,
pseudocode, and practice traces. The current sections cover:

1. **Part 1: Naive String Search:** Test every possible starting position and
   count the character comparisons.
2. **Part 2: Rabin–Karp:** Use hashing to filter candidate matches, update a
   window's hash efficiently, and verify matching hashes.
3. **Part 3: Knuth–Morris–Pratt (KMP):** Build a prefix table and reuse matched
   characters when a comparison fails.

## Files and deliverables

| File               | Your work                                    |
| ------------------ | -------------------------------------------- |
| `README.md`        | Complete the traces and complexity questions |
| `string_search.py` | Fill in the four implementation TODOs        |
| `lab_checks.py`    | Provided automated checks; do not edit       |

- [ ] Part 1: Trace and implement naive search.
- [ ] Part 2: Trace, implement, and analyze Rabin–Karp.
- [ ] Part 3: Trace the prefix table and matcher, implement KMP, and analyze its
      running time.

### Shared conventions

Use zero-based indexing: text `T` has length $n$, pattern `P` has length $m$,
with candidate starting positions $s=0,\ldots,n-m$. There are $n-m+1$ windows.
Compare `T[s + j]` with `P[j]`.

All three search functions return **all matching indices in increasing order**,
including overlaps: searching for `"aa"` in `"aaaa"` returns `[0, 1, 2]`. Assume
a nonempty pattern; return `[]` when the pattern is longer than the text. Use
character comparisons to implement matching. Do not use `find`, `index`, regular
expressions, or substring membership tests.

---

## Part 1: Naive String Search

### Background: Align, compare, shift

A **shift** $s$ is the position in the text where we start checking the pattern.
Compare `P[j]` with `T[s + j]`, starting at `j = 0`. Stop when the characters
differ. If all $m$ characters match, add $s$ to the results. Then move one
position to the right and start again at `j = 0`.

For the lecture's `T = "abacaabadcab"` and `P = "aba"`, shift `0` compares text
indices `0, 1, 2` and records a match. At shift `1`, the first comparison is
`T[1] = b` against `P[0] = a`, so this attempt stops immediately.

### Pseudocode

```text
NAIVE-SEARCH(T, P)
  n = length(T)
  m = length(P)
  matches = []
  for s = 0 to n - m inclusive
    j = 0
    while j < m and T[s + j] == P[j]
      j = j + 1
    if j == m
      append s to matches
  return matches
```

### 1.1 Trace: Where does each attempt stop?

**TODO 1.1:** For the same text and pattern, trace the shifts below. List the
text indices checked, in order, including the one where a mismatch occurs.
Record where $j$ stops and whether you add $s$ to the results.

| Shift `s` | Text indices checked | Final `j` | Append `s`? |
| --------- | -------------------- | --------- | ----------- |
| 1         | `1`                  | 0         | No          |
| 2         | `2`                  | 1         | No          |
| 4         | `2`                  | 1         | No          |
| 5         | `3`                  | 2         | Yes         |

### 1.2 Implementation

**TODO 1.2:** Complete `naive_search` in the provided `string_search.py` using
the pseudocode. Return the list of all matching shifts, including overlaps.

---

## Part 2: Rabin–Karp

### Background: Compare fingerprints, then verify

Rabin–Karp computes a small number, called a **hash** or **fingerprint**, for
the pattern and each text window. Let $p$ be the pattern hash and $t$ the window
hash. If they differ, skip that window. If they match, check the characters
before recording a match. Two different strings can have the same hash; this is
called a **spurious hit**.

To compute the hash, give each character a numeric code. Start with zero,
multiply by the base $d$, and add the next code. Take the remainder modulo a
prime $q$ after each step:

```text
hash = (d * hash + code(character)) mod q
```

In the lecture's decimal example, `"31415"` with $d=10$, $q=13$, and digit codes
gives the hashes `3, 5, 2, 8, 7` as we read the digits. The final hash is `7`.
Taking the remainder keeps these numbers small.

### Updating the hash

When the window moves one position, only the first and last characters change.
Compute $h=d^{m-1} \bmod q$ once; it gives the first character its place value
in the hash. To move from shift $s$ to $s+1$:

1. Subtract `code(T[s]) * h` to remove the outgoing character.
2. Multiply by $d$ to shift the remaining characters left.
3. Add `code(T[s + m])`, then take the remainder modulo $q$.

For example, the exact-number update from `31415` to `14152` is
`(31415 - 3 * 10000) * 10 + 2`. The same operations work on fingerprints using
$h=10^4 \bmod 13=3$.

### Pseudocode

This is the lecture's matcher with zero-based string indices and a returned list
of shifts. `MATCHES` compares the $m$ characters from left to right and stops at
the first mismatch.

```text
RABIN-KARP-SEARCH(T, P, d, q)
  n = length(T)
  m = length(P)
  matches = []
  if m > n
    return matches
  h = d^(m - 1) mod q
  p = 0
  t = 0
  for j = 0 to m - 1 inclusive
    p = (d * p + code(P[j])) mod q
    t = (d * t + code(T[j])) mod q
  for s = 0 to n - m inclusive
    if p == t
      if MATCHES(T, P, s)
        append s to matches
    if s < n - m
      t = (d * (t - code(T[s]) * h) + code(T[s + m])) mod q
  return matches
```

### 2.1 Trace: Roll and verify

Use the lecture's `T = "2359023141526739921"` and `P = "31415"`. **Both are
strings.** To calculate the hashes by hand, use each digit's value: the
character `'3'` contributes the number `3`. To check a match, compare the
characters in the text and pattern.

Use $d=10$ and $q=13$. Here $m=5$, $p=7$, and $h=3$. At shift `6`, the hash is
`7`; all five characters match, so record `6`.

**TODO 2.1:** Trace these two steps:

1. **Move from shift `6` to `7`.** Which digit leaves the window, and which
   digit enters? Substitute them into the rolling-hash formula and calculate the
   new hash.

3 leaves and 2 enters.

`hash = ((31415 - 3 * 10000) * 10 + 2) mod 13 = 8`

2. **Check shift `12`.** Its hash is `7`, so compare the characters. List the
   text and pattern indices checked before stopping. Is this a match or a
   spurious hit?

Checked text index 12 and pattern index 0. It is a spurious hit.

### 2.2 Implementation

**TODO 2.2:** Complete `rabin_karp` in the provided `string_search.py` using the
pseudocode. Write the character-by-character check inside the function. The
length check and initial variables are provided.

Use **ASCII strings**, `ord(character)` for codes, and the provided defaults
`d=256`, `q=101`. The hand trace uses decimal digit codes to keep arithmetic
manageable. Python's `% q` gives a nonnegative remainder for positive `q`;
`pow(d, m - 1, q)` computes $h$.

### 2.3 Best- and worst-case time complexity

**TODO 2.3:** Find the best- and worst-case running times, including the time
spent building the first hashes. Assume $1 \le m \le n$ and that each hash
operation takes constant time.

- **Best case:** Every window hash differs from the pattern hash.
- **Worst case:** The text is $n$ copies of `a`, and the pattern is $m$ copies
  of `a`.

Give tight bounds in terms of $n$ and $m$. The search column includes both hash
comparisons and character checks.

| Case  | Build hashes | Search                    | Total                         |
| ----- | ------------ | ------------------------- | ----------------------------- |
| Best  | $\Theta(m)$  | $\Theta(n - m)$           | $\Theta(n)$                   |
| Worst | $\Theta(m)$  | $\Theta(m * (n - m + 1))$ | $\Theta(m * (n - m + 1) + m)$ |

For each case, explain in one sentence how many windows need character checks
and how many characters are checked in each one.

In the best case, there will be no hits. No windows will need character checks.
The full length of both strings will be searched. In the worst case, every
character will produce a matching hash. Every character will need to be checked.
Every pass will check the full pattern.

### Connection: Searching for several patterns

You can also search for several patterns of the same length. Hash each pattern,
then move through the text once. When a window's hash matches one of the stored
hashes, compare it with the patterns that have that hash. Choosing a larger
prime for $q$ makes accidental hash matches less likely.

---

## Part 3: Knuth–Morris–Pratt (KMP)

### Background: Keep the useful part of a partial match

Suppose `P = "ababaca"` and five characters, `"ababa"`, have matched. The next
text character is `b`, but the pattern expects `c`. The matched substring starts
and ends with `"aba"`. We can keep those three matches and compare the same text
`b` with the next pattern character, `P[3] = b`. The text index stays in place
during this fallback.

Before searching, KMP builds a **prefix table**, $\pi$ (`pi` in code). This
table tells us how many matched characters we can keep after a mismatch.

### The prefix table

`pi[j]` is the length of the longest **proper prefix** of `P[0:j + 1]` that is
also a suffix. A prefix starts at the beginning; a suffix ends at the end.
“Proper” means shorter than the whole substring. A string that is both a prefix
and a suffix is called a **border**.

For `"ababa"`, the longest border is `"aba"`, so `pi[4] = 3`. The prefix and
suffix may overlap. For a single character, only the empty prefix qualifies, so
`pi[0] = 0`.

The lecture uses one-based indices. Here, `pi[j]` describes the substring
**ending at zero-based index `j`**. If `k` characters have matched, fall back to
`pi[k - 1]`. This gives the length of the next shorter border to try. If the
next character still differs, follow another prefix-table entry.

### Pseudocode: Build the prefix table

```text
COMPUTE-PREFIX-FUNCTION(P)
  m = length(P)
  pi = array of m zeros
  k = 0
  for j = 1 to m - 1 inclusive
    while k > 0 and P[k] != P[j]
      k = pi[k - 1]
    if P[k] == P[j]
      k = k + 1
    pi[j] = k
  return pi
```

### Pseudocode: Search the text

Here `q` counts the characters currently matched. It is separate from the prime
modulus named `q` in Rabin–Karp. After recording a complete match,
`q = pi[m - 1]` keeps the matching suffix so the next match can overlap it.

```text
KMP-SEARCH(T, P)
  n = length(T)
  m = length(P)
  matches = []
  if m > n
    return matches
  pi = COMPUTE-PREFIX-FUNCTION(P)
  q = 0
  for i = 0 to n - 1 inclusive
    while q > 0 and P[q] != T[i]
      q = pi[q - 1]
    if P[q] == T[i]
      q = q + 1
    if q == m
      append i - m + 1 to matches
      q = pi[m - 1]
  return matches
```

### 3.1 Trace: Fallbacks and a complete match

Use the lecture's `P = "ababaca"` and `T = "abababacaba"`. The first five prefix
entries are `[0, 0, 1, 2, 3]`.

**TODO 3.1:** Finish the prefix-table steps below. If `k` falls back, show its
starting value and each value it reaches. Write “none” if no fallback occurs.
The first row is worked: `P[2] == P[4]`, so `k` increases to `3`.

| Index `j` | Starting `k` | Fallbacks | `pi[j]` |
| --------- | ------------ | --------- | ------- |
| 4         | 2            | none      | 3       |
| 5         | 3            | none      | 0       |
| 6         | 0            | 0         | 0       |

Now trace the matcher at `i = 8`, starting with `q = 6`. Which pattern index is
compared with `T[8]`? What shift is recorded, and what is `q` afterward?

`P[6]` is compared. A shift is recorded at `2`. q becomes `7`

### 3.2 Implementation

In the provided `string_search.py`:

- **TODO 3.2A:** Complete `compute_prefix_function(pattern)` and return `pi`.
- **TODO 3.2B:** Complete `kmp_search(text, pattern)` using that helper.

Follow the pseudocode's fallback rules both on a mismatch and after a full
match. The provided checks cover repeated fallbacks and overlapping matches.

### 3.3 Best- and worst-case time complexity

**TODO 3.3:** Find the best- and worst-case running times, including the time to
build `pi`. Assume $1 \le m \le n$ and that the search returns all matches.

- **Best case:** The text contains only `a`, and the pattern contains only `b`.
- **Worst case:** Long partial matches keep ending in mismatches. For example,
  search for `"aaab"` in a text of twenty `a` characters.

Give tight bounds in terms of $n$ and $m$.

| Case  | Build `pi`  | Search      | Total           |
| ----- | ----------- | ----------- | --------------- |
| Best  | $\Theta(m)$ | $\Theta(n)$ | $\Theta(n + m)$ |
| Worst | $\Theta(m)$ | $\Theta(n)$ | $\Theta(n + m)$ |

Explain the worst-case bound in a few lines. Across the whole scan, how often
can `q` increase? How does that limit the number of fallbacks? Use the same
reasoning for `k` when building `pi`.

In the worst case, the scan will occur twice per character in `T`. `q` can only
increase by `n / m` times, limiting the number of fallbacks so that no character
gets scanned more than twice. The same occurs for `k` when building `pi`.

---

## Final check

Run the provided practice file from within the `lab7/` directory:

```bash
python3 string_search.py
```

- Unfinished implementations report `[TODO]`.
- Incorrect results or errors report `[FAIL]`.
- Successful checks report `[PASS]`.

When all checks pass, the command returns exit code `0`.
