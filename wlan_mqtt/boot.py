# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import os, machine
#os.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

from wlan_base import do_connect
wlan = do_connect("FuchsHome", "0544555561")
from umqttsimple import MQTTClient
from sensor_mqtt_conf import topic_pub, topic_conf
import ubinascii

mqtt_server = '10.100.102.82'
mqtt_user = 'mqtt'
mqtt_pass = 'luka6484'

client_id = ubinascii.hexlify(machine.unique_id())

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
  
mqclient = connect_broker(client_id, mqtt_server, mqtt_user, mqtt_pass)
# client.subscribe(topic_sub)