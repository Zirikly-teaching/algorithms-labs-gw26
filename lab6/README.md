---
layout: default
title: Lab 6
nav_order: 7
---

# CSCI 3212 Lab 6: Hashing, Separate Chaining, and Linear Probing

In lecture, we introduced **hashing**, a technique for looking up, inserting, and
deleting records in $O(1)$ average time. Instead of scanning an unsorted list in
$O(N)$ time or traversing a binary search tree in $O(\log N)$ time, a hash table
uses a mathematical **hash function** $h(k)$ to turn a key $k$ directly into an
array slot index.

This lab walks through each core idea step
by step with worked examples from lecture before asking you to trace or write
any code. You will focus on the three most important building blocks from class:
1. **Part 1: Hash Functions**: Computing array indices with the **Division Method** and **Multiplication Method**, and seeing why table size $m$ matters.
2. **Part 2: Separate Chaining**: Resolving collisions by storing a list (bucket chain) at each array slot, and tracking the **load factor** $\alpha = N / M$.
3. **Part 3: Open Addressing with Linear Probing**: Resolving collisions directly inside a single array by stepping forward one slot at a time.

## Files and deliverables

| File | Your work |
|---|---|
| `README.md` | Complete the 3 short trace tables and 3 short-answer questions |
| `hash_functions_practice.py` | Implement `division_hash` and `multiplication_hash` (2 short functions) |
| `chaining_practice.py` | Implement `chaining_insert` and `chaining_lookup`; `load_factor`, `chaining_delete`, and `chaining_rehash` are provided |
| `probing_practice.py` | Implement `linear_probe_insert` and `linear_probe_lookup`; `probe_index` is provided |
| `lab_checks.py` | Provided automated checks and load-factor demonstration; do not edit |

- [ ] Part 1: Division vs. Multiplication hash trace, 2 short functions, and 1 question.
- [ ] Part 2: Separate Chaining trace, 2 functions (`chaining_insert`, `chaining_lookup`), and 1 question.
- [ ] Part 3: Linear Probing trace, 2 functions (`linear_probe_insert`, `linear_probe_lookup`), and 1 question.
- [ ] Run all three practice files and confirm all checks pass.

Keep function names and parameters unchanged, and do not use Python's built-in
`dict` or `set` inside your hash table implementations.

---

## Part 1: Hash Functions and Choosing Table Size $m$

### Background: Why do we need a hash function?

Suppose we want to store student records indexed by a 9-digit Student ID.
- If we used **Direct Addressing** (putting ID `k` directly at `Array[k]`), we
  would need an array of **1,000,000,000 slots** even if our class only has 100
  students!
- **Hashing** solves this by compressing a huge universe of keys into a small,
  realistic array of $m$ slots (indices `0` to `m - 1`) using a hash function
  $h(k)$.

Think of a hash function like a magic index in a textbook: instead of flipping
through pages one by one, $h(k)$ immediately tells you which slot index to jump
to in $O(1)$ time. A good hash function must be:
1. **Deterministic:** Calling $h(k)$ on the same key $k$ *always* gives the
   exact same slot index.
2. **Uniform:** It spreads keys evenly across all $m$ slots to minimize
   collisions.
3. **Fast:** It runs in $O(1)$ constant time.

### The two hash functions from lecture

#### 1. The Division Method
$$h(k) = k \bmod m$$
We divide key $k$ by the table size $m$ and take the remainder (`key % m` in
Python). Since remainders when dividing by $m$ are always between `0` and
`m - 1`, the result is guaranteed to be a valid slot index.

- **How to choose table size $m$:** Choose $m$ to be a **prime number roughly halfway between two powers of 2**.

- **Why avoid powers of 2 ($m = 2^p$)?**
  - **The Base-10 Analogy:** In base-10, taking $123,456 \bmod 1000$ keeps only the last 3 digits (`456`) and throws away the upper digits (`123`).
  - **The Binary Trap (Why binary matters):** Computers physically store all numbers, memory addresses, and data in **binary** (base-2 as `0`s and `1`s). When $m = 2^p$, taking $k \bmod 2^p$ does not perform any true arithmetic mixing—it operates as a raw bitmask (`k & (m - 1)`) that extracts **only the last $p$ binary bits** of $k$ and completely ignores all higher bits. This makes **only the last few bits relevant** to the slot choice!
  - **Why this causes severe collisions:** Because only those last few bits dictate where a key lands, any binary pattern in your input data will cause keys to pile into the same slots:
    - *Memory addresses / Pointers:* Typically aligned to 4 or 8 bytes, so their lowest bits are always `00` or `000`. With $m = 8$, *every single pointer* hashes to slot `0`!
    - *Shared endings:* In our trace below, keys `19`, `51`, `83`, and `115` have very different upper bits, but all end in `011` in binary. With $m = 8 = 2^3$, only those last 3 bits matter, so all four keys collide into slot `3` (`19 % 8 == 51 % 8 == 83 % 8 == 115 % 8 == 3`), leaving most of the table empty.
