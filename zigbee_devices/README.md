# ZigBee Devices Example

The Hub works as a ZigBee coordinator, it creates a ZigBee network so that most Zigbee 3.0 devices can join it.

This is a simple example of zigbee devices communication. Currently, it supports:

- Press [ Setup ] button to enter the commissioning mode;
- Handle the MIJIA button's event and control a ZigBee light's ON/OFF.

## SETUP

- Run the example, then press [ Setup ] to enter commissioning mode
- Trigger a MIJIA button enter the 'pairing mode'
- Trigger a ZigBee light bulb enter the 'pairing mode'
- Check the console output and find the ZigBee light's Node ID (IEEE address), you will see:

```
I (54650) APP: node joined/rejoined
D (54791) APP: IEEEAddr 0x124b001bbbff66
```

- Replace the placeholder of TARGET_LIGHT_NODE_ID with your real light's IEEEAddr
- Run the example again
- Press the button to toggle the light's ON/OFF

## Note

- Philips Hue light bulb is not tested yet and may not work.
