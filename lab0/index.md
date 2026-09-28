---
layout: default
title: Lab 0
nav_order: 2
permalink: /lab0/
---

# Lab 0: Python Setup and Recursion

This lab starts with a short Python development setup and two warm-up exercises. The course material that follows is a Python adaptation of Professor Rahul Simha's [Module 4: Recursion, Part I](https://www2.seas.gwu.edu/~simhaweb/cs1112/modules/module4/module4.html). It follows the original order, explanations, examples, and exercises; the programs have been converted from Java to Python.

## On this page

1. TOC
{:toc}

---

## Part 1: Python development setup

### Install Python

1. Download a current Python 3 release from [python.org/downloads](https://www.python.org/downloads/).
2. Run the installer. On Windows, allow the installer to add Python to `PATH` if that option is shown.
3. Open a new terminal and verify the installation:

```bash
python --version
```

On some macOS and Linux systems, the command is:

```bash
python3 --version
```

On Windows, the Python launcher also supports:

```powershell
py --version
```

You should see `Python 3.x.x`. If the command is not found, restart the terminal and check that Python was added to `PATH`.

### Install and configure VS Code

1. Download and install [Visual Studio Code](https://code.visualstudio.com/Download).
2. In VS Code, open **Extensions** and install the Microsoft **Python** extension.
3. Open the Command Palette with <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> (Windows/Linux) or <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> (macOS).
4. Run **Python: Select Interpreter** and choose the Python 3 installation you just verified.

VS Code is the editor, the Python extension adds editor support, and the Python interpreter is the program that actually runs your code. The [official VS Code Python tutorial](https://code.visualstudio.com/docs/python/python-tutorial) has a longer setup walkthrough.

### Create and run a Python file

Create a folder for your lab work, open it in VS Code, and create a file named `hello.py`:

```python
print("Hello, algorithms!")
```

Open VS Code's terminal with **Terminal → New Terminal**, then run:

```bash
python hello.py
```

Use `python3 hello.py` on a system where the interpreter command is `python3`. You can also use the **Run Python File** button in the upper-right corner of the editor.

{: .setup }
> Your setup is ready when the terminal prints `Hello, algorithms!` and exits without an error.

### What is `pip`?

`pip` is Python's package installer. It downloads and installs libraries that are not part of Python's standard library. Check that it is available with:

```bash
python -m pip --version
```

Install a library with:

```bash
pip install package-name
```

Using `python -m pip` makes it explicit which Python interpreter receives the package:

```bash
python -m pip install package-name
```

On Windows you may use `py -m pip`; on some macOS/Linux systems use `python3 -m pip`. See the [official pip getting-started guide](https://pip.pypa.io/en/stable/getting-started/) for more commands. Lab 0 itself uses only the standard library, so it does not require any packages.

### Git in one minute

Git records changes to a project. A repository is the project plus its history. The short workflow you will use most often is:

```bash
git clone REPOSITORY-URL   # Make your local copy once.
git pull                   # Get changes from the remote repository.
git status                 # See which files you changed.
git add FILE-NAME          # Stage a file for a commit.
git commit -m "Message"    # Record the staged changes locally.
git push                   # Send your commits to the remote repository.
```

Run commands from the repository folder. Use `git status` before committing so you know exactly what will be recorded. The [Git reference and cheat sheet](https://git-scm.com/docs) cover these and other common commands.

---

## Part 2: Python warm-up

### Basic syntax: addition

Python variables do not need declared types, statements do not end with semicolons, and indentation marks blocks of code.

```python
a = 5
b = 3

result = a + b
print(result)
```

Run the complete example:

```bash
python lab0/examples/addition.py
```

[View `addition.py`]({{ '/lab0/examples/addition.py' | relative_url }})

{: .exercise }
> Open [`addition_practice.py`]({{ '/lab0/practice/addition_practice.py' | relative_url }}). Replace the `TODO` items so the program adds `a` and `b`, stores the answer in `result`, and prints it. Then change the operation to multiplication and run the file again.

### A first recursive function

A recursive function calls itself. It needs a **base case** that returns without another recursive call, and each recursive call must move toward that case. Here is factorial, where `n!` is the product of the integers from `n` down to `1`:

```python
def factorial(n):
    if n < 0:
        raise ValueError("factorial is not defined for negative integers")
    if n == 0:                 # Base case
        return 1
    return n * factorial(n - 1)


print(factorial(5))            # 120
```

Run the complete example:

```bash
python lab0/examples/recursion.py
```

[View `recursion.py`]({{ '/lab0/examples/recursion.py' | relative_url }})

{: .exercise }
> Complete the base case and recursive return in [`recursion_practice.py`]({{ '/lab0/practice/recursion_practice.py' | relative_url }}). Run it and confirm that `factorial(3)` is `6` and `factorial(5)` is `120`.

---

## Part 3: Recursion, Part I

### A simple example

We begin with repeated multiplication to compute integer powers. For example,

**2<sup>4</sup> = 2 × 2 × 2 × 2 = 16.**

First consider the direct approach using a loop:

```python
def power(a, b):
    p = 1                       # a^0
    while b > 0:
        p = p * a               # Repeat b times.
        b -= 1
    return p


print(f"3^2 = {power(3, 2)}")
print(f"3^4 = {power(3, 4)}")
print(f"2^8 = {power(2, 8)}")
```

Now look at a recursive version of the same computation:

```python
def power(a, b):
    if b == 0:
        p = 1
    else:
        # The function calls itself:
        p = a * power(a, b - 1)
    return p


print(f"3^2 = {power(3, 2)}")
print(f"3^4 = {power(3, 4)}")
print(f"2^8 = {power(2, 8)}")
```

How does this work?

- Every successive call reduces `b` by `1`, so eventually `b == 0`.
- At `b == 0`, the base case returns `1`. That produces a cascade of returns to the earlier function calls.
- The essential point is that successive recursive calls to `power()` change something—here, `b`—so the recursion comes to an end.
- `a` does not change. It passes a value used in the calculation, but it does not decide how the recursion progresses.

To see the calls more clearly, print the level during each call:

```python
def make_blanks(n):
    return "  " * n


def power(a, b, level):
    print(f"{make_blanks(level)}Level {level}: b={b}")

    if b == 0:
        p = 1
    else:
        p = a * power(a, b - 1, level + 1)

    print(f"{make_blanks(level)}Level {level}: p={p}")
    return p


p = power(3, 2, 0)
print(f"3^2 = {p}")
```

Here is the annotated output:

```text
Level 0: b=2              # First call: a=3, b=2
  Level 1: b=1            # First recursive call
    Level 2: b=0          # Second recursive call
    Level 2: p=1          # Base case: recursion bottoms out
  Level 1: p=3            # Return to the call where b=1
Level 0: p=9              # Return to the original call
3^2 = 9
```

For `3^4`, four recursive calls take `b` down to `0`; the return values then build from `1` to `3`, `9`, `27`, and finally `81`.

### The call stack

The memory used for these active calls is the **stack**.

![Stack frames while recursively computing 3 squared]({{ '/lab0/images/Recursion_Pow3.jpg' | relative_url }})

- When a function is called, a stack frame stores its parameters and local variables. In this example, those include `a`, `b`, and `p`.
- When the function finishes, its frame disappears from the stack.
- When one function calls another, the new call receives its own frame. The caller's frame remains available until execution returns to it.
- The first call to `power()` creates a frame with `a = 3` and `b = 2`.
- The next call creates a separate frame with `a = 3` and `b = 1`.
- A third call has `a = 3` and `b = 0`. It does not recurse; it returns `1`.
- That `1` goes back to the second call and is multiplied by `a`, producing `3`.
- The second call returns `3` to the first call, where it is multiplied by `a` to produce `9`.
- Finally, `9` is returned to the original caller.

The gray area in each frame in the diagram represents bookkeeping information used to manage function calls.

{: .exercise }
> **In-Class Exercise 1.** On paper, show what happens when the program computes 4<sup>3</sup>. Draw the stack at each step.

The recursive function can be written more compactly:

```python
def power(a, b):
    if b == 0:
        return 1
    return a * power(a, b - 1)
```

This shorter form does not change the execution; it only makes the code more compact.

{: .exercise }
> **In-Class Exercise 2.** Implement a recursive function that computes the sum of the first `n` positive integers. For example, `sum_first(4)` should return `10`.

### Factorial

The factorial of an integer `n` is defined as

**n! = n × (n − 1) × (n − 2) × ... × 2 × 1.**

For example, **5! = 5 × 4 × 3 × 2 × 1 = 120**. We multiply `n` by `n - 1`, then by `n - 2`, and continue until multiplying by `1`.

```python
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


print(f"3! = {factorial(3)}")
print(f"5! = {factorial(5)}")
print(f"5! x 3! = {factorial(3) * factorial(5)}")
```

{: .exercise }
> **In-Class Exercise 3.** Add the kind of indented tracing used in the power example. Add a `level` parameter, print when a call begins, and print the result just before each call returns.

### Which parameter controls the recursion?

Factorial has one parameter. The power example has two:

```python
def power(a, b):
    pass
```

Here, `b` changes and controls the recursion. The parameter `a` is used in the calculation but is not essential to the recursive progress. To demonstrate, the original experiment makes `a` a global value:

```python
a = 0


def power(b):
    if b == 0:
        p = 1
    else:
        p = a * power(b - 1)

    print(f"Intermediate result: {a}^{b}={p}")
    return p


a = 3
print(f"3^2 = {power(2)}")
print(f"3^4 = {power(4)}")

a = 2
print(f"2^8 = {power(8)}")
```

{: .note }
> This global-variable version reproduces the source experiment; passing values as parameters is normally clearer. The point is that moving unchanged `a` outside the parameter list does not change the recursive progress controlled by `b`.

{: .exercise }
> **In-Class Exercise 4.** Run the program and explain why making `a` global does not change the returned powers.

Next, make the controlling value `b` global too:

```python
a = 0
b = 0


def power():
    global b

    if b == 0:
        p = 1
    else:
        b = b - 1
        p = a * power()

    print(f"Intermediate result: {a}^{b}={p}")
    return p


a = 3
b = 2
print(f"3^2 = {power()}")

b = 4
print(f"3^4 = {power()}")

a = 2
b = 8
print(f"2^8 = {power()}")
```

{: .exercise }
> **In-Class Exercise 5.** Run this parameterless version and explain its output. In particular, follow the single global `b` while calls return, and compare it with the separate `b` value stored in each stack frame of the parameterized version.

---

### Searching a list via recursion

We know how to loop through a list to search for a particular value. Here is the same task using recursion:

```python
import random


def make_random_list(length):
    return [random.randint(1, 100) for _ in range(length)]


def search(values, value, index):
    # Two base cases:
    if index >= len(values):
        return False
    if values[index] == value:
        return True

    # Otherwise, search farther into the list.
    return search(values, value, index + 1)


test_data = make_random_list(10)
search_term = random.randint(1, 100)
found = search(test_data, search_term, 0)

print(test_data)
print(f"search_term={search_term}")
print(f"found={found}")
```

Notice the following:

- `search()` has three parameters, but only `index` controls the recursion.
- There are two ways to bottom out:
  - If `index` reaches the length of the list, the value was not found, so return `False`.
  - If `values[index]` equals the target value, return `True`.
- The search begins at index `0`.
- This program has the characteristic parts of a recursive function:
  - At least one parameter controls the recursion.
  - The base cases check that controlling parameter, possibly together with other parameters.
  - Each recursive call reduces the remaining problem by changing the controlling parameter.

{: .exercise }
> **In-Class Exercise 6.** What happens if the two `if` statements are switched so the program accesses `values[index]` before checking whether `index` is outside the list? Test a value that is not present and explain the error.

### Palindrome checking

Use this idea to test whether a string is a palindrome: if its first and last characters match, then the string left after removing those characters must itself be a palindrome.

```python
def check_palindrome(text):
    # Two base cases combined into one:
    if len(text) == 0 or len(text) == 1:
        return "is a palindrome"

    if text[0] != text[-1]:
        return "is not a palindrome"

    # The ends match. Remove them and check the remainder.
    next_text = text[1:-1]
    return check_palindrome(next_text)


for text in ["redder", "river", "neveroddoreven"]:
    print(text, check_palindrome(text))
```

The return value here is a string. The function could instead return `True` or `False`.

{: .exercise }
> **In-Class Exercise 7.** Rewrite `check_palindrome()` so it works on a list of individual characters, such as `['r', 'e', 'd', 'd', 'e', 'r']`, rather than on a string.

---

### Solving a combinatorial problem using recursion

Consider the problem of seating people in a row:

- There are `K` speakers, and each must be assigned a seat on a panel.
- There are `M` seats, where `M >= K`.
- In how many different ways can the speakers be seated?

With `K = 2` speakers and `M = 3` seats, the six arrangements are:

```text
1 2 _
1 _ 2
2 1 _
2 _ 1
_ 1 2
_ 2 1
```

First, count the arrangements without printing them:

```python
def count_permutations(num_spaces, num_remaining):
    # If nobody remains, there is one completed arrangement.
    if num_remaining == 0:
        return 1

    # Count a smaller problem, then account for the available seat.
    n = count_permutations(num_spaces - 1, num_remaining - 1)
    return num_spaces * n


num_seats = 3
num_people = 2
n = count_permutations(num_seats, num_people)
print(f"{num_people} people can sit in {num_seats} seats in {n} arrangements")
```

The reasoning is:

- To assign `K` people among `M` seats, the first person can choose from `M` seats.
- The remaining `K - 1` people must be assigned among the remaining `M - 1` seats.
- Multiply the two counts.

Now modify the program to print the actual arrangements:

```python
count = 0


def print_permutations(num_spaces, num_remaining, seats, person):
    global count

    # Each time this base case is reached, one arrangement is complete.
    if num_remaining == 0:
        print(seats)
        count += 1
        return

    # Find an empty seat for the current person.
    for i in range(len(seats)):
        if seats[i] == 0:
            seats[i] = person
            print_permutations(
                num_spaces - 1,
                num_remaining - 1,
                seats,
                person + 1,
            )

            # Undo the choice before trying another seat.
            seats[i] = 0


num_seats = 3
num_people = 2
seats = [0] * num_seats
count = 0
print_permutations(num_seats, num_people, seats, 1)
print(f"=> {count} permutations")
```

The list `seats` records an arrangement: each position is a seat, and the value in that position identifies the person seated there. The recursive function now has two additional parameters:

```python
def print_permutations(num_spaces, num_remaining, seats, person):
    pass
```

- `seats` carries the arrangement that will be printed at the base case.
- `person` identifies the speaker being seated by the current call.
- Seat person `1`, then person `2`, and so on.
- For person `i`, choose an available position and recursively seat the people beginning with `i + 1`.
- When no one remains, the current arrangement is complete and can be printed.

Most importantly, each choice must be undone before the loop explores the next possibility:

```python
seats[i] = person
print_permutations(num_spaces - 1, num_remaining - 1, seats, person + 1)
seats[i] = 0
```

For two people and three seats, the output is:

```text
[1, 2, 0]
[1, 0, 2]
[2, 1, 0]
[0, 1, 2]
[2, 0, 1]
[0, 2, 1]
=> 6 permutations
```

With two people and five seats, the same program produces `20` arrangements.

Another way to handle the undo step is to pass a fresh copy into every recursive call:

```python
def print_permutations(num_spaces, num_remaining, seats, person):
    global count

    if num_remaining == 0:
        print(seats)
        count += 1
        return

    for i in range(len(seats)):
        if seats[i] == 0:
            seats_copy = seats.copy()
            seats_copy[i] = person
            print_permutations(
                num_spaces - 1,
                num_remaining - 1,
                seats_copy,
                person + 1,
            )
```

This version modifies a fresh list. Because each recursive call receives its own copy, there is no seating choice to undo afterward.

Now add a restriction: person `1` may not sit at either end. Positions `0` and `M - 1` are therefore banned for person `1`.

```python
def print_permutations(num_spaces, num_remaining, seats, person):
    global count

    if num_remaining == 0:
        print(seats)
        count += 1
        return

    for i in range(len(seats)):
        # Person 1 cannot sit at either end.
        if person == 1 and (i == 0 or i == len(seats) - 1):
            continue

        if seats[i] == 0:
            seats[i] = person
            print_permutations(
                num_spaces - 1,
                num_remaining - 1,
                seats,
                person + 1,
            )
            seats[i] = 0
```

---

### Another combinatorial example

Suppose we are at one Manhattan intersection and want to reach another. Many shortest paths have the same length. We want to count all such paths. First, represent the streets as a simple grid:

![A five-by-three grid from coordinate zero zero to coordinate five three]({{ '/lab0/images/img1.png' | relative_url }})

From `(0, 0)`, every shortest path must begin in one of two ways: move one column or move one row. Therefore, the number of paths for the full problem is the sum of the numbers of paths for those two smaller problems.

![The path count from zero zero is split into two smaller path counts]({{ '/lab0/images/img2.png' | relative_url }})

We can write the same problem in reverse, as moving from `(5, 3)` to `(0, 0)`. From a general point `(r, c)`, one smaller problem reduces the row and the other reduces the column.

![The path count from five three to zero zero splits by reducing either coordinate]({{ '/lab0/images/img3.png' | relative_url }})

Compute each smaller problem recursively and add the results:

```python
def count_paths(num_rows, num_cols):
    # If either coordinate is zero, only one straight path remains.
    # Notice that this condition uses "or", not "and".
    if num_rows == 0 or num_cols == 0:
        return 1

    # Reduce the problem to two smaller problems.
    down_count = count_paths(num_rows - 1, num_cols)
    right_count = count_paths(num_rows, num_cols - 1)
    return down_count + right_count


for r, c in [(1, 1), (2, 2), (5, 7)]:
    n = count_paths(r, c)
    print(f"r={r} c={c} => n={n}")
```

The recursive function `count_paths()` makes two recursive calls:

- `count_paths(num_rows - 1, num_cols)` creates a smaller problem with fewer rows.
- `count_paths(num_rows, num_cols - 1)` creates a smaller problem with fewer columns.

{: .exercise }
> **In-Class Exercise 8.** Why must the base-case condition use `or`? What happens if it is replaced by `and`? Then determine how many shortest paths connect the corner of Park and 55th to the corner of 2nd and 50th.

Next, print the different paths. For `(2, 2)` to `(0, 0)`, the output should be:

```text
[2,2] -> [1,2] -> [0,2] -> [0,1] -> [0,0]
[2,2] -> [1,2] -> [1,1] -> [0,1] -> [0,0]
[2,2] -> [1,2] -> [1,1] -> [1,0] -> [0,0]
[2,2] -> [2,1] -> [1,1] -> [0,1] -> [0,0]
[2,2] -> [2,1] -> [1,1] -> [1,0] -> [0,0]
[2,2] -> [2,1] -> [2,0] -> [1,0] -> [0,0]
```

There are six paths. Pass a string through the recursive calls and append each coordinate. When the recursion reaches a base case, the complete path is ready to print.

```python
def count_paths(num_rows, num_cols, partial_path):
    # Complete a path that has reached the top row.
    if num_rows == 0:
        final_path = partial_path
        for c in range(num_cols - 1, -1, -1):
            final_path += f" -> [0,{c}]"
        print(final_path)
        return 1

    # Complete a path that has reached the first column.
    if num_cols == 0:
        final_path = partial_path
        for r in range(num_rows - 1, -1, -1):
            final_path += f" -> [{r},0]"
        print(final_path)
        return 1

    # Otherwise, reduce the problem in both possible ways.
    down_path = partial_path + f" -> [{num_rows - 1},{num_cols}]"
    down_count = count_paths(num_rows - 1, num_cols, down_path)

    right_path = partial_path + f" -> [{num_rows},{num_cols - 1}]"
    right_count = count_paths(num_rows, num_cols - 1, right_path)

    return down_count + right_count


for r, c in [(1, 1), (2, 2)]:
    n = count_paths(r, c, f"[{r},{c}]")
    print(f"r={r} c={c} => n={n}")
```

The path is represented by a string that grows as the recursion moves downward. Printing happens at a base case because the string then contains a full path. The two base cases require different finishing steps: one completes the remaining columns and the other completes the remaining rows.

{: .exercise }
> **In-Class Exercise 9.** Modify the program so it labels its output `Path #1:`, `Path #2:`, and so on.

---

### Unnecessary recursion

Recursion is not always the best solution. A simple loop often works well and may be easier to write; searching a list is one example. Recursion can also repeat a great deal of work, as the next example shows.

The standard Fibonacci sequence begins:

```text
1st Fibonacci number: 0
2nd Fibonacci number: 1
3rd Fibonacci number: 1
4th Fibonacci number: 2
5th Fibonacci number: 3
6th Fibonacci number: 5
7th Fibonacci number: 8
...
```

The `n`th value is the sum of the preceding two:

**f<sub>n</sub> = f<sub>n−1</sub> + f<sub>n−2</sub>.**

This definition is an obvious candidate for recursion:

```python
def fibonacci(n):
    # Base cases:
    if n == 1:
        return 0
    if n == 2:
        return 1

    f_n_minus_one = fibonacci(n - 1)
    f_n_minus_two = fibonacci(n - 2)
    return f_n_minus_one + f_n_minus_two


for n in [5, 20]:
    print(f"f({n}) = {fibonacci(n)}")
```

The earlier terms are computed recursively. The same function can be written more compactly:

```python
def fibonacci(n):
    if n <= 2:
        return n - 1
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Now count how often `fibonacci()` is called:

```python
num_calls = 0


def fibonacci(n):
    global num_calls
    num_calls += 1

    if n <= 2:
        return n - 1
    return fibonacci(n - 1) + fibonacci(n - 2)


for n in [5, 20]:
    num_calls = 0
    f = fibonacci(n)
    print(f"f({n}) = {f}    num_calls={num_calls}")
```

For `n = 5`, the function is called `9` times. For `n = 20`, it is called `13,529` times.

{: .exercise }
> **In-Class Exercise 10.** Before continuing, explain why the recursive version makes so many calls.

To avoid repeated work, store values after computing them. When a previously computed value is needed, read it from the list rather than making the same recursive call again.

```python
num_calls = 0
f_values = []


def fibonacci(n):
    global num_calls
    num_calls += 1

    if n <= 2:
        f_values[n] = n - 1
        return n - 1

    if f_values[n - 1] is None:
        f_values[n - 1] = fibonacci(n - 1)
    if f_values[n - 2] is None:
        f_values[n - 2] = fibonacci(n - 2)

    f_values[n] = f_values[n - 1] + f_values[n - 2]
    return f_values[n]


for n in [5, 20]:
    num_calls = 0
    f_values = [None] * (n + 1)
    f = fibonacci(n)
    print(f"f({n}) = {f}    num_calls={num_calls}")
```

Now `n = 5` takes `5` calls and `n = 20` takes `20` calls. The number of calls grows linearly with `n`, although the stored values require additional space.

Fibonacci numbers are also easy to compute iteratively without a list:

```python
def fibonacci(n):
    if n == 1:
        return 0
    if n == 2:
        return 1

    f_previous = 1
    f_previous_previous = 0

    for _ in range(3, n + 1):
        f = f_previous + f_previous_previous
        f_previous_previous = f_previous
        f_previous = f

    return f
```

{: .exercise }
> **In-Class Exercise 11.** Add a call counter to the recursive Manhattan-path program. Then store previously computed path counts and see how much this reduces the number of recursive calls.

---

## Lab files

Complete examples:

- [`examples/addition.py`]({{ '/lab0/examples/addition.py' | relative_url }})
- [`examples/recursion.py`]({{ '/lab0/examples/recursion.py' | relative_url }})

Practice starters:

- [`practice/addition_practice.py`]({{ '/lab0/practice/addition_practice.py' | relative_url }})
- [`practice/recursion_practice.py`]({{ '/lab0/practice/recursion_practice.py' | relative_url }})

## Source and attribution

The recursion lesson follows Rahul Simha, [Module 4: Recursion, Part I](https://www2.seas.gwu.edu/~simhaweb/cs1112/modules/module4/module4.html), © 2006, revised 2017. The examples on this page translate the original Java programs into Python while retaining the source lesson's progression and exercises.