- **Why choose a prime $m$?** A prime has no divisors matching binary bit boundaries or regular step patterns in data. Dividing by a prime forces the remainder to depend on **all** bits of $k$ rather than just the lowest bits.
- **Concrete examples: What to avoid vs. what to choose:**
  | Target Table Size | Powers of 2 (Avoid) | Primes Too Close (Avoid) | Good Primes to Choose (In the Middle) |
  |---|---|---|---|
  | **~20 slots** | $16$ ($2^4$) and $32$ ($2^5$) | $17$ ($16+1$), $31$ ($32-1$) | **$23$** |
  | **~50 slots** | $32$ ($2^5$) and $64$ ($2^6$) | $31$, $61$, $67$ | **$47$** or **$53$** |
  | **~100 slots** | $64$ ($2^6$) and $128$ ($2^7$) | $127$ ($128-1$) | **$97$** or **$101$** |
  | **~700 slots** | $512$ ($2^9$) and $1024$ ($2^{10}$) | $509$, $1021$ | **$701$** |

#### 2. The Multiplication Method
$$h(k) = \lfloor m \cdot ((k \cdot A) \bmod 1) \rfloor$$
If we want the hardware speed of a power-of-2 table size ($m = 2^p$) without the
bit-pattern trap of the Division Method, we use the Multiplication Method:
1. Multiply key `k` by a constant `A` between `0` and `1`, commonly `A = (√5 − 1) / 2 ≈ 0.6180339887`, which helps spread keys across buckets. Simple fractions like `0.5` or `0.75` make the fractional parts repeat every 2 or 4 integer keys, concentrating keys in just a few buckets and causing frequent collisions.
2. Keep **only the fractional part** after the decimal point: $(k \cdot A) \bmod 1$
   (in Python, `(key * A) % 1.0`). For example, the fractional part of `11.7426`
   is `0.7426`.
3. Multiply that fraction by $m$ and round down (`math.floor`) to get an integer
   slot in `0` to `m - 1`.

| Method | Formula | Python Expression | Best Table Size $m$ |
|---|---|---|---|
| **Division Method** | $h(k) = k \bmod m$ | `key % m` | Prime number (not near $2^p$) |
| **Multiplication Method** | $\lfloor m \cdot ((k \cdot A) \bmod 1) \rfloor$ | `math.floor(m * ((key * A) % 1.0))` | Any $m$ (often $m = 2^p$) |

### 1.1 Trace: The Power-of-2 Trap vs. Prime $m$

In lecture, we saw four keys `[19, 51, 83, 115]` whose binary representations
all end in the exact same 3 bits (`011`).

**TODO 1.1:** Complete the table below comparing what happens when we hash these
four keys using the Division Method with $m = 8$ ($2^3$), the Division Method
with prime $m = 7$, and the Multiplication Method with $m = 8$. The first row is
worked for you.

| Key $k$ | Binary (8-bit) | Last 3 Bits | Division $k \bmod 8$ ($m = 8$) | Prime Division $k \bmod 7$ ($m = 7$) | Multiplication $\lfloor 8 \cdot ((k \cdot A) \bmod 1) \rfloor$ ($m = 8$) |
|---|---|---|---|---|---|
| 19 | `00010 011` | `011` | `19 % 8 = 3` | `19 % 7 = 5` | `floor(8 * 0.7426) = 5` |
| 51 | `00110 011` | `011` | TODO | TODO | `floor(8 * 0.5197) = 4` |
| 83 | `01010 011` | `011` | TODO | TODO | `floor(8 * 0.2968) = 2` |
| 115 | `01110 011` | `011` | TODO | TODO | `floor(8 * 0.0739) = 0` |

### 1.2 Implementation

