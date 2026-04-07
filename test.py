#!/usr/bin/env python3
"""
Multiprocessing demo: compute the sum of factorials in parallel.

Each number in the input list is processed by a separate subprocess; results
are passed back to the parent via a shared :class:`~multiprocessing.Queue`.

Usage::

    python test.py
    5 3 4
    Sum of factorials is 150
"""

from multiprocessing import Process, Queue, set_start_method
from typing import List


def calculate_factorial(n: int, queue: "Queue[int]") -> None:
    """Compute ``n!`` and push the result onto the shared queue.

    Args:
        n: Non-negative integer whose factorial to compute.
        queue: Shared queue used to return the result to the parent process.
    """
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    queue.put(factorial)


def sum_of_factorials(numbers: List[int]) -> int:
    """Compute the sum of factorials concurrently using one subprocess per number.

    Args:
        numbers: List of non-negative integers.

    Returns:
        The value of ``sum(n! for n in numbers)``.
    """
    queue: "Queue[int]" = Queue()
    processes = [
        Process(target=calculate_factorial, args=(n, queue)) for n in numbers
    ]

    for process in processes:
        process.start()

    # Wait for all workers to finish before draining the queue
    for process in processes:
        process.join()

    total = 0
    while not queue.empty():
        total += queue.get()

    print(f"Sum of factorials is {total}")
    return total


if __name__ == "__main__":
    set_start_method("spawn")
    numbers = list(map(int, input().split()))
    sum_of_factorials(numbers)
