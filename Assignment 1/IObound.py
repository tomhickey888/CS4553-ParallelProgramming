import requests
import time
import concurrent.futures
import threading
import aiohttp
import asyncio
import multiprocessing

#Definitions for Serial Processing
def download_site(url, session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")

def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)

#Definitions for Multithreaded Processing
def get_sessionThreading():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def download_siteThreading(url):
    session = get_sessionThreading()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")

def download_all_sitesThreading(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_siteThreading, sites)

#Definitions for Asyncio Processing
async def download_siteAsync(session, url):
    async with session.get(url) as response:
        print("Read {0} from {1}".format(response.content_length, url))


async def download_all_sitesAsync(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_siteAsync(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

#Definitions for Multiprocessing
session = None

def set_global_sessionMulti():
    global session
    if not session:
        session = requests.Session()


def download_siteMulti(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")


def download_all_sitesMulti(sites):
    with multiprocessing.Pool(initializer=set_global_sessionMulti) as pool:
        pool.map(download_siteMulti, sites)

#Main Statement
if __name__ == "__main__":

    #Serial Processing
    print('\nStarting Serial Processing\n')
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"\nDownloaded {len(sites)} in {duration} seconds using Serial Processing\n")
    print()

    #Multithreaded Processing
    print('\nStarting Multithreaded Processing\n')
    thread_local = threading.local()
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sitesThreading(sites)
    duration = time.time() - start_time
    print(f"\nDownloaded {len(sites)} in {duration} seconds using Multithreaded Processing\n")

    #Asyncio Processing
    print('\nStarting Asyncio Processing\n')
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_sitesAsync(sites))
    duration = time.time() - start_time
    print(f"\nDownloaded {len(sites)} sites in {duration} seconds using Asyncio Processing\n")

    #Multiprocessing
    print('\nStarting Multiprocessing\n')
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sitesMulti(sites)
    duration = time.time() - start_time
    print(f"\nDownloaded {len(sites)} in {duration} seconds using Multiprocessing\n")
