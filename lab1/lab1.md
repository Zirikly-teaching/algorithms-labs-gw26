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
fibonacci(5) = fibonacci(4) + fibonacci(3) = 3 + 2 = 5
fibonacci(6) = fibonacci(5) + fibonacci(4) = 5 + 3 = 8
fibonacci(7) = fibonacci(6) + fibonacci(5) = 8 + 5 = 13
fibonacci(8) = fibonacci(7) + fibonacci(6) = 13 + 8 = 21
fibonacci(9) = fibonacci(8) + fibonacci(7) = 21 + 13 = 34
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
A: The code takes in the fibonacci number we want to calculate. It checks for the base cases, then use recursion to add the fibonacci of the number-1 and number-2, repeating until we get to the base case.
2. What happens if we remove the "if ... return ..." and only keep the last line?
A: If we only keep the last line, the function will run infinitely since there's no case to break the loop, leading to a stack overflow error.
3. What is fibonacci(20)? how much time did it take to calculate that?
A: fibonacci(20) = 6765, and it took 1.7566e-03 seconds to calculate.
4. What is fibonacci(30)? how much time did it take to calculate that?
A: fibonacci(30) = 832040, and it took 9.008e-02 second to calculate.
5. How much time did it take you to calculate fibonacci(40)? (this might take a while...)
A: fibonacci(40) = 102334155, and it took 7.649e+00 seconds to calculate.
```

## How many function calls?

Modify ``fibonacci_counting.py`` so that it does the same calculation as ``fibonacci.py``, but it also counts how many times the function ``fibonacci(n)`` had to be called. Then answer the following:
```
TODO:
1. How many function calls does fibonacci(1) take?
A: fibonacci(1) takes 1 function call.
2. How many function calls does fibonacci(5) take?
A: fibonacci(5) takes 15 function calls.
3. How many function calls does fibonacci(10) take?
A: fibonacci(10) takes 177 function calls.
4. Why is it so slow? Where does the complexity come from?
A: It is so slow because it runs the function but then needs to use recursion to call the former fibonnaci sequences. So for example, for fibonnaci(5), it needs to call fibonacci(4) which calls the function 9 times, and then it needs to call fibonacci(3) and so on. 
5. Is this O(n)? is this O(2^n)? Why?
A: This is O(2^n). If it was O(n), the number of function calls would grow at a constant rate. However, when we compare the function calls between each n, it does not grow at a constant rate. If we graph the amount of times that the function is called, we see a pattern matching a growth of O(2^n).
6. Is this Ω(n)? Why?
A: This is Ω(n). This is because the lowest bound the efficiency is constant. We can see this when we graph the amount of times that the function is called for each n. No matter what, it never goes below a constant rate of n, making the lower bound of Ω(n) work.
```

## Memoization Optimization

Take a look at ``fibonacci_counting.py``, where memoization is used.
```
TODO:
1. How is this one different from the previous one?
A: This code checks to see if fibonacci(n) is stored in a cache. If it's not, it calculates it then stores it in a cache.
2. How much time does it take to calculate fibonacci(30)?
A: It took 4.40209e-05 seconds to calculate fibonacci(30).
3. Why is it often faster?
A: It is often faster because once it calculates a fibonacci value and stores it in the cache, it can be called again.
4. Also modify this file to count: how many times the function had to be called for fibonacci(30)?
A: The function had to be called 59 times for fibonacci(30).
5. Is this O(n)? is this O(2^n)? Why?
A: This is O(n) because when graphing the number of times that the function is called for a specific n, it increases at a constant rate.
6. Is this Ω(n)? is this Ω(2^n)? Why?
A: This is Ω(n) because if the upper bound is constant, we can also say that the lower bound is also constantly increasing with an increase of n.
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