Open `hash_functions_practice.py` and implement the two functions (each is just
1–2 lines of code):
- **TODO 1.2A:** `division_hash(key, m)`
- **TODO 1.2B:** `multiplication_hash(key, m, A)`

Test your implementation by running:

```bash
python3 hash_functions_practice.py
```

### 1.3 Short answer

**TODO 1.3:** Look at your `k mod 8` column vs. your `k mod 7` column in
Table 1.1. Why did all four keys collide into slot `3` when $m = 8$, and why did
choosing a prime table size ($m = 7$) spread them into different slots?

---

## Part 2: Collision Resolution Strategy 1: Separate Chaining

### Background: Collisions and Separate Chaining

Even with a great hash function, **collisions** (two different keys hashing to
the same slot) are unavoidable: by the **Pigeonhole Principle**, if you place 10
items into 7 slots, at least one slot *must* hold more than one item.

**Separate Chaining** handles collisions in the simplest possible way: instead
of storing a single item at each array index, **each table slot holds a list
(called a bucket or chain)** of `[key, value]` pairs that hashed to that index.

For example, in a table with $M = 7$ buckets (`0` to `6`), if keys `12` and `19`
both hash to slot `5` ($12 \bmod 7 = 5$ and $19 \bmod 7 = 5$), bucket `5` simply
stores both pairs in a list:
```text
Bucket 3: [ [24, "C"] ]
Bucket 4: [ ]
Bucket 5: [ [12, "A"], [19, "B"] ]   <-- collision resolved by appending to bucket 5's list!
Bucket 6: [ ]
```

### How Separate Chaining operations work

Let $M$ be `table.capacity` (number of buckets) and $N$ be `table.size` (total
number of stored key-value pairs):
1. **Insert (`chaining_insert(table, key, value)`):**
   - Compute `index = key % table.capacity` to find the right bucket list:
     `bucket = table.buckets[index]`.
   - First, loop through `bucket` to check if `key` is already stored there. If
     you find an entry `[k, v]` where `k == key`, update its value (`entry[1] = value`)
     and return (do **not** increase `table.size`!).
   - If `key` is not in `bucket`, append `[key, value]` to `bucket` and add `1`
     to `table.size`.
   - Finally, check the **load factor** ($\alpha = N / M$). If
     `load_factor(table) > table.max_load` (`0.75`), call the provided
     `chaining_rehash(table, 2 * table.capacity)` helper to double the table size!
2. **Lookup (`chaining_lookup(table, key)`):**
   - Compute `index = key % table.capacity`.
   - Loop through the `[k, v]` pairs in `table.buckets[index]`. If `k == key`,
     return `v`.
   - If you finish checking the bucket without finding `key`, return `None`.

### Load Factor ($\alpha$) and Dynamic Resizing

The **load factor** measures how full or crowded the hash table is:
$$\alpha = \frac{N}{M} = \frac{\text{number of stored elements}}{\text{number of table slots}}$$

Under the **Simple Uniform Hashing Assumption (SUHA)** (each key is equally
likely to land in any bucket), the average length of each bucket chain is $\alpha$,
so searching or inserting takes **$O(1 + \alpha)$** expected time. To prevent
chains from growing too long, whenever $\alpha > 0.75$, the table **doubles its
capacity to $2M$ and rehashes all keys** into the new buckets, resetting $\alpha$
down to $\approx 0.375$.

### Pseudocode

```text
CHAINING-INSERT(T, key, value)
  index = key mod T.capacity
  for each entry in T.buckets[index]
    if entry[0] == key
      entry[1] = value       // update existing key in place
      return
  append [key, value] to T.buckets[index]
  T.size = T.size + 1
  if load_factor(T) > T.max_load
    chaining_rehash(T, 2 * T.capacity)

CHAINING-LOOKUP(T, key)
  index = key mod T.capacity
  for each [entry_key, entry_val] in T.buckets[index]
    if entry_key == key
      return entry_val
  return None
```

### 2.1 Trace: Separate Chaining Insertions

Trace inserting `(12, "A")`, `(19, "B")`, `(24, "C")`, `(26, "D")`, and
`(31, "E")` into an empty Separate Chaining table with $M = 7$ buckets (`0` to `6`)
and $h(k) = k \bmod 7$.

**TODO 2.1:** Fill in the remaining three rows of the table. The first two rows
are worked for you.

