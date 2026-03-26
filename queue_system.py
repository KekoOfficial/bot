import asyncio

queue = asyncio.Queue()

async def add_to_queue(data):
    await queue.put(data)

async def worker():
    while True:
        job = await queue.get()
        try:
            await job()
        except Exception as e:
            print(f"Error: {e}")
        queue.task_done()