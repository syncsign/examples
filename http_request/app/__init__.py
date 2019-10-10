# -*- coding: UTF-8 -*-

import logging
import uasyncio as asyncio
import arequests as requests
import ujson as json

log = logging.getLogger("APP")
log.setLevel(logging.DEBUG)

class App:
    def __init__(self, mgr, loop, pan):
        log.info('APP init')
        self.loop = loop
        self.loop.create_task(self.requestTask())

    async def getRequest(self, url, headers = {}):
        response = None
        resultStr = ''
        try:
            response = await requests.get(url, headers = headers)
            resultStr = await response.text
        except Exception as e:
            log.exception(e, 'request fail')
        if response:
            log.info("status code: %d", response.status_code)
            await response.close()
            log.info("GET result: %s", resultStr)

    async def postRequest(self, url, headers = {}, json = {}):
        response = None
        resultStr = None
        try:
            response = await requests.post(url, headers = headers, data = None, json = json)
            resultStr = await response.text
        except Exception as e:
            log.exception(e, 'request fail')
        if response:
            log.info("status code: %d", response.status_code)
            await response.close()
            log.info("POST result: %s", resultStr)

    async def putRequest(self, url, headers = {}, json = {}):
        response = None
        resultStr = None
        try:
            response = await requests.put(url, headers = headers, data = None, json = json)
            resultStr = await response.text
        except Exception as e:
            log.exception(e, 'request fail')
        if response:
            log.info("status code: %d", response.status_code)
            await response.close()
            log.info("PUT result: %s", resultStr)

    async def deleteRequest(self, url, headers = {}, json = {}):
        response = None
        resultStr = None
        try:
            response = await requests.delete(url, headers = headers, data = None, json = json)
            resultStr = await response.text
        except Exception as e:
            log.exception(e, 'request fail')
        if response:
            log.info("status code: %d", response.status_code)
            await response.close()
            log.info("DELETE result: %s", resultStr)

    async def patchRequest(self, url, headers = {}, json = {}):
        response = None
        resultStr = None
        try:
            response = await requests.patch(url, headers = headers, data = None, json = json)
            resultStr = await response.text
        except Exception as e:
            log.exception(e, 'request fail')
        if response:
            log.info("status code: %d", response.status_code)
            await response.close()
            log.info("PATCH result: %s", resultStr)

    def base64Encode(self, _json = {}):
        import base64
        base64Str = base64.b64encode(json.dumps(_json).encode()).decode()
        log.info("base64 result: %s", base64Str)
        return base64Str

    def urlEncode(self, url, params = {}):
        import urllib.parse
        url = url + urllib.parse.urlencode(params)
        log.info("url encode: %s", url)
        return url

    async def requestTask(self):
        await asyncio.sleep(5)
        _header = { "KEY" : "VALUE" }
        _data = { "id": 5, "HELLO" : "WORLD" }

        # methods example
        await self.getRequest( "https://httpbin.org/get", headers = _header )
        await self.postRequest( "https://httpbin.org/post", json = _data)
        await self.putRequest( "https://httpbin.org/put", json = _data)
        await self.deleteRequest( "https://httpbin.org/delete", json = _data)
        await self.patchRequest( "https://httpbin.org/patch", json = _data)

        # base64 encoding example
        await self.getRequest( "https://httpbin.org//base64/{val}".format(val = self.base64Encode(_data)) )

        # redirect & url encoding example
        _redirect_to = { "url": "https://httpbin.org/uuid" }
        await self.getRequest( self.urlEncode("https://httpbin.org/redirect-to?", _redirect_to) )

        log.info('request completed')
