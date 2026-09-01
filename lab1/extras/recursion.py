"""A small recursion example using factorial."""


def factorial(n):
    """Return n! for a nonnegative integer n."""
    if n < 0:
        raise ValueError("factorial is not defined for negative integers")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def main():
    print(f"3! = {factorial(3)}")
    print(f"5! = {factorial(5)}")


if __name__ == "__main__":
    main()
