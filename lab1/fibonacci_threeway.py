# fibonacci_threeway(negative number) = 0
# fibonacci_threeway(0) = 0
# fibonacci_threeway(1) = 1
# fibonacci_threeway(2) = 1
# fibonacci_threeway(3) = 1
# fibonacci_threeway(4) = 1 + 1 + 1 = 3
# and so on...

def fibonacci_threeway(n):
    raise NotImplementedError("TODO: replace this line in fibonacci_threeway.py with your solution!")

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
        start = time.perf_counter()
        result = fibonacci_threeway(int(text))
        end = time.perf_counter()
        print(f"fibonacci_threeway({int(text)}) = {result}, calculating this took {end - start:.4e} seconds.")
