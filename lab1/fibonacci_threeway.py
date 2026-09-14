# fibonacci_threeway(negative number) = 0
# fibonacci_threeway(0) = 0
# fibonacci_threeway(1) = 1
# fibonacci_threeway(2) = 1
# fibonacci_threeway(3) = 1
# fibonacci_threeway(4) = 1 + 1 + 1 = 3
# and so on...

def fibonacci_threeway(n):
    if n <= 0:
        return 0
    if n == 1 or n == 2 or n == 3:
        return 1
    if n not in cache:
        cache[n] = fibonacci_threeway(n-1) + fibonacci_threeway(n-2) + fibonacci_threeway(n-3)
    return cache[n]

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
        start = time.perf_counter()
        result = fibonacci_threeway(int(text))
        end = time.perf_counter()
        print(f"fibonacci_threeway({int(text)}) = {result}, calculating this took {end - start:.4e} seconds.")
