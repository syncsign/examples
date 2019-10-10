# -*- coding: UTF-8 -*-

import uasyncio as asyncio
import ujson as json
from core.constants import *
import arequests as requests
import logging
from micropython import const

log = logging.getLogger("APP")
log.setLevel(logging.DEBUG)

# replace these lines with zigbee device you are going to control
TARGET_LIGHT_NODE_ID             = const(0x00124B0014C40F0F)
ZCL_CLUSTER_ID_GEN_LEVEL_CONTROL = const(0x0008)
ZCL_CLUSTER_ID_GEN_ON_OFF        = const(0x0006)
SRC_ENDPOINT                     = const(9)
DST_ENDPOINT                     = const(8)

class App:
    # User App of Hub SDK, send a 'Hello world' to wireless display
    def __init__(self, mgr, loop, pan):
        log.info('APP init')
        self.pan = pan
        mgr.setSetupPressedCallback(self.onSetupPressed)
        self.pan.setAppNodeJoinCallback(self.onNodeJoin)
        self.pan.setAppDataReceiveCallback(self.onDataReceive)
        self.loop = loop

    def onSetupPressed(self):
        log.info('setup button pressed')
        if self.pan:
            self.pan.permitDeviceJoin(60)

    def onNodeJoin(self, rawData, n):
        log.info('node joined/rejoined')
        log.debug("SrcAddr %s", hex(n.SrcAddr))
        log.debug("NwkAddr %s", hex(n.NwkAddr))
        log.debug("IEEEAddr %s", hex(n.IEEEAddr)) # nodeId
        log.debug("Capabilities %s", hex(n.Capabilities))

    def onDataReceive(self, rawData, n):
        log.info('data received')
        log.debug("GroupId# %s", n.GroupId)
        log.debug("ClusterId# %s", hex(n.ClusterId))
        log.debug("SrcAddr# %s", hex(n.SrcAddr))
        log.debug("SrcEndpoint# %d", n.SrcEndpoint)
        log.debug("DstEndpoint# %d", n.DstEndpoint)
        log.debug("WasBroadcast# %d", n.WasBroadcast)
        log.debug("LinkQuality# %d", n.LinkQuality)
        log.debug("SecurityUse# %d", n.SecurityUse)
        log.debug("TimeStamp# %d", n.TimeStamp)
        log.debug("TransSeqNum# %d", n.TransSeqNum)
        log.debug("Len# %d", n.Len)
        print("Data#", end = ' ')
        i = 0
        while i < n.Len:
            print('0x{0:0{1}X}'.format(n.Data[i],2), end = ' ')
            i+=1
        self.loop.create_task(self.taskDataReceived(n)) # run a asyncio task

    async def taskDataReceived(self, n):
        if n.ClusterId == 0x6 and n.SrcEndpoint == 1: # MIJIA button
            if n.Data[6] == 0:
                log.info("click down")
            elif n.Data[6] == 1:
                log.info("click released")
                await self.sendMessage()
            elif n.Data[6] == 2:
                log.info("double click")

    async def sendMessage(self, isLevelCtrl = False):
        if isLevelCtrl:
            clusterId = ZCL_CLUSTER_ID_GEN_LEVEL_CONTROL
            # 0x01:cluster specific command; 0x00:seq; 0x04:COMMAND_LEVEL_MOVE_TO_LEVEL_WITH_ON_OFF
            payload = [0x01, 0x00, 0x04, 0xAA, 0x30, 0x00]
        else: # Toggle the light
            clusterId = ZCL_CLUSTER_ID_GEN_ON_OFF
            # payload[2] 0x02: toggle, 0x00: off, 0x01: on
            payload = [0x01, 0x00, 0x02]

        print(payload)
        return self.pan.sendRawData(
            nodeId      = TARGET_LIGHT_NODE_ID,
            payload     = payload,
            nwkAddr     = None, # use nodeId
            clusterId   = clusterId,
            DstEndpoint = DST_ENDPOINT,
            SrcEndpoint = SRC_ENDPOINT
        )
