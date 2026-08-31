def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    if n not in cache:
        cache[n] = fibonacci(n-1) + fibonacci(n-2)
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
        result = fibonacci(int(text))
        end = time.perf_counter()
        print(f"fibonacci({int(text)}) = {result}, calculating this took {end - start:.4e} seconds.")
