import time
import concurrent.futures
import multiprocessing


def cpu_bound(number):
    return sum(i * i for i in range(number))

#Definition for Serial Processing
def find_sums(numbers):
    for number in numbers:
        cpu_bound(number)

#Definitions for Multithreaded Processing
def find_sumsMT(numbers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(cpu_bound, numbers)

#Definition for Multiprocessing
def find_sumsMP(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)

if __name__ == "__main__":

    #Serial Processing
    print('\nStarting Serial Processing:')
    numbers = [5_000_000 + x for x in range(20)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")

    #Multithreaded Processing
    print('\nStarting Mulithreaded Processing:')
    numbers = [5_000_000 + x for x in range(20)]

    start_time = time.time()
    find_sumsMT(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")

    #Multiprocessing
    print('\nStarting Multiprocessing:')
    numbers = [5_000_000 + x for x in range(20)]

    start_time = time.time()
    find_sumsMP(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds\n")