import uasyncio as asyncio
import json
from core.constants import *

class App:
    # User App of Hub SDK, send a 'Hello world' to wireless display

    def __init__(self, mgr, loop, pan):
        self.pan = pan
        loop.create_task(self.task()) # run a asyncio task
        self.targetNodeId = None
        mgr.setPanCallback(self.onPanEvent)

    async def task(self):
        # This coro task() was brought up by __init__()
        # waiting for at least one display node becomes online
        while self.targetNodeId is None:
            await asyncio.sleep(1)
        await self.printHello()

    def onPanEvent(self, event, data):
        # Event listener, handling NODE.PRESENCE and remember the nodeId
        if event == EVT_NODE_PRESENCE:
            if data['isOnline']:
                self.targetNodeId = data['nodeId']
                print('node:', self.targetNodeId, 'online.')

    async def printHello(self):
        # Create layout render template and send to display
        try:
            layout = '''
            {
                "items": [
                    { "type": "TEXT",
                      "data": {
                        "caption": "HELLO WORLD",
                        "block": { "x": 120, "y": 110, "w": 200, "h": 56 }
                      }
                    }
                ]
            }
            '''
            return await self.pan.updateDisplay(self.targetNodeId, json.loads(layout))
        except Exception as e:
            print('unable to process:', str(e))
        return False
