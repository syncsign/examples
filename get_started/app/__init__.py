import uasyncio as asyncio

class App:
    def __init__(self, mgr):
        # User's App, print a 'hello world' to console every 10 seconds
        asyncio.create_task(self.loopTask('hello world'))

    async def loopTask(self, s):
        while True:
            print(s)
            await asyncio.sleep(10)
