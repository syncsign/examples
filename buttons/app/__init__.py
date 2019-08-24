from micropython import const
import logging
import uasyncio as asyncio
from core.constants import *

#  buttonMask:
#
#  -------------------------
#  |                       |
#  |                       |
#  |       SyncSign        |
#  |                       |
#  |                       |
#  -------------------------
#  |  1  |  2  |  4  |  8  |
#  -------------------------

BUTTON_MASK_1 = const(1)
BUTTON_MASK_2 = const(2)
BUTTON_MASK_3 = const(4)
BUTTON_MASK_4 = const(8)
BUTTON_STATUS_PRESSED = const(0)

WEBHOOK_KEY = 'dVcMCuct838W9ssxxxxxxxx' # replace these lines with your webhook key
EVENT = 'button'
IFTTT_TRIGGER_URL = "https://maker.ifttt.com/trigger/{event}/with/key/{webhook_key}"

class App:
    # User App of Hub SDK, trigger an http request to IFTTT when a button event occurs

    def __init__(self, mgr, loop, pan):
        self.log = logging.getLogger("APP")
        self.log.setLevel(logging.DEBUG)
        self.pan = pan
        self.loop = loop
        mgr.setPanCallback(self.onPanEvent);
        self.log.info('App Starting')

    def onPanEvent(self, event, data):
        if event == EVT_NODE_BUTTONS:
            self.onNodeButtonEvent(data['nodeId'], data['buttonMask'], data['status'])

    def onNodeButtonEvent(self, nodeId, buttonMask, status):
        """Event of button pressed
        When the button is pressed, this method will be called by system
        Args:
            nodeId: (int) indicates which node is changing its status
            buttonMask: (int) =1, first button; =2, second button; =4, third button; =8, fourth button;
            status: (int) =0, button pressed
        """
        if buttonMask == BUTTON_MASK_1 and status == BUTTON_STATUS_PRESSED:
            pass
        elif buttonMask == BUTTON_MASK_2 and status == BUTTON_STATUS_PRESSED:
            pass
        elif buttonMask == BUTTON_MASK_3 and status == BUTTON_STATUS_PRESSED:
            pass
        elif buttonMask == BUTTON_MASK_4 and status == BUTTON_STATUS_PRESSED:
            self.loop.create_task(self.triggerIfttt()) # run a asyncio task

    async def triggerIfttt(self):
        import ujson as json
        url = IFTTT_TRIGGER_URL.format(event = EVENT, webhook_key = WEBHOOK_KEY)
        postBody = { "name": "BTN_D", "status":"PRESSED" }
        self.log.info("triggerIfttt url: %s", url)
        self.log.info("triggerIfttt body: %s", json.dumps(postBody))
        await self.postRequest(url, json = postBody)

    async def postRequest(self, url, headers = {}, json = {}):
        import arequests as requests
        response = None
        resultStr = None
        try:
            response = await requests.post(url, headers = headers, data = None, json = json)
            resultStr = await response.text
        except Exception as e:
            self.log.exception(e, 'request fail')
        if response:
            self.log.info("status code: %d", response.status_code)
            await response.close()
            self.log.info("POST result: %s", resultStr)
