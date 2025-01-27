print("start")

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp

from utime import sleep

mqtt_server = '10.100.102.82'
mqtt_user = 'mqtt'
mqtt_pass = 'luka6484'

client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = "test/abc"
topic_sub = "test/123"
def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_broker(client_id, mqtt_server, mqtt_user, mqtt_pass):
  client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
  client.set_callback(sub_cb)
  client.connect()
  print('Connected to %s MQTT broker')
  return client

client = connect_broker(client_id, mqtt_server, mqtt_user, mqtt_pass)
client.subscribe(topic_sub)
for ii in range(200):
    try:
        msg = f"messeagenumber {ii}"
        client.check_msg()
        client.publish(topic_pub, msg)
    except:
        pass
    print(ii)
    sleep(1)