"""Provided checks for Lab 6. No third-party packages required."""

import math
import random


def require(condition, message):
  if not condition:
    raise AssertionError(message)


def run_checks(cases):
  """Run (name, zero-arg callable) pairs; return a process exit status.

  NotImplementedError -> [TODO]; any other exception -> [FAIL].
  """
  failed = 0

  for name, test in cases:
    try:
      test()
      print("[PASS] " + name)
    except NotImplementedError as error:
      failed += 1
      print("[TODO] " + name + ": " + str(error))
    except Exception as error:
      failed += 1
      print(
        "[FAIL] " + name + ": "
        + type(error).__name__ + ": " + str(error)
      )

  print(str(len(cases) - failed) + "/" + str(len(cases)) + " checks passed")
  return 1 if failed else 0


# Shared containers for test harness
class ChainingHashTable:
  def __init__(self, capacity=7, max_load=0.75):
    self.capacity = capacity
    self.max_load = max_load
    self.size = 0
    self.buckets = [[] for _ in range(capacity)]


class OpenAddressingHashTable:
  def __init__(self, capacity=7):
    self.capacity = capacity
    self.size = 0
    self.slots = [None] * capacity


# Test suites
def check_hash_functions(division_hash, multiplication_hash):
  def test_division_power_of_two_trap():
    # Keys from lecture slide 9 that all end in binary 011
    keys = [19, 51, 83, 115]
    results_mod8 = [division_hash(k, 8) for k in keys]
    require(
      results_mod8 == [3, 3, 3, 3],
      "All keys ending in binary 011 must hash to 3 under m=8, got " + str(results_mod8)
    )

  def test_division_prime_spread():
    keys = [19, 51, 83, 115]
    results_mod7 = [division_hash(k, 7) for k in keys]
    require(
      results_mod7 == [5, 2, 6, 3],
      "Expected [5, 2, 6, 3] under prime m=7, got " + str(results_mod7)
    )
    require(division_hash(0, 13) == 0, "division_hash(0, 13) must be 0")
    require(division_hash(26, 13) == 0, "division_hash(26, 13) must be 0")

  def test_multiplication_trace():
    keys = [19, 51, 83, 115]
    A = (math.sqrt(5) - 1.0) / 2.0
    results = [multiplication_hash(k, 8, A) for k in keys]
    require(
      results == [5, 4, 2, 0],
      "Expected [5, 4, 2, 0] for multiplication_hash on trace keys, got " + str(results)
    )

  def test_multiplication_bounds():
    A = (math.sqrt(5) - 1.0) / 2.0
    for k in range(50):
      idx = multiplication_hash(k, 16, A)
      require(0 <= idx < 16, "multiplication_hash index out of bounds [0, 15]")

  cases = [
    ("Division Method power-of-2 bit trap (m=8 on [19, 51, 83, 115])", test_division_power_of_two_trap),
    ("Division Method prime table size spread (m=7 on [19, 51, 83, 115])", test_division_prime_spread),
    ("Multiplication Method with Golden Ratio A on trace keys", test_multiplication_trace),
    ("Multiplication Method slot bounds check (m=16)", test_multiplication_bounds),
  ]

  return run_checks(cases)


