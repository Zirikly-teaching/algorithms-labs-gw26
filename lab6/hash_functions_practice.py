"""Part 1: implement the Division Method and Multiplication Method hash functions.

Golden Ratio conjugate constant A is provided.
"""

import math

GOLDEN_RATIO_A = (math.sqrt(5) - 1.0) / 2.0


def division_hash(key, m):
  """Map integer key to a slot in [0, m - 1] using the Division Method.

  Formula: h(k) = k mod m
  Preconditions: key is an integer, m > 0.
  """
  hash = key % m
  # TODO 1.2A: Return the remainder of key divided by table size m (using %).
  return hash


def multiplication_hash(key, m, A=GOLDEN_RATIO_A):
  """Map integer key to a slot in [0, m - 1] using the Multiplication Method.

  Formula: h(k) = floor(m * ((k * A) mod 1))
  Hint: In Python, ((key * A) % 1.0) extracts the fractional part after the decimal point.
  """
  fractional_part = (key * A) % 1.0
  hash = math.floor(m * fractional_part)
  # TODO 1.2B: Compute the fractional part of (key * A), multiply by m, and return math.floor(...).
  return hash


if __name__ == "__main__":
  from lab_checks import check_hash_functions
  raise SystemExit(
    check_hash_functions(
      division_hash,
      multiplication_hash,
    )
  )
