import paho.mqtt.client as mqtt
import board
import neopixel
import time
import json


MQTT_SERVER = "192.168.178.50"
MQTT_PATH = "tele/Pi1"
# WZ Decke
# 0-145 hinten
# 146-295 rechts (Fenster)
# 296-441 vorne ( TV)
# 442-590 links (Flur)
#TV Wand (351 LEDs)
# 0-107 rechts TV
# 108-242
# 243-350
pixels = neopixel.NeoPixel(board.D18, 4)
encoding = 'utf-8'
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    prefix ="0x"
    color = prefix + str(msg.payload,encoding)
    red_hex = prefix + color[2] + color[3]
    green_hex = prefix + color[4] + color[5]
    blue_hex = prefix + color[6] + color[7]
    red=int(red_hex,0)
    green=int(green_hex,0)
    blue=int(blue_hex,0) 
    pixels.fill((red, green, blue))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.will_set(MQTT_PATH + "/LWT", payload="Offline")
client.connect(MQTT_SERVER, 1883, 10)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.publish(MQTT_PATH + "/LWT","Online")
client.loop_forever()