def check_chaining(chaining_insert, chaining_lookup, chaining_delete, chaining_rehash):
  def test_trace_2_1_insertions():
    table = ChainingHashTable(capacity=7, max_load=0.75)
    pairs = [(12, "A"), (19, "B"), (24, "C"), (26, "D"), (31, "E")]
    for k, v in pairs:
      chaining_insert(table, k, v)

    require(table.capacity == 7, "Capacity must remain 7 for 5 items (alpha = 5/7 <= 0.75)")
    require(table.size == 5, "Table size must be 5")
    require(
      table.buckets[5] == [[12, "A"], [19, "B"], [26, "D"]],
      "Bucket 5 chain mismatch: " + str(table.buckets[5])
    )
    require(
      table.buckets[3] == [[24, "C"], [31, "E"]],
      "Bucket 3 chain mismatch: " + str(table.buckets[3])
    )

  def test_lookup_existing_and_missing():
    table = ChainingHashTable(capacity=7, max_load=0.75)
    for k, v in [(12, "A"), (19, "B"), (24, "C"), (26, "D"), (31, "E")]:
      chaining_insert(table, k, v)

    require(chaining_lookup(table, 12) == "A", "Lookup 12 must return 'A'")
    require(chaining_lookup(table, 19) == "B", "Lookup 19 must return 'B'")
    require(chaining_lookup(table, 26) == "D", "Lookup 26 (tail of chain) must return 'D'")
    require(chaining_lookup(table, 31) == "E", "Lookup 31 must return 'E'")
    require(chaining_lookup(table, 5) is None, "Missing key in occupied bucket 5 must return None")
    require(chaining_lookup(table, 0) is None, "Missing key in empty bucket 0 must return None")

  def test_update_existing_key():
    table = ChainingHashTable(capacity=7, max_load=0.75)
    chaining_insert(table, 12, "A")
    chaining_insert(table, 19, "B")
    chaining_insert(table, 12, "UPDATED")

    require(table.size == 2, "Updating existing key must not increment table.size")
    require(chaining_lookup(table, 12) == "UPDATED", "Updated value must be returned")
    require(len(table.buckets[5]) == 2, "Bucket 5 must still have 2 entries")

  def test_dynamic_resize_trigger():
    table = ChainingHashTable(capacity=4, max_load=0.75)
    chaining_insert(table, 10, "W")
    chaining_insert(table, 14, "X")
    chaining_insert(table, 18, "Y")
    require(table.capacity == 4, "Capacity at alpha = 3/4 = 0.75 must remain 4")

    # 4th insert pushes alpha = 4/4 = 1.0 > 0.75 -> triggers rehash to 8
    chaining_insert(table, 22, "Z")
    require(table.capacity == 8, "Capacity must double to 8 when alpha > 0.75")
    require(table.size == 4, "Size must remain 4 after rehash")
    require(chaining_lookup(table, 14) == "X", "Lookup 14 must succeed at new bucket after rehash")
    require(chaining_lookup(table, 22) == "Z", "Lookup 22 must succeed at new bucket after rehash")

  cases = [
    ("Separate Chaining Trace 2.1 insertions (M=7)", test_trace_2_1_insertions),
    ("Separate Chaining lookup on existing and missing keys", test_lookup_existing_and_missing),
    ("Separate Chaining in-place value update on duplicate key", test_update_existing_key),
    ("Dynamic resizing trigger when alpha > 0.75 (M=4 -> 2M=8)", test_dynamic_resize_trigger),
  ]

  return run_checks(cases)


