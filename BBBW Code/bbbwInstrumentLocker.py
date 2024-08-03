import datetime
from datetime import timedelta
import sched
import threading
import time
from Adafruit_BBIO.SPI import SPI
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import adafruit_vcnl4010
import board
import busio
import digitalio
import adafruit_ssd1306
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont
import socketio

SERVER_IP_ADDRESS = "192.168.124.13"

# Turn off USR LEDs
GPIO.setup("USR0", GPIO.OUT)
GPIO.setup("USR1", GPIO.OUT)
GPIO.setup("USR2", GPIO.OUT)
GPIO.setup("USR3", GPIO.OUT)
GPIO.output("USR0", GPIO.LOW)
GPIO.output("USR1", GPIO.LOW)
GPIO.output("USR2", GPIO.LOW)
GPIO.output("USR3", GPIO.LOW)

# S1: BarGraph initialisation (Door status indicator)
GPIO.setup("P9_14", GPIO.OUT)
GPIO.setup("P9_12", GPIO.OUT)
GPIO.output("P9_14", GPIO.HIGH)
GPIO.output("P9_12", GPIO.HIGH)
BarGraphSPI = SPI(1,0)
BarGraphSPI.mode = 0

def barGraph_colour_control(colour):
    if colour == "GREEN":
        BarGraphSPI.writebytes([0x00, 0x03, 0xFF])
    elif colour == "YELLOW":
        BarGraphSPI.writebytes([0x0F, 0xFF, 0xFF])
    elif colour == "RED":
        BarGraphSPI.writebytes([0x0F, 0xFC, 0x00])

# S2: OLED initialisation (Screen)
Pin_DC = digitalio.DigitalInOut(board.P9_16)
Pin_DC.direction = digitalio.Direction.OUTPUT
Pin_DC.value = False
Pin_RESET = digitalio.DigitalInOut(board.P9_23)
Pin_RESET.direction = digitalio.Direction.OUTPUT
Pin_RESET.value = True
OledI2C = busio.I2C(SCL, SDA)
Display = adafruit_ssd1306.SSD1306_I2C(128, 32, OledI2C, addr=0x3C)
ImageObj = Image.new("1", (Display.width, Display.height))
Draw = ImageDraw.Draw(ImageObj)
Font = ImageFont.load_default()

def oled_x_offset(string):
    return 31 + int(3 * (15 - len(string)))

def update_OLED(status=None, instrument_name=None):
    Draw.rectangle((0, 0, Display.width - 1, Display.height - 1), outline=0, fill=0)
    if status:
        Draw.text((oled_x_offset(status), 12), " " + status, font=Font, fill=1)
    if instrument_name:
        Draw.text((oled_x_offset(instrument_name), 20), " " + instrument_name, font=Font, fill=1)
    Display.image(ImageObj)
    Display.show()

# S3: Reed initialisation (Door opened/ closed detection)
REED_PIN = "P8_10"
GPIO.setup(REED_PIN, GPIO.IN)

# S4: Tamper initialisation (Instrument inside/ outside detection)
i2c = board.I2C()
proxSensor = adafruit_vcnl4010.VCNL4010(i2c)


database = {
    "INSTRUMENT_LOCKER_NUMBER": "1",
    "locker_locked": True,
    "instrument_name": None,
    "session_end_datetime": None
}

sio = socketio.Client()
@sio.event
def connect():
    TxData = {
        "bbbw_role": "InstrumentLocker",
        "instrument_locker_number": database["INSTRUMENT_LOCKER_NUMBER"]
    }
    sio.emit("bbbw_connected", TxData)
    print("Connection with server established.")
@sio.event
def disconnect():
    print("Lost connection to server.")

# Attempt connection to server
while True:
    try:
        print("Attempting to establish connection...")
        sio.connect(f"http://{SERVER_IP_ADDRESS}:5000")
        break
    except:
        print("Retrying in", end="")
        for i in range(5, 0, -1):
            print(" " + str(i), end="", flush=True)
            time.sleep(0.25)
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.25)
        print("\n")


# FUNCTIONS
def door_closed_change():
    pass
    
def instrument_in_change():
    if not database["locker_locked"]:
        barGraph_colour_control("GREEN" if instrument_in else "YELLOW")
        
        TxData = {
            "locker_id": database["INSTRUMENT_LOCKER_NUMBER"],
            "usage": not instrument_in
        }
        sio.emit("bbbwInstrumentLocker_Usage", TxData)
    else:
        barGraph_colour_control("RED")


# SOCKETIO EVENTS

@sio.event
def serverToInstrumentLocker_connected(data):
    if database["INSTRUMENT_LOCKER_NUMBER"] in data:
        database["instrument_name"] = data[database["INSTRUMENT_LOCKER_NUMBER"]]
        update_OLED(status=None, instrument_name=database["instrument_name"])

@sio.event
def serverToInstrumentLocker_updateLockers(data):
    if database["INSTRUMENT_LOCKER_NUMBER"] in data["unlocked_locker_ids"]:
        database["locker_locked"] = False
        update_OLED(status="UNLOCKED", instrument_name=database["instrument_name"])
        barGraph_colour_control("GREEN" if instrument_in else "YELLOW")
    else:
        database["locker_locked"] = True
        update_OLED(status="LOCKED", instrument_name=database["instrument_name"])
        barGraph_colour_control("RED")
        
        
# MAIN LOGIC

door_closed = GPIO.input(REED_PIN)
proxThreshold = 10000
instrument_in = proxSensor.proximity > proxThreshold
door_closed_change()
instrument_in_change()

while True:
    proximity_value = proxSensor.proximity
    current_door_closed = GPIO.input(REED_PIN)
    print(proximity_value)
    if door_closed != current_door_closed:
        door_closed = current_door_closed
        door_closed_change()
    if instrument_in != (proximity_value > proxThreshold):
        instrument_in = proximity_value > proxThreshold
        print(f"proximity_value > proxThreshold {proximity_value > proxThreshold}")
        instrument_in_change()
    time.sleep(0.1)