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

# Function to perform encryption
def encrypt(x):
    return hashlib.sha256(str(x).encode())

# Function for child process to check primes
def primesFunction(output):
    primes = []
    for n in range(0, 2_500):
        if is_prime(n):
            primes.append(n)
    output.put(f"primesFunction says: {primes}\n")

# Function for child process to perform encryption
def encryptionFunction(output):
    hashvalues = []
    for n in range(0,100):
        hashvalues.append(encrypt(n))
    output.put(f"encryptionFunction says: {hashvalues}\n")


#Main Function
if __name__ == '__main__':

    # Show that main is beginning before other processes are spawned
    print("\nParent Process Started\n")

    # Set the process creation method to 'spawn'
    multi.set_start_method('spawn')

    # Create a shared message queue for the processes to produce/consume data
    outputQueue    = multi.Queue()

    primesProcess   = multi.Process(target=primesFunction,  args=(outputQueue,))
    encryptionProcess   = multi.Process(target=encryptionFunction,  args=(outputQueue,))

    # Start the child processes
    primesProcess.start()
    encryptionProcess.start()

    # Wait for child processes to complete
    primesProcess.join()
    encryptionProcess.join()

    # Empty the queue by displaying the results from the child processes
    while not outputQueue.empty():
        print(outputQueue.get())

    # Show that main is terminating now that all subprocesses are complete
    print("\nParent Process Exiting\n")