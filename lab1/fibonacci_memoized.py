def fibonacci(n):
    global call_count
    call_count += 1
    if n <= 1:
        return n

    prev2 = 0
    prev1 = 1

    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    return prev1

def is_positive_integer(text):
    try:
        return int(text) > 0
    except:
        pass
    return False

if __name__ == "__main__":
    import time
    while True:
        cache = {}
        text = input("Please enter a positive integer: ")
        if not is_positive_integer(text):
            continue
        call_count = 0
        start = time.perf_counter()
        result = fibonacci(int(text))
        end = time.perf_counter()
        print(f"fibonacci({int(text)}) = {result}, calculating this took {end - start:.4e} seconds.\nThe function \"fibonacci\" was called {call_count} times.")