| Step | Insert `(key, val)` | Bucket Index ($k \bmod 7$) | Contents of `table.buckets[index]` after insert | Total items $N$ | Load Factor $\alpha = N / 7$ |
|---|---|---|---|---|---|
| 1 | `(12, "A")` | `12 % 7 = 5` | `[[12, "A"]]` | 1 | `1/7 ≈ 0.14` |
| 2 | `(19, "B")` | `19 % 7 = 5` | `[[12, "A"], [19, "B"]]` | 2 | `2/7 ≈ 0.29` |
| 3 | `(24, "C")` | TODO | TODO | TODO | TODO |
| 4 | `(26, "D")` | TODO | TODO | TODO | TODO |
| 5 | `(31, "E")` | TODO | TODO | TODO | TODO |

### 2.2 Implementation

Open `chaining_practice.py`. Notice that `load_factor`, `chaining_rehash`, and
`chaining_delete` are already provided for you! Implement the two core functions:
- **TODO 2.2A:** `chaining_insert(table, key, value)`
- **TODO 2.2B:** `chaining_lookup(table, key)`

Test your implementation by running:

```bash
python3 chaining_practice.py
```

### 2.3 Short answer

**TODO 2.3:** Look at the provided `chaining_rehash` function in
`chaining_practice.py`. When the table doubles in capacity from $M = 4$ to
$2M = 8$, why do we have to recompute `key % new_capacity` for every key
(for example, key `14` moves from bucket `14 % 4 = 2` to bucket `14 % 8 = 6`)
instead of just copying bucket `2` from the old table into bucket `2` of the new
table?

---

## Part 3: Collision Resolution Strategy 2: Open Addressing (Linear Probing)

### Background: How Linear Probing works

Unlike Separate Chaining, **Open Addressing** does not use linked lists or bucket
chains. Every `[key, value]` pair lives **directly inside the table array**
`table.slots` of size $M$ (where empty slots hold `None`).

What happens if we want to insert key $k$, but slot $h(k) = k \bmod M$ is
already occupied? With **Linear Probing**, we simply check the next slot to the
right ($+1$, $+2$, $+3$, wrapping around to index `0` if we pass the end of the
array) until we find an empty slot:
$$\text{slot}_i = ((k \bmod M) + i) \bmod M \quad \text{for } i = 0, 1, 2, \dots, M - 1$$

### Walkthrough from lecture ($M = 7$, $h(k) = k \bmod 7$)

Start with 7 empty slots `[ _, _, _, _, _, _, _ ]` (indices `0` through `6`):
1. **Insert `12`:** $12 \bmod 7 = 5$. Slot `5` is empty (`1` probe). Place `12`
   at index `5`:
   `[ _, _, _, _, _, 12, _ ]`
2. **Insert `19`:** $19 \bmod 7 = 5$. Slot `5` is occupied by `12` (collision!).
   Probe $i = 1$: $(5 + 1) \bmod 7 = 6$. Slot `6` is empty (`2` probes total).
   Place `19` at index `6`:
   `[ _, _, _, _, _, 12, 19 ]`
3. **Insert `26`:** $26 \bmod 7 = 5$.
   - Probe $i = 0 \to$ slot `5` (occupied by `12`, collision!)
   - Probe $i = 1 \to$ slot `6` (occupied by `19`, collision!)
   - Probe $i = 2 \to (5 + 2) \bmod 7 = 0$ (**wraps around** to slot `0`, which
     is empty! `3` probes total). Place `26` at index `0`:
   `[ 26, _, _, _, _, 12, 19 ]`

### How Linear Probing Lookup works (and when to stop!)

To search for a key $k$ (`linear_probe_lookup`), we must follow the **exact same
probe path** $(h(k) + i) \bmod M$ for $i = 0, 1, \dots, M - 1$:
- If `table.slots[slot]` contains our target `key`, we found it! Return
  `(value, probes)` where `probes = i + 1`.
- If `table.slots[slot]` is **`None` (empty)**, we can **stop immediately** and
  return `(None, probes)`! Why? Because if `key` had ever been inserted, it
  would have been placed in this empty slot (or earlier).
- Notice how contiguous occupied slots form a block (like slots `5, 6, 0` above).
  In lecture, this is called **Primary Clustering**: as clusters grow and merge,
  new collisions have to walk across the entire cluster to find an empty slot,
  and expected probes grow as $\approx \frac{1}{1 - \alpha}$ when $\alpha$ nears `1.0`.

