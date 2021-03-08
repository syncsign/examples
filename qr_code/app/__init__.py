import uasyncio as asyncio
import ujson as json
import core.constants as c
from core.pan_parameters import QOS1

class App:
    # User App, send a QR Code to wireless display

    def __init__(self, mgr):
        self.targetNodeId = None
        self.pan = mgr.pan
        # run a asyncio task
        asyncio.create_task(self.oneShotTask())

        # setup an event handler
        mgr.setPanCallback(self.onPanEvent)

    async def oneShotTask(self):
        # This coro task() was brought up by __init__()
        # waiting for at least one display node becomes online
        while self.targetNodeId is None:
            await asyncio.sleep(1)
        await self.showQRCode()

    def onPanEvent(self, event, data):
        # Event listener, handling NODE.PRESENCE and remember the nodeId
        if event == c.EVT_NODE_PRESENCE:
            if data['isOnline']:
                self.targetNodeId = data['nodeId']
                print('node:', self.targetNodeId, 'online.')

    async def showQRCode(self):
        # Create layout render template and send to display
        try:
            layout = '''
            {
                "background": {
                    "bgColor": "WHITE"
                },
                "items": [
                    { "type": "TEXT",
                      "data": {
                        "text": "Scan Me!",
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
            return self.pan.putRefreshQueue(self.targetNodeId, json.loads(layout), qos=QOS1)
        except Exception as e:
            print('unable to process:', str(e))
        return False
