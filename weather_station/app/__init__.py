import logging
import uasyncio as asyncio
import arequests as requests
import asyn
import json
from core.params import *

# Change to your own settings
OPENWEATHERMAP_APIKEY = 'REPLACE_THIS_WITH_YOUR_OWN_API_KEY'
CITY_NAME = 'Los Angeles'
COUNTRY_CODE = 'us'

# Options
REFRESH_INTERVAL = 60 * 60 # refresh every hour
LAYOUT_FILE = "/app/layout_4in2.json"

class App:
    """App for periodic update of weather station

    - Request for latest weather over HTTP GET every hour
    - Analysis the weather condition
    - Generate a layout template and send to wireless display
    """

    def __init__(self, mgr, loop, pan):
        self.log = logging.getLogger("APP")
        self.log.setLevel(logging.DEBUG)
        self.pan = pan
        self.loop = loop
        self.targetNodeId = None
        self.nodeOnlineEvent = asyn.Event()
        mgr.setPanCallback(self.onPanEvent);
        self.loop.create_task(self.task()) # run a asyncio task
        self.log.info('App Starting')

    async def task(self):
        """Main task of App Class
        This coro task() was brought up by __init__().
        """
        # waiting for at least one display node becomes online
        await self.nodeOnlineEvent
        self.targetNodeId = self.nodeOnlineEvent.value()
        self.nodeOnlineEvent.clear()

        # loop forever
        while True:
            self.log.debug('App Task Running')
            await self._fetchLastestWeather()
            await asyncio.sleep(REFRESH_INTERVAL) # sleep for a while

    def onPanEvent(self, event, data):
        if event == EVT_NODE_PRESENCE:
            self.onNodePresence(data['nodeId'], data['isOnline'])

    def onNodePresence(self, nodeId, isOnline):
        """Event of presence/absence
        Whenever a node becomes online or offline, this method will be called by system
        Args:
            nodeId: (int) indicates which node is changing its status
            isOnline: (bool) =True, a presence; =False: absence
        """
        self.log.info('node "%s" is %s', hex(nodeId), 'online.' if isOnline else 'offline!')
        if isOnline:
            self.nodeOnlineEvent.set(nodeId)

    async def _fetchLastestWeather(self):
        """Lookup current weather info through a REST API request"""
        url = 'http://api.openweathermap.org/data/2.5/weather?q={cityName},{countryCode}&appid={apiKey}'.format(
                cityName = CITY_NAME, countryCode = COUNTRY_CODE, apiKey = OPENWEATHERMAP_APIKEY )
        self.log.debug(url)
        response = None
        try:
            response = await requests.get(url)
            res = await response.json()
            if not 'cod' in res:
                self.log.error(res)
            else:
                code = res['cod']
                if code == 200:
                    await self._parseWeather(res)
                else:
                    self.log.error('invalid response: {}'.format(code))
        except Exception as e:
            self.log.exception(e, 'unable to get weather')
            if response:
                self.log.debug(str(response._cached))
        finally:
            if response: # If the error is an OSError the socket has to be closed.
                await response.close()

    async def _parseWeather(self, response):
        """Extract weather details from response"""
        try:
            weather = response['weather']
            main = response['main']
            self.log.info('Weather: {} {}'.format(weather, main))
            await self._sendToDisplay(weather[0]['main'], main['temp'], main['humidity'])
        except Exception as e:
            self.log.exception(e, 'unable to parse weather')

    async def _sendToDisplay(self, mainCondition, temperatureKelvin, humidity):
        """Create layout render template and send to display"""
        if not self.pan:
            return False
        self.log.debug('send to display')
        try:
            with open(LAYOUT_FILE, 'r') as f:
                layout = json.loads(f.read())

                import core.device_display as disp
                dp = disp.getSpec(disp.DISPLAY_4IN2_BW)
                fullWidth = dp['resolution']['width']
                from core.font_render import FontRender
                self.font = FontRender()

                # Replace weather condition data in layout
                width = self.font.getRenderedWidth(mainCondition, self.font.FONT_YKSZ_BOLD_44) # calculate width, in order to align center
                layout['items'][0]['data']['caption'] = mainCondition
                layout['items'][0]['data']['offset']['x'] = (fullWidth - width - 48 * 2) // 2
                # Replace temperature & humidity data in layout
                fahrenheit = int((temperatureKelvin * 9 / 5 - 459.67) * 10) / 10
                temp = str(fahrenheit) + "\'F  " + str(humidity) + "%"
                # celsius = int((temperatureKelvin - 273.15) * 10) / 10
                # temp = str(celsius) + "\'C    " + str(humidity) + "%"
                width = self.font.getRenderedWidth(temp, self.font.FONT_DIN_CON_32) # calculate width, in order to align center
                layout['items'][1]['data']['caption'] = temp
                layout['items'][1]['data']['offset']['x'] = (fullWidth - width - 48 * 2) // 2

                """Send to display"""
                '''
                # if you have more than one nodes, try lookup like this:
                nodes = self.pan.getNodeIDs()
                if len(nodes):
                    self.targetNodeId = nodes[0]
                '''
                return await self.pan.updateDisplay(self.targetNodeId, layout)
        except Exception as e:
            self.log.exception(e, 'unable to process layout')
        return False
