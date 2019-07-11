# -*- coding: UTF-8 -*-

import logging
import uasyncio as asyncio
import arequests as requests
import ujson as json

class App:
    def __init__(self, mgr, loop, pan):
        self.log = logging.getLogger("APP")
        self.log.setLevel(logging.DEBUG)
        self.log.info('APP init')
        self.loop = loop
        self.base64Example()
        self.urlEncodeExample()
        self.loop.create_task(self.requestTask())

    async def getRequest(self, url, headers = {}):
        response = None
        resultStr = ''
        try:
            response = await requests.get(url, headers = headers)
            resultStr = await response.text
        except Exception as e:
            self.log.exception(e, 'request fail')
        if response:
            self.log.info("status code: %d", response.status_code)
            await response.close()
            self.log.info("GET result: %s", resultStr)

    async def postRequest(self, url, headers = {}, json = {}):
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

    async def putRequest(self, url, headers = {}, json = {}):
        response = None
        resultStr = None
        try:
            response = await requests.put(url, headers = headers, data = None, json = json)
            resultStr = await response.text
        except Exception as e:
            self.log.exception(e, 'request fail')
        if response:
            self.log.info("status code: %d", response.status_code)
            await response.close()
            self.log.info("PUT result: %s", resultStr)

    async def deleteRequest(self, url, headers = {}, json = {}):
        response = None
        resultStr = None
        try:
            response = await requests.delete(url, headers = headers, data = None, json = json)
            resultStr = await response.text
        except Exception as e:
            self.log.exception(e, 'request fail')
        if response:
            self.log.info("status code: %d", response.status_code)
            await response.close()
            self.log.info("DELETE result: %s", resultStr)

    async def patchRequest(self, url, headers = {}, json = {}):
        response = None
        resultStr = None
        try:
            response = await requests.patch(url, headers = headers, data = None, json = json)
            resultStr = await response.text
        except Exception as e:
            self.log.exception(e, 'request fail')
        if response:
            self.log.info("status code: %d", response.status_code)
            await response.close()
            self.log.info("PATCH result: %s", resultStr)

    def base64Example(self):
        import base64
        token = { "client": "xxx" }
        base64Str = base64.b64encode(json.dumps(token).encode()).decode()
        self.log.info("base64 result: %s", base64Str)

    def urlEncodeExample(self):
        import urllib.parse
        url = "https://httpbin.org/"
        params = { "id": 5, "type": "xxx" }
        url = url + urllib.parse.urlencode(params)
        self.log.info("url encode: %s", url)

    async def requestTask(self):
        await asyncio.sleep(5)
        _header = { "KEY" : "VALUE" }
        _data = { "HELLO" : "WORLD" }
        await self.getRequest( "https://httpbin.org/get", headers = _header )
        await self.postRequest( "https://httpbin.org/post", json = _data)
        await self.putRequest( "https://httpbin.org/put", json = _data)
        await self.deleteRequest( "https://httpbin.org/delete", json = _data)
        await self.patchRequest( "https://httpbin.org/patch", json = _data)
        self.log.info('request completed')