| Load Factor ($\alpha = N / M$) | Table Fullness | Expected Probes ($\approx \frac{1}{1 - \alpha}$) | Performance Impact |
|---|---|---|---|
| `0.50` | 50% full | `1 / (1 - 0.50) = 2` probes | Fast $O(1)$ lookup |
| `0.75` | 75% full | `1 / (1 - 0.75) = 4` probes | Standard resize threshold |
| `0.90` | 90% full | `1 / (1 - 0.90) = 10` probes | Clusters merge; noticeable slowdown |
| `0.99` | 99% full | `1 / (1 - 0.99) = 100` probes | Severe probe explosion |

### Pseudocode

```text
PROBE-INDEX(key, i, m)
  return ((key mod m) + i) mod m

LINEAR-PROBE-INSERT(T, key, value)
  for i from 0 to T.capacity - 1
    slot = PROBE-INDEX(key, i, T.capacity)
    probes = i + 1
    if T.slots[slot] is None
      T.slots[slot] = [key, value]
      T.size = T.size + 1
      return (slot, probes)
    else if T.slots[slot][0] == key
      T.slots[slot][1] = value     // update existing key in place
      return (slot, probes)
  raise OverflowError("Hash table is full")

LINEAR-PROBE-LOOKUP(T, key)
  for i from 0 to T.capacity - 1
    slot = PROBE-INDEX(key, i, T.capacity)
    probes = i + 1
    if T.slots[slot] is None
      return (None, probes)        // hit empty slot: key is not in table!
    else if T.slots[slot][0] == key
      return (T.slots[slot][1], probes)
  return (None, T.capacity)
```

### 3.1 Trace: Linear Probing Insertions and Lookups

Starting with the 7-slot table from the lecture walkthrough where `12` and `19`
have already been inserted, complete the trace for inserting `26`, `3`, and `10`,
and then trace two lookups on the final table.

**TODO 3.1:** Complete the remaining rows of the table below (`M = 7`,
$h(k) = k \bmod 7$). The first two insertions and first lookup are worked.

| Operation | Initial Hash ($k \bmod 7$) | Slots Inspected in Order | Number of Probes | Result / Slot Placed | Table State `[s0, s1, s2, s3, s4, s5, s6]` |
|---|---|---|---|---|---|
| Insert `12` | `12 % 7 = 5` | `5` | 1 | Placed at slot `5` | `[_, _, _, _, _, 12, _]` |
| Insert `19` | `19 % 7 = 5` | `5 -> 6` | 2 | Placed at slot `6` | `[_, _, _, _, _, 12, 19]` |
| Insert `26` | `26 % 7 = 5` | TODO | TODO | Placed at slot `0` | `[26, _, _, _, _, 12, 19]` |
| Insert `3` | `3 % 7 = 3` | TODO | TODO | Placed at slot `3` | `[26, _, _, 3, _, 12, 19]` |
| Insert `10` | `10 % 7 = 3` | TODO | TODO | Placed at slot `4` | `[26, _, _, 3, 10, 12, 19]` |
| Lookup `26` | `26 % 7 = 5` | `5 -> 6 -> 0` | 3 | Found `26` at slot `0` | *(unchanged)* |
| Lookup `33` | `33 % 7 = 5` | TODO | TODO | Not found (hit empty slot `1`) | *(unchanged)* |

### 3.2 Implementation

Open `probing_practice.py`. The `probe_index(key, i, m)` helper is already
provided for you. Implement the two core functions:
- **TODO 3.2A:** `linear_probe_insert(table, key, value)`
- **TODO 3.2B:** `linear_probe_lookup(table, key)`

Test your implementation by running:

```bash
python3 probing_practice.py
```

### 3.3 Short answer

**TODO 3.3:** When searching for missing key `33` ($33 \bmod 7 = 5$) in
Table 3.1, why can `linear_probe_lookup` stop as soon as it hits empty slot `1`
without checking slots `2`, `3`, or `4`? Also, why does Open Addressing slow
down much more drastically than Separate Chaining when the load factor $\alpha$
approaches `1.0`?

---

## Final check

Run all three practice files from within the `lab_6/` directory:

```bash
python3 hash_functions_practice.py
python3 chaining_practice.py
python3 probing_practice.py
```

- Any unfinished function reports `[TODO]`.
- Any logic error or failed assertion reports `[FAIL]`.
- Any fully working function reports `[PASS]`.

When all checks pass, all three commands return exit code `0`.
