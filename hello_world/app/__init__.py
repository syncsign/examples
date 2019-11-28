import uasyncio as asyncio
import ujson as json
from core.pan_parameters import *

TEMPLATE = '''
{
    "items": [
        { "type": "TEXT",
          "data": {
            "text": "HELLO WORLD",
            "block": { "x": 120, "y": 110, "w": 200, "h": 56 }
          }
        }
    ]
}
'''

class App:
    # User's App, send a 'Hello world' to wireless display

    def __init__(self, mgr, loop, pan):
        self.pan = pan
        loop.create_task(self.printHello()) # run a asyncio coro task

    async def printHello(self):
        # Wait for at least one display node becomes online
        while 0 == len(self.pan.onlineNodes()):
            await asyncio.sleep(1)
        # Create layout render template and send to display
        layout = json.loads(TEMPLATE)
        # Select the first online node as the target
        target = next(iter(self.pan.onlineNodes()))
        return self.pan.putRefreshQueue(target, layout, qos = QOS1)
