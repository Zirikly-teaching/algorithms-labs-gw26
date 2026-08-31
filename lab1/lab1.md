# CSCI 3212 Lab 1

## Fibonacci numbers

Source: https://en.wikipedia.org/wiki/Fibonacci_sequence  

The Fibonacci sequence is a sequence of numbers where:  
1. The first and second numbers are both ``1``, that is, ``fibonacci(1) = fibonacci(2) = 1``
2. The numbers that follow are the sum of the previous TWO numbers, so  
``fibonacci(3) = fibonacci(2) + fibonacci(1) = 1 + 1 = 2``  
``fibonacci(4) = fibonacci(3) + fibonacci(2) = 2 + 1 = 3``.

```
TODO: Answer the following questions:
fibonacci(5) = 
fibonacci(6) = 
fibonacci(7) = 
fibonacci(8) = 
fibonacci(9) = 
```

## Basic implementation

Let's take a look at an implementation:
```python
def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)
```
You can also find this in ``algorithms-labs-gw26/lab1/fibonacci.py``, and run it: 
```bash
cd algorithms-labs-gw26/lab1
python fibonacci.py
```
The code version also tells you how much time does it take to complete each calculation.
```
TODO:
1. Explain what the code above is doing.
A: 
2. What happens if we remove the "if ... return ..." and only keep the last line?
A: 
3. What is fibonacci(20)? how much time did it take to calculate that?
A: 
4. What is fibonacci(30)? how much time did it take to calculate that?
A: 
5. How much time did it take you to calculate fibonacci(40)? (this might take a while...)
A: 
```

## How many function calls?

Modify ``fibonacci_counting.py`` so that it does the same calculation as ``fibonacci.py``, but it also counts how many times the function ``fibonacci(n)`` had to be called. Then answer the following:
```
TODO:
1. How many function calls does fibonacci(1) take?
2. How many function calls does fibonacci(5) take?
3. How many function calls does fibonacci(10) take?
4. Why is it so slow? Where does the complexity come from?
5. Is this O(n)? is this O(2^n)? Why?
6. Is this Ω(n)? Why?
```

## Memoization Optimization

Take a look at ``fibonacci_counting.py``, where memoization is used.
```
TODO:
1. How is this one different from the previous one?
2. How much time does it take to calculate fibonacci(30)?
3. Why is it often faster?
4. Also modify this file to count: how many times the function had to be called for fibonacci(30)?
5. Is this O(n)? is this O(2^n)? Why?
6. Is this Ω(n)? is this Ω(2^n)? Why?
```

## Extension: Staircase Problem

Implement ``fibonacci_threeway.py``, where:
1. The first, second, and third numbers are ``1``.
2. The numbers afterwards are the sum of the previous **THREE** numbers, instead of two.
3. Your implementation should be optimized, taking less than 1 second to calculate ``fibonacci_threeway(50)``.

## Optional, challenge problems
1. Instead of recursion, implement ``fibonacci(n)`` using iteration instead.
2. ``fibonacci_memoized.py`` fails if you give it a very large input number such as one million - why? Try fixing it.
3. There is an even faster way to calculate fibonacci numbers, in (almost) O(1) time. Read Wikipedia and try to implement it, or if you like a big challenge, implement it without looking it up.