def fibonacci(n):
    global call_count
    raise NotImplementedError("TODO: replace this line with one that not only calculates, but also counts how many times it has been called.")

def is_positive_integer(text):
    try:
        return int(text) > 0
    except:
        pass
    return False

if __name__ == "__main__":
    import time
    while True:
        text = input("Please enter a positive integer: ")
        if not is_positive_integer(text):
            continue
        call_count = 0
        start = time.perf_counter()
        result = fibonacci(int(text))
        end = time.perf_counter()
        print(f"fibonacci({int(text)}) = {result}\nCalculating this took {end - start:.4e} seconds\nThe function \"fibonacci\" was called {call_count} times.")
