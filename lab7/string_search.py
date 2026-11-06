"""Complete the string-search algorithms and prefix helper for Lab 7."""


def naive_search(text, pattern):
    """Return all matching starting indices, including overlapping matches.

    Inputs are ASCII strings and pattern is nonempty.
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    matches = []

    for shift in range(n - m + 1):
        j = 0
        while j < m and text[shift + j] == pattern[j]:
            j += 1
        if j == m:
            matches.append(shift)

    return matches


def rabin_karp(text, pattern, d=256, q=101):
    """Return all matching starting indices using a rolling hash.

    Inputs are ASCII strings, pattern is nonempty, and q is a positive prime.
    Use ord(character) for character codes and verify every hash hit.
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    matches = []
    h = pow(d, m - 1, q)
    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for shift in range(n - m + 1):
        if p == t:
            j = 0
            while j < m and text[shift + j] == pattern[j]:
                j += 1
            if j == m:
                matches.append(shift)
        if shift < n - m:
            t = (d * (t - ord(text[shift]) * h) + ord(text[shift + m])) % q

    return matches


def compute_prefix_function(pattern):
    """Return the longest proper border length for each pattern prefix.

    pattern is nonempty. pi[j] describes pattern[0:j + 1].
    """
    m = len(pattern)
    pi = [0] * m
    k = 0

    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = pi[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        pi[i] = k

    return pi


def kmp_search(text, pattern):
    """Return all matching starting indices using the prefix table.

    Inputs are ASCII strings and pattern is nonempty.
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    matches = []
    pi = compute_prefix_function(pattern)
    q = 0

    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            matches.append(i - m + 1)
            q = pi[q - 1]

    return matches


if __name__ == "__main__":
    from lab_checks import check_string_search

    raise SystemExit(check_string_search(
        naive_search, rabin_karp, compute_prefix_function, kmp_search
    ))
