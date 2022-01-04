import paho.mqtt.client as mqtt
import board
import neopixel
import time
import json

MQTT_SERVER = "192.168.178.51"
MQTT_PATH = "tele/Pi101/STATE"
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
rgb = [0,0,0,0,0,0,0,0,0,0,0,0,] # 0-2 Farbe1,3-5 Farbe2, 6-8 Farbe3, 9-11 Farbe4
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    pixels.fill((0,0,0))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, message):
    decoded_message=str(message.payload.decode("utf-8"))
    msg=json.loads(decoded_message)
    anzahlZonen = msg['Zonen']
    if anzahlZonen == "1":
        print("1 Zone")
#        print("Rot: " + str(rgb[0]))
#        print("Gruen: " + str(rgb[1]))
#        print("Blau: " + str(rgb[2]))
        rgb_werte(msg['Farbe1'])
        pixels[0]= (rgb[0],rgb[1],rgb[2])
    if anzahlZonen == "2":
        print("2 Zonen")
        rgb_werte(msg['Farbe1'])
        pixels[0]= (rgb[0],rgb[1],rgb[2])
        rgb_werte(msg['Farbe2'])
        pixels[1]= (rgb[0],rgb[1],rgb[2])

    if anzahlZonen == "3":
        print("3 Zonen")
        rgb_werte(msg['Farbe1'])
        pixels[0]= (rgb[0],rgb[1],rgb[2])
        rgb_werte(msg['Farbe2'])
        pixels[1]= (rgb[0],rgb[1],rgb[2])
        rgb_werte(msg['Farbe3'])
        pixels[2]= (rgb[0],rgb[1],rgb[2])
    if anzahlZonen == "4":
        print("4 Zonen")
        rgb_werte(msg['Farbe1'])
        pixels[0]= (rgb[0],rgb[1],rgb[2])
        rgb_werte(msg['Farbe2'])
        pixels[1]= (rgb[0],rgb[1],rgb[2])
        rgb_werte(msg['Farbe3'])
        pixels[2]= (rgb[0],rgb[1],rgb[2])
        rgb_werte(msg['Farbe4'])
        pixels[3]= (rgb[0],rgb[1],rgb[2])

def rgb_werte(hex_farbe):
    prefix ="0x"
    rgb[0] = int(prefix + hex_farbe[0] + hex_farbe [1],0)
    rgb[1] = int(prefix + hex_farbe[2] + hex_farbe [3],0)
    rgb[2] = int(prefix + hex_farbe[4] + hex_farbe [5],0)
    return rgb
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.will_set("tele/Pi101/LWT", payload="Offline")
client.connect(MQTT_SERVER, 1883, 30)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.publish("tele/Pi101/LWT","Online")
client.loop_forever()
