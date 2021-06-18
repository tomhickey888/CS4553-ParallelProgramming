import hashlib
import time
import concurrent.futures
import multiprocessing

min = 1
reps = 5_000
hashvalues = []

def encrypt(min, max):
    for x in range(int(min), int(max)):
        hashvalues.append(hashlib.sha256(str(x).encode()))


if __name__ == "__main__":

    #Serial Processing Encryption
    print()
    startTimeS = time.time()
    encrypt(min,reps)
    durationS = time.time() - startTimeS
    hashvaluesS = hashvalues
    print(f'Serial time to encode: {(durationS)}')
    print()

    #Multithreaded Processing Encryption
    print()
    startTimeMT = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(encrypt, str(min), str(reps))
    durationMT = time.time() - startTimeMT
    hashvaluesMT = hashvalues
    print(f'Multithreaded time to encode: {durationMT}')
    print()

    #Error Checking
    print(f'The output from each algorithm was the same: {hashvaluesS == hashvaluesMT}')





