import asyncio

queue = asyncio.Queue()

async def add_to_queue(job):
    await queue.put(job)

async def worker():
    while True:
        job = await queue.get()
        try:
            await job()
        except Exception as e:
            print("❌ Error en job:", e)
        queue.task_done()