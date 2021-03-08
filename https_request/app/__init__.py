# -*- coding: UTF-8 -*-

import logging
import uasyncio as asyncio
import arequests as requests
import ujson as json

log = logging.getLogger("APP")
log.setLevel(logging.DEBUG)

CERT_ROOT_CA = 'app/ca_httpbin.pem'

class App:
    def __init__(self, mgr):
        log.info('APP init')
        asyncio.create_task(self.requestTask())

    async def getRequest(self, url, headers = {}, verify = False):
        response = None
        resultStr = ''
        try:
            response = await requests.get(url, headers = headers, verify = verify)
            resultStr = await response.text
        except Exception as e:
            log.exception(e, 'request fail')
        if response:
            log.info("status code: %d", response.status_code)
            await response.close()
            log.info("GET result: %s", resultStr)

    async def requestTask(self):
        await asyncio.sleep(5)
        _header = { "KEY" : "VALUE" }

        # request without verifying example
        log.info("request without verifying")
        await self.getRequest( "https://httpbin.org/get", headers = _header, verify = False)

        # request with verifying example
        log.info("request with verifying")
        await self.getRequest( "https://httpbin.org/get", headers = _header, verify = CERT_ROOT_CA)

        log.info('request completed')