def check_probing(probe_index, linear_probe_insert, linear_probe_lookup):
  def test_trace_3_1_insertions():
    table = OpenAddressingHashTable(capacity=7)
    s1, p1 = linear_probe_insert(table, 12, "v12")
    s2, p2 = linear_probe_insert(table, 19, "v19")
    s3, p3 = linear_probe_insert(table, 26, "v26")
    s4, p4 = linear_probe_insert(table, 3, "v3")
    s5, p5 = linear_probe_insert(table, 10, "v10")

    require((s1, p1) == (5, 1), "Insert 12 must land at slot 5 in 1 probe")
    require((s2, p2) == (6, 2), "Insert 19 must land at slot 6 in 2 probes")
    require((s3, p3) == (0, 3), "Insert 26 must wrap around to slot 0 in 3 probes")
    require((s4, p4) == (3, 1), "Insert 3 must land at slot 3 in 1 probe")
    require((s5, p5) == (4, 2), "Insert 10 must land at slot 4 in 2 probes")
    require(table.size == 5, "Table size must be 5")

  def test_trace_3_1_lookups():
    table = OpenAddressingHashTable(capacity=7)
    for k in [12, 19, 26, 3, 10]:
      linear_probe_insert(table, k, "val_" + str(k))

    # Lookup 26: probes 5 -> 6 -> 0 (3 probes)
    val_26, probes_26 = linear_probe_lookup(table, 26)
    require(val_26 == "val_26" and probes_26 == 3, "Lookup 26 must return ('val_26', 3)")

    # Lookup 33 (missing, 33 mod 7 = 5): probes 5 -> 6 -> 0 -> 1 (empty) (4 probes)
    val_33, probes_33 = linear_probe_lookup(table, 33)
    require(val_33 is None and probes_33 == 4, "Missing key 33 must stop at empty slot 1 in 4 probes")

  def test_update_and_full_table():
    table = OpenAddressingHashTable(capacity=3)
    linear_probe_insert(table, 1, "a")
    linear_probe_insert(table, 4, "b")
    slot, probes = linear_probe_insert(table, 4, "b_updated")
    require(table.size == 2, "Updating existing key in linear probing must not increase size")
    require(slot == 2 and probes == 2, "Updating collided key 4 must take 2 probes at slot 2")

    linear_probe_insert(table, 7, "c")
    full_raised = False
    try:
      linear_probe_insert(table, 10, "d")
    except OverflowError:
      full_raised = True
    require(full_raised, "Inserting into a full table must raise OverflowError")

  def demo_load_factor_and_clustering_profiling():
    # Self-contained demonstration comparing probe counts as alpha approaches 1.0
    m = 200
    rng = random.Random(3212)
    table = OpenAddressingHashTable(capacity=m)
    inserted = []

    def _demo_insert(tbl, k, v):
      for step in range(tbl.capacity):
        idx = ((k % tbl.capacity) + step) % tbl.capacity
        if tbl.slots[idx] is None:
          tbl.slots[idx] = [k, v]
          tbl.size += 1
          return
        if tbl.slots[idx][0] == k:
          tbl.slots[idx][1] = v
          return

    def _demo_lookup_probes(tbl, k):
      for step in range(tbl.capacity):
        idx = ((k % tbl.capacity) + step) % tbl.capacity
        if tbl.slots[idx] is None or tbl.slots[idx][0] == k:
          return step + 1
      return tbl.capacity

    report_lines = [
      "\n  [Demo] Linear Probing probe growth as table fills up (M = 200):"
    ]
    checkpoints = {100: 0.50, 150: 0.75, 180: 0.90, 190: 0.95}

    while table.size < 190:
      candidate = rng.randint(1, 100000)
      if candidate not in inserted:
        _demo_insert(table, candidate, candidate)
        inserted.append(candidate)
        if table.size in checkpoints:
          alpha = checkpoints[table.size]
          theory = 1.0 / (1.0 - alpha)
          missing_probes = []
          for probe_key in range(200000, 200200):
            p_cnt = _demo_lookup_probes(table, probe_key)
            missing_probes.append(p_cnt)
          avg_missing = sum(missing_probes) / len(missing_probes)
          report_lines.append(
            "         alpha = " + "{:.2f}".format(alpha)
            + " | Uniform 1/(1-alpha) = " + "{:5.1f}".format(theory)
            + " | Actual probes with clustering = "
            + "{:5.1f}".format(avg_missing)
          )

    print("\n".join(report_lines))

  cases = [
    ("Linear Probing Trace 3.1 insertions (M=7)", test_trace_3_1_insertions),
    ("Linear Probing Trace 3.1 lookups (present and missing keys)", test_trace_3_1_lookups),
    ("Linear Probing duplicate key update and full-table overflow", test_update_and_full_table),
    ("Load factor probe explosion demonstration", demo_load_factor_and_clustering_profiling),
  ]

  return run_checks(cases)
