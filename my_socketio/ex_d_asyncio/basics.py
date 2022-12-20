#!/usr/bin/env python3
# ref: https://realpython.com/async-io-python/
# countasync.py

''' This program runs on its own, showing how several async functions run concurrently.
 Note that for the function to "await" I had to use awaitable function, specifically the asyncio.sleep '''

import asyncio

ii = 0

async def mult(i):
    print(f'Within mult')
    await asyncio.sleep(5)
    return i*2

async def count_my():
    #global ii
    ii = 10
    print(f"One, ii: {ii}")
    await mult(ii)  # The mult function must be a coroutine also!!
    ii += 1
    #await asyncio.sleep(1)  # rather than time.sleep(1)
    print(f"Two, after mult,  ii: {ii}")

async def count():
    print("One")

    # Pause here and come back to count when the below function is ready
    await asyncio.sleep(1)

    print("Two")

async def main():
    await asyncio.gather(count_my(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
