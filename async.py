#  In Python, async is used to define asynchronous code, which allows you to perform tasks without blocking the
#  execution of your program — especially useful for I/O-bound tasks
#  like network requests, file operations, or waiting for user input.

import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World!")

# Run it
asyncio.run(say_hello())

#============================================================================================

import asyncio

async def task1():
    print("Task 1 starting...")
    await asyncio.sleep(3)   # non-blocking
    print("Task 1 done")

async def task2():
    print("Task 2 starting...")
    await asyncio.sleep(2)
    print("Task 2 done")

async def main():
    await asyncio.gather(task1(), task2())  # run together

asyncio.run(main())
