"""Provided checks for Lab 7."""

from functools import partial


def check_string_search(naive_search, rabin_karp, compute_prefix_function, kmp_search):
    """Run the algorithms' and prefix helper's checks; return an exit status."""
    examples = [
        ("overlapping matches", "ababa", "aba", [0, 2]),
        ("repeated characters", "aaaa", "aa", [0, 1, 2]),
        ("missing pattern", "abc", "xy", []),
        ("pattern longer than text", "ab", "abc", []),
        ("whole text", "abc", "abc", [0]),
        ("empty text", "", "a", []),
        ("last window", "xxabc", "abc", [2]),
        ("single character", "banana", "a", [1, 3, 5]),
        ("lecture example", "abacaabadcab", "aba", [0, 5]),
        ("rolling updates", "xx314152xx314", "314", [2, 10]),
    ]
    cases = []
    for search in (naive_search, rabin_karp, kmp_search):
        for name, text, pattern, expected in examples:
            cases.append((
                search.__name__ + ": " + name,
                partial(search, text, pattern),
                expected,
            ))

    # these inputs force hash collisions with q=2 under the ASCII encoding
    cases.extend([
        ("Rabin–Karp: reject collision", partial(rabin_karp, "c", "a", q=2), []),
        ("Rabin–Karp: match after collision", partial(rabin_karp, "ca", "a", q=2), [1]),
        ("Rabin–Karp: verify entire window", partial(rabin_karp, "acab", "ab", q=2), [2]),
    ])

    prefix_examples = [
        ("a", [0]),
        ("abcd", [0, 0, 0, 0]),
        ("aaaa", [0, 1, 2, 3]),
        ("ababaca", [0, 0, 1, 2, 3, 0, 1]),
        ("aabaaab", [0, 1, 0, 1, 2, 2, 3]),
    ]
    for pattern, expected in prefix_examples:
        cases.append((
            "Prefix table: " + pattern,
            partial(compute_prefix_function, pattern),
            expected,
        ))

    cases.extend([
        ("KMP: lecture fallback", partial(kmp_search, "abababacaba", "ababaca"), [2]),
        ("KMP: repeated fallbacks", partial(kmp_search, "abababacabaababaca", "ababaca"), [2, 11]),
        ("KMP: fallback then extend", partial(kmp_search, "aabaaabaaab", "aabaaab"), [0, 4]),
        ("KMP: repeated partial matches", partial(kmp_search, "a" * 20, "aaab"), []),
    ])

    failed = 0
    for name, search, expected in cases:
        try:
            actual = search()
            if actual != expected:
                raise AssertionError(f"expected {expected}, got {actual!r}")
            print("[PASS] " + name)
        except NotImplementedError as error:
            failed += 1
            print("[TODO] " + name + ": " + str(error))
        except Exception as error:
            failed += 1
            print("[FAIL] " + name + ": " + type(error).__name__ + ": " + str(error))

    print(f"{len(cases) - failed}/{len(cases)} checks passed")
    return 1 if failed else 0
