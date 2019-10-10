import logging
import uasyncio as asyncio
import arequests as requests
import asyn
import ujson as json
from core.constants import *

log = logging.getLogger("APP")
log.setLevel(logging.DEBUG)

# Change to your own settings
OPENWEATHERMAP_APIKEY = 'REPLACE_THIS_WITH_YOUR_OWN_API_KEY'
CITY_NAME = 'Los Angeles'
COUNTRY_CODE = 'us'

# Options
REFRESH_INTERVAL = 60 * 60 # refresh every hour
LAYOUT_FILE = "app/layout_4in2.json"

class App:
    """App for periodic update of weather station

    - Request for latest weather over HTTP GET every hour
    - Analysis the weather condition
    - Generate a layout template and send to wireless display
    """

    def __init__(self, mgr, loop, pan):
        self.pan = pan
        self.loop = loop
        self.targetNodeId = None
        self.nodeOnlineEvent = asyn.Event()
        mgr.setPanCallback(self.onPanEvent)
        self.loop.create_task(self.loopTask()) # run a asyncio task
        log.info('App Starting')

    async def loopTask(self):
        """Main task of App Class
        This coro task() was brought up by __init__().
        """
        # waiting for at least one display node becomes online
        await self.nodeOnlineEvent # an example of how to use 'asyn' event
        self.targetNodeId = self.nodeOnlineEvent.value()
        self.nodeOnlineEvent.clear()

        # loop forever
        while True:
            log.debug('App Task Running')
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
        log.info('node "%s" is %s', hex(nodeId), 'online.' if isOnline else 'offline!')
        if isOnline:
            self.nodeOnlineEvent.set(nodeId)

    async def _fetchLastestWeather(self):
        """Lookup current weather info through a REST API request"""
        url = 'http://api.openweathermap.org/data/2.5/weather?q={cityName},{countryCode}&appid={apiKey}'.format(
                cityName = CITY_NAME, countryCode = COUNTRY_CODE, apiKey = OPENWEATHERMAP_APIKEY )
        log.debug(url)
        response = None
        try:
            response = await requests.get(url)
            res = await response.json()
            if not 'cod' in res:
                log.error(res)
            else:
                code = res['cod']
                if code == 200:
                    await self._parseWeather(res)
                else:
                    log.error('invalid response: {}'.format(code))
        except Exception as e:
            log.exception(e, 'unable to get weather')
            if response:
                log.debug(str(response._cached))
        finally:
            if response: # If the error is an OSError the socket has to be closed.
                await response.close()

    async def _parseWeather(self, response):
        """Extract weather details from response"""
        try:
            weather = response['weather']
            main = response['main']
            log.info('Weather: {} {}'.format(weather, main))
            await self._sendToDisplay(weather[0]['main'], main['temp'], main['humidity'])
        except Exception as e:
            log.exception(e, 'unable to parse weather')

    async def _sendToDisplay(self, mainCondition, temperatureKelvin, humidity):
        """Create layout render template and send to display"""
        if not self.pan:
            return False
        log.debug('send to display')
        try:
            with open(LAYOUT_FILE, 'r') as f:
                layout = json.loads(f.read())
                # Replace weather condition data in layout
                layout['items'][0]['data']['text'] = mainCondition
                # Replace temperature & humidity data in layout
                fahrenheit = int((temperatureKelvin * 9 / 5 - 459.67) * 10) / 10
                temp = '{0:.1f}'.format(fahrenheit) + u"\u00b0F    " + str(int(humidity)) + "%"
                # celsius = int((temperatureKelvin - 273.15) * 10) / 10
                # temp = '{0:.1f}'.format(celsius) + u"\u00b0C    " + str(int(humidity)) + "%"
                layout['items'][1]['data']['text'] = temp
                # FIXME: use correct weather icon, see: https://erikflowers.github.io/weather-icons/
                layout['items'][2]['data']['text'] = '\uf002'

                """Send to display"""
                '''
                # if you have more than one nodes, try lookup like this:
                nodes = self.pan.onlineNodes()
                if len(nodes):
                    self.targetNodeId = next(iter(nodes))
                '''
                return await self.pan.updateDisplay(self.targetNodeId, layout)
        except Exception as e:
            log.exception(e, 'unable to process layout')
        return False
