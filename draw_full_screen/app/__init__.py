import uasyncio as asyncio
import json
import core.pan_vfs
from core.constants import *

BITMAP_NAME = "bitmap.bin"
BITMAP_PATH = "/app/" + BITMAP_NAME

class App:
    # User App of Hub SDK, send a full screen image to wireless display

    def __init__(self, mgr, loop, pan):
        self.pan = pan
        loop.create_task(self.task()) # run a asyncio task
        self.targetNodeId = None
        mgr.setPanCallback(self.onPanEvent)
        self.vfs = core.pan_vfs.PanVFS()

    async def task(self):
        # This coro task() was brought up by __init__()
        # waiting for at least one display node becomes online
        while self.targetNodeId is None:
            await asyncio.sleep(1)
        await self.saveBitmapDataToNode(self.targetNodeId, BITMAP_PATH, BITMAP_NAME)
        await self.showFullScreenBitmap(self.targetNodeId)

    def onPanEvent(self, event, data):
        # Event listener, handling NODE.PRESENCE and remember the nodeId
        if event == EVT_NODE_PRESENCE:
            if data['isOnline'] and data['nodeId'] == 0x124b000435f708:
                self.targetNodeId = data['nodeId']
                print('node:', self.targetNodeId, 'online.')

    async def saveBitmapDataToNode(self, target, filePath, fileName):
        with open(filePath,'rb') as f:
            return await self.vfs.save(target, fileName, f.read())
        return False

    async def showFullScreenBitmap(self, target):
        # Create layout render template and send to display
        try:
            layout = json.loads('''{
                "background": {
                    "bitmap": { "name": "" }
                },
            }''')
            layout['background']['bitmap']['name'] = BITMAP_NAME
            return await self.pan.updateDisplay(target, layout)
        except Exception as e:
            print('unable to process:', str(e))
        return False
