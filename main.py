import asyncio
from utils.gmail.gmail import Gmail

async def task():
    for ind in range(10000):
        print(f'op: {ind}')
        await asyncio.sleep(1)

async def main():
    gmail = Gmail()
    tasks = [asyncio.create_task(gmail.initialise()), asyncio.create_task(task())]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
