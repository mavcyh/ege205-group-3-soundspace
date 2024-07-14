import datetime
from datetime import timedelta
import sched
import threading
import time
from Adafruit_BBIO.SPI import SPI
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import board
import busio
import digitalio
import adafruit_ssd1306
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont
import socketio

SERVER_IP_ADDRESS = "192.168.1.20"

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
        pass
    Draw.text((oled_x_offset(instrument_name), 20), " " + instrument_name, font=Font, fill=1)
    Display.image(ImageObj)
    Display.show()

# S3: Tamper initialisation (Instrument inside/ outside detection)
TAMPER_PIN = "P8_18"
GPIO.setup(TAMPER_PIN, GPIO.IN)

# S4: Reed initialisation (Door opened/ closed detection)
REED_PIN = "P8_10"
GPIO.setup(REED_PIN, GPIO.IN)


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
def door_closed_change(door_closed):
    pass

def instrument_in_change(instrument_in):
    if instrument_in:
        barGraph_colour_control("GREEN")
    else:
        barGraph_colour_control("YELLOW")


# SOCKETIO EVENTS

@sio.event
def serverToInstrumentLocker_connected(data):
    if database["INSTRUMENT_LOCKER_NUMBER"] in data:
        database["locker_locked"] = data["locker_locked"]
        instrument_name = data[database["INSTRUMENT_LOCKER_NUMBER"]]["instrument_name"]
        database["instrument_name"] = instrument_name
        update_OLED("LOCKED" if database["locker_locked"] else "UNLOCKED", instrument_name)

@sio.event
def serverToInstrumentLocker_updateLockers(data):
    # Finds datetime of end of session (accurate for BBBW) using length of session in seconds
    database["session_end_datetime"] = datetime.datetime.now() + timedelta(seconds=data["session_duration"])


# MAIN LOGIC

door_closed = GPIO.input(REED_PIN)
instrument_in = GPIO.input(TAMPER_PIN)

while True:
    if door_closed != GPIO.input(REED_PIN):
        door_closed = not door_closed
        door_closed_change(door_closed)
    if instrument_in != GPIO.input(TAMPER_PIN):
        instrument_in = not instrument_in
        instrument_in_change(instrument_in)
    time.sleep(0.1)