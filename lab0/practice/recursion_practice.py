"""Practice: complete the recursive factorial function."""


def factorial(n):
    """Return n! for a nonnegative integer n."""
    if n < 0:
        raise ValueError("factorial is not defined for negative integers")

    # TODO: Add the base case. Remember that 0! is 1.
    if n == 0:
        return 1

    # TODO: Return n multiplied by factorial(n - 1).
    return n * factorial(n-1)
    raise NotImplementedError("Complete factorial")


def main():
    print(f"3! = {factorial(3)}")  # Expected: 6
    print(f"5! = {factorial(5)}")  # Expected: 120


if __name__ == "__main__":
    main()
