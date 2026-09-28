"""Practice: complete the recursive fibonacci function."""

def fibonacci(n):
    """Return the n-th fibonacci number for a given integer n."""
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative integers")

    # TODO: Add the base case. Note: Fib(0) is 0; Fib(1) is 1; Fib(2) is 1, so on.
    if n <= 2:
        return n - 1
    
    # TODO: Return fibonacci: 
    return fibonacci(n - 1) + fibonacci(n - 2)
    raise NotImplementedError("Complete fibonacci")


def main():
    print(f"Fib(3) = {fibonacci(3)}")  # Expected: 2
    print(f"Fib(5) = {fibonacci(5)}")  # Expected: 5
    print(f"Fib(20) = {fibonacci(20)}")  # Expected: 6765
    
    # See what happens when you try this:
    print(f"Fib(50) = {fibonacci(50)}")  # Expected: 12,586,269,025 (Python can handle this number)
    
    # Why does it happen? What is the time complexity of this implementation? How can we improve it?
    # Time complexity is exponential, we can make it better (linear) by avoiding repeated work (store values after computing them)

if __name__ == "__main__":
    main()
