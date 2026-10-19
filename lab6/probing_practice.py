"""Part 3: implement Open Addressing with Linear Probing insert and lookup.

OpenAddressingHashTable container and probe_index helper are provided.
"""


class OpenAddressingHashTable:
  """Open Addressing hash table storing [key, value] pairs directly in slots."""

  def __init__(self, capacity=7):
    self.capacity = capacity
    self.size = 0
    self.slots = [None] * capacity

  def __repr__(self):
    return (
      "OpenAddressingHashTable(capacity=" + str(self.capacity)
      + ", size=" + str(self.size) + ")"
    )


def probe_index(key, i, m):
  """Provided: return the slot index for probe step i using Linear Probing.

  Formula: ((key mod m) + i) mod m
  """
  return ((key % m) + i) % m


def linear_probe_insert(table, key, value):
  """Insert or update (key, value) in table using Linear Probing.

  Loop i from 0 to table.capacity - 1:
  - Compute slot = probe_index(key, i, table.capacity) and probes = i + 1.
  - If table.slots[slot] is None: place [key, value] there, increment table.size,
    and return (slot, probes).
  - If table.slots[slot][0] == key: update table.slots[slot][1] = value (do not
    change table.size) and return (slot, probes).
  - If the loop finishes without finding a slot, raise OverflowError("Hash table is full").
  """
  # TODO 3.2A: Probe along probe_index(key, i, table.capacity) to insert or update [key, value].
  raise NotImplementedError("Complete linear_probe_insert")


def linear_probe_lookup(table, key):
  """Search for key in table using Linear Probing; return (value_or_None, probes_count).

  Loop i from 0 to table.capacity - 1:
  - Compute slot = probe_index(key, i, table.capacity) and probes = i + 1.
  - If table.slots[slot] is None: stop immediately and return (None, probes).
  - If table.slots[slot][0] == key: return (table.slots[slot][1], probes).
  - If all slots are checked without a match, return (None, table.capacity).
  """
  # TODO 3.2B: Trace the linear probe path and stop on key match or empty slot (None).
  raise NotImplementedError("Complete linear_probe_lookup")


if __name__ == "__main__":
  from lab_checks import check_probing
  raise SystemExit(
    check_probing(
      probe_index,
      linear_probe_insert,
      linear_probe_lookup,
    )
  )
