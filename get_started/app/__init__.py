import uasyncio as asyncio

class App:
    def __init__(self, mgr, loop, pan):
        # User's App, print a 'hello world' to console every 10 seconds
        self._loop = loop
        self._loop.create_task(self.myLoop('hello world'))

    async def myLoop(self, s):
        while True:
            print(s)
            await asyncio.sleep(10)
