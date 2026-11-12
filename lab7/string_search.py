"""Complete the string-search algorithms and prefix helper for Lab 7."""


def naive_search(text, pattern):
    """Return all matching starting indices, including overlapping matches.

    Inputs are ASCII strings and pattern is nonempty.
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    matches = []

    # TODO 1.2: compare characters at each shift and collect complete matches
    for s in range(0, n - m):
        j = 0
        while j < m and text[s + j] == pattern[j]:
            j += 1
        if j == m:
            matches.append(s)

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

    def is_match(shift):
        for i in range(0, m):
            if text[shift + i] != pattern[i]:
                return False

        return True

    for j in range(0, m):
        p = (d * p + ord(pattern[j])) % q
        t = (d * t + ord(text[j])) % q

    for s in range(0, n - m + 1):
        if p == t and is_match(text, pattern, s):
            matches.append(s)
        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s + m])) % q

    return matches


def compute_prefix_function(pattern):
    """Return the longest proper border length for each pattern prefix.

    pattern is nonempty. pi[j] describes pattern[0:j + 1].
    """
    m = len(pattern)
    pi = [0] * m
    k = 0

    # TODO 3.2A: extend each border, following prefix links on a mismatch
    for j in range(1, m):
        while k > 0 and pattern[k] != pattern[j]:
            k = pi[k - 1]
        if pattern[k] == pattern[j]:
            k += 1
        pi[j] = k

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

    # TODO 3.2B: scan the text with prefix fallbacks and record all matches
    for i in range(0, n):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            matches.append(i - m + 1)
            q = pi[m - 1]

    return matches


if __name__ == "__main__":
    from lab_checks import check_string_search

    raise SystemExit(
        check_string_search(
            naive_search, rabin_karp, compute_prefix_function, kmp_search
        )
    )
