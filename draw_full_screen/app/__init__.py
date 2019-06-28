import uasyncio as asyncio
import ujson as json
import core.pan_vfs
from core.constants import *

BITMAP_NAME = "test.bmp"
BITMAP_PATH = "app/" + BITMAP_NAME
TARGET_NODE_ID = 0x124b001bbbf89e # REPLACE ME WITH YOUR DISPLAY NODE ID

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
        # Waiting for at least one display node becomes online
        while self.targetNodeId is None:
            await asyncio.sleep(1)
        # Send bitmap to display
        # The first call spends quite a long time to download bitmap to the node in PAN.
        # If the bitmap's hash is the same as previous, saveBitmapDataToNode() will not
        # download again and return immediately
        await self.saveBitmapDataToNode(self.targetNodeId, BITMAP_PATH, BITMAP_NAME)
        # load the bitmap (on display node) to screen
        await self.showFullScreenBitmap(self.targetNodeId)

    def onPanEvent(self, event, data):
        # Event listener, handling NODE.PRESENCE and remember the nodeId
        if event == EVT_NODE_PRESENCE:
            if data['isOnline'] and data['nodeId'] == TARGET_NODE_ID:
                self.targetNodeId = data['nodeId']
                print('node:', self.targetNodeId, 'online.')

    async def saveBitmapDataToNode(self, target, filePath, fileName):
        with open(filePath,'rb') as f:
            import core.image_process as img
            bitmapData, msg = img.loadBMP(f.read())
            if (len(bitmapData)):
                return await self.vfs.save(target, fileName, bytes(bitmapData))
        return False

    async def showFullScreenBitmap(self, target):
        # Create layout render template and send to display
        try:
            layout = json.loads('''{
                "background": {
                    "bitmap": { "name": "" }
                }
            }''')
            layout['background']['bitmap']['name'] = BITMAP_NAME
            return await self.pan.updateDisplay(target, layout)
        except Exception as e:
            print('unable to process:', str(e))
        return False
