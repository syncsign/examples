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
                "background": {
                    "bgColor": "WHITE",
                },
                "items": [
                    { "type": "TEXT",
                      "data": {
                        "caption": "Scan Me!",
                        "block": { "x": 144, "y": 200, "w": 144, "h": 56 }
                      }
                    },
                    { "type": "QRCODE",
                      "data": {
                        "text": "https://getvobot.com",
                        "position": { "x": 144, "y": 60 },
                        "scale": 4
                      }
                    }
                ]
            }
            '''
            return await self.pan.updateDisplay(self.targetNodeId, json.loads(layout))
        except Exception as e:
            print('unable to process:', str(e))
        return False
