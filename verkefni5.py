# Verkefni 5 HP
# Imports
from machine import Pin, unique_id, Pin, ADC, PWM
from binascii import hexlify
from time import sleep_ms
from umqtt.simple import MQTTClient
import json
import asyncio
import uasyncio as asyncio
from neopixel import NeoPixel
from dfplayer import DFPlayer # 17, 18 and 21

# ------------ Variables -------------



# ------------ Tengjast WIFI -------------
WIFI_SSID = "TskoliVESM"
WIFI_LYKILORD = "Fallegurhestur"

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_LYKILORD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    
do_connect()


# ---------------- MQTT ------------------
# MQTT Broker Configuration
BROKER = "10.201.48.109"
CLIENT_ID = "esp32_client"
TOPICS = [
            "test/topic",
            "test/topic1",
            "test/topic2",
            "test/topic3",
]

# ------------ MQTT Callback --------------
async def mqtt_callback(topic, message):
    try:
        # Decode the topic and message
        topic_str = topic.decode()
        message_str = message.decode()

        # Attempt to parse the message as JSON
        payload = json.loads(message_str)
        print(f"Received message on topic '{topic_str}': {payload}")

        # Handle specific topics
        if topic_str == "test/topic":
            print(f"Handling message for topic 1 with data: {payload}")
            
        elif topic_str == "test/topic1":
            print(f"Handling message for topic 2 with data: {payload}")
            
        else:
            print(f"Received message on unknown topic '{topic_str}': {payload}")

    except json.JSONDecodeError as e:
        print(f"Invalid JSON received on topic '{topic.decode()}': {message.decode()}")
        print(f"Error details: {e}")

    except Exception as e:
        print(f"Error processing message from topic '{topic.decode()}': {e}")

    
# ------------ MQTT Connection -------------

class AsyncMQTTClient:
    def __init__(self, client_id, broker):
        self.client = MQTTClient(client_id, broker)
        self.connected = False

    async def connect(self):
        try:
            self.client.connect()
            print("Connected to MQTT Broker:", BROKER)
            self.connected = True
        except Exception as e:
            print("Error connecting to broker:", e)

    async def subscribe_to_topics(self, topics):
        for topic in topics:
            self.client.subscribe(topic)
            print(f"Subscribed to: {topic}")

    async def listen(self):
        while self.connected:
            try:
                # Check for incoming messages in a non-blocking way
                self.client.check_msg()
            except Exception as e:
                print("Error checking message:", e)
            await asyncio.sleep(0.1)  # Prevent high CPU usage

# ------ Asyncio Functions ------

# Plays music
async def play_audio(folder=1, file=1):
    df = DFPlayer(2) # Find UART id  "2" 
    df.init()
    await df.wait_available()
    
    await df.volume(15)
    await df.play(folder, file)
    print("Playing:", folder, file)





# ------ MAIN -------

async def main():
    do_connect()  # Connect to WiFi

    mqtt_client = AsyncMQTTClient(CLIENT_ID, BROKER)
    await mqtt_client.connect()

    # Register callback and subscribe to topics
    mqtt_client.client.set_callback(lambda topic, msg: asyncio.create_task(mqtt_callback(topic, msg)))
    await mqtt_client.subscribe_to_topics(TOPICS)

    # Start listening
    await mqtt_client.listen()

# Run the main loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Disconnected from MQTT broker")
    
