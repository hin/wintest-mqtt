from aiowintest import WintestProtocol
import asyncio
import sys
import json
import datetime
import functools
import os

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

def serializer(v):
    if isinstance(v, datetime.datetime):
        return v.astimezone().isoformat()

async def print_message(message):
    print(json.dumps(message, default=serializer, indent=4, sort_keys=True))

async def on_summary(mqtt_client, msg):
    json_msg = json.dumps(msg, default=serializer)
    await mqtt_client.publish(os.environ('TOPIC_SUMMARY'),
        json_msg.encode('utf-8'), qos=QOS_2, retain=True)
    print('Published:', msg)

async def on_status(mqtt_client, msg):
    json_msg = json.dumps(msg, default=serializer)
    await mqtt_client.publish('%s/%s'%(os.environ('TOPIC_STATUS'), msg['station']),
        json_msg.encode('utf-8'), qos=QOS_2, retain=True)
    print('Published:', msg)

async def on_gab_out(mqtt_client, msg):
    json_msg = json.dumps(msg, default=serializer)
    await mqtt_client.publish('%s/out'%(os.environ['TOPIC_GAB']),
        json_msg.encode('utf-8'), qos=QOS_2, retain=True)
    print('Published:', msg)

def parse_address(str):
    v = str.split(':')
    return (v[0], int(v[1]))

async def main(argv):
    loop = asyncio.get_event_loop()

    # Connect to MQTT
    mqc = MQTTClient()
    await mqc.connect(os.environ['MQTT_URL'])
    print('connected to mqtt')

    local_addr = parse_address(os.environ['WINTEST_LOCAL_ADDRESS'])
    broadcast_addr = parse_address(os.environ['WINTEST_BROADCAST_ADDRESS'])
    wt = WintestProtocol(loop, local_addr, broadcast_addr)
    await wt.connect()
    wt.add_handler('summary', functools.partial(on_summary, mqc))
    wt.add_handler('gab', functools.partial(on_gab_out, mqc))
    wt.add_handler('status', functools.partial(on_status, mqc))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv))
    loop.run_forever()
    loop.close()
