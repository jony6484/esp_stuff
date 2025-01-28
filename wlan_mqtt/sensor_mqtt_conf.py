import json
import esp
from hcsr04 import HCSR04

topic_pub = "homeassistant/device/esp8266_jon1"
topic_conf = "homeassistant/device/esp8266_jon1/config"

conf_payload = json.dumps({
    "device": {
        "name": "my esp8266",
        "identifiers": ["devId1"]
        },
    "origin":{
        "name": "eps8266",
        "sw": "0.0.1"
        },
    "components":{
        "distance-sensor1":{
            "platform": "sensor",
            "state_topic": topic_pub,
            "name": "distance sensor 1",
            "unique_id": "devId1_distance"
            }
        }
    }
)

sensor = HCSR04(12, 14, 10000)