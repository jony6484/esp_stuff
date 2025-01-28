import uasyncio as asyncio
from sensor_mqtt_conf import conf_payload, sensor
import socket

async def handle_client(reader, writer):
    try:
        request = await reader.read(1024)
        request = request.decode('utf-8')
        print("Request:", request)

        # Parse the request
        method, path, _ = request.split(' ', 2)

        # Handle LED_ON request
        if method == 'GET' and path == '/TOPIC_ON':
            mqclient.publish(topic_conf, conf_payload)
            response = """\
HTTP/1.1 200 OK
Content-Type: text/plain

TOPIC is ON
"""
            await writer.awrite(response)

        # Handle LED_OFF request
        elif method == 'GET' and path == '/TOPIC_OFF':
            mqclient.publish(topic_conf, "")
            response = """\
HTTP/1.1 200 OK
Content-Type: text/plain

LED is OFF
"""
            await writer.awrite(response)

        # Handle unknown endpoints
        else:
            response = """\
HTTP/1.1 404 Not Found
Content-Type: text/plain

Endpoint not found
"""
            await writer.awrite(response)
    except Exception as e:
        print("Error handling client:", e)
    finally:
        await writer.aclose()

# Start the server
async def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
    print("Starting server on", addr)
    server = await asyncio.start_server(handle_client, "0.0.0.0", 8080)
    await server.wait_closed()

async def main_task():
    while True:
        try:
           distance = sensor.distance_cm()
           msg = f"distance: {distance}"
           mqclient.publish(topic_pub, str(distance))
        except:
            pass
        print(f'Distance: {distance} cm')
        #sleep(1.0)
        await asyncio.sleep(1.0)

# Run the event loop
async def main():
    # Run server and other tasks concurrently
    await asyncio.gather(start_server(), main_task())

# Start the program
asyncio.run(main())

# 
# import time


# import machine
# import micropython
# import network

# 
# from utime import sleep


