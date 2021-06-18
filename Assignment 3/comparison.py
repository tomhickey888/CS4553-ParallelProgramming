import multiprocessing as multi
import hashlib
import time


# Function to determine if a number is prime
def is_prime(n):
    if n <=1:
        return False
    for i in range(2, n): 
        if n %  i == 0:
            return False
    return True

# Function for child process to check primes
def primesFunction(output,min,max):
    for n in range(min, max):
        if is_prime(n):
            output.put(n)


# Main Function
if __name__ == '__main__':

    # Show that main is beginning before other processes are spawned
    print("\nParent Process Started\n")

    # Process the primes serially and store in a list while timing
    print('Serial Processing Starting')
    start=time.time()
    serialPrimes = []
    for n in range(2,4001):
        if is_prime(n):
            serialPrimes.append(n)
    serialTime = time.time()-start

    # Set the process creation method to 'spawn'
    multi.set_start_method('spawn')

    # Create a shared message queue for the processes to produce/consume data
    outputQueue    = multi.Queue()

    primesProcess1   = multi.Process(target=primesFunction,  args=(outputQueue,2,2001))
    primesProcess2   = multi.Process(target=primesFunction,  args=(outputQueue,2002,4001))

    # Start the child processes and timer
    start=time.time()
    primesProcess1.start()
    primesProcess2.start()

    # Wait for child processes to complete and end timer
    primesProcess1.join()
    primesProcess2.join()
    multiTime = time.time()-start

    # Empty the queue by storing the multiprocessing primes data in its own list
    multiPrimes = []
    while not outputQueue.empty():
        multiPrimes.append(outputQueue.get())

    # Display the times and results from each form of processing
    print(f'Serial Processing Time: {serialTime}')
    print(f"Serial Processing Output: {serialPrimes}\n")
    print(f'Multiprocessing Time: {multiTime}')
    print(f'Multiprocessing Output: {multiPrimes}\n')

    # Data validation between each form of processing
    serialPrimes.sort()
    multiPrimes.sort()
    if serialPrimes == multiPrimes:
        print('Data validated between processing forms\n')
    else:
        print('Different processing forms produce invalid results\n')    
 
    # Show that main is terminating now that all subprocesses are complete
    print("\nParent Process Exiting\n")