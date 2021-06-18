import multiprocessing as multi
import hashlib


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

    # Set the process creation method to 'spawn'
    multi.set_start_method('spawn')

    # Create a shared message queue for the processes to produce/consume data
    outputQueue    = multi.Queue()

    primesProcess1   = multi.Process(target=primesFunction,  args=(outputQueue,2,2001))
    primesProcess2   = multi.Process(target=primesFunction,  args=(outputQueue,2002,4001))

    # Start the child processes
    primesProcess1.start()
    primesProcess2.start()

    # Wait for child processes to complete
    primesProcess1.join()
    primesProcess2.join()

    # Empty the queue by displaying the results from the child processes
    while not outputQueue.empty():
        print(outputQueue.get())

    # Show that main is terminating now that all subprocesses are complete
    print("\nParent Process Exiting\n")