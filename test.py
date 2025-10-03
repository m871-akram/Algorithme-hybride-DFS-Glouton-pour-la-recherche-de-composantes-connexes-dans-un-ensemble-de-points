from multiprocessing import Process, set_start_method , Queue

def calculate_factorial(n,q):
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    q.put(factorial)


def sum_of_factorials(numbers):
    q=Queue()
    processes = [Process(target=calculate_factorial, args=(n, q)) for n in numbers]

    for p in processes:
        p.start()

    # Wait for all to finish
    for p in processes:
        p.join()

    # Collect results
    results = 0
    while not q.empty():
        results+=q.get()

    print(f"Sum of factorials is {results}")



if __name__ == "__main__":
    # Set the start method to 'spawn'
    set_start_method('spawn')

    numbers = list(map(int, input().split()))
    sum_of_factorials(numbers)
