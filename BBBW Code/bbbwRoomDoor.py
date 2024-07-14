import datetime
from datetime import timedelta
import threading
import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import board
import busio
import digitalio
import adafruit_ssd1306
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont
import socketio

SERVER_IP_ADDRESS = "192.168.X.X"

# Turn off USR LEDs
GPIO.setup("USR0", GPIO.OUT)
GPIO.setup("USR1", GPIO.OUT)
GPIO.setup("USR2", GPIO.OUT)
GPIO.setup("USR3", GPIO.OUT)
GPIO.output("USR0", GPIO.LOW)
GPIO.output("USR1", GPIO.LOW)
GPIO.output("USR2", GPIO.LOW)
GPIO.output("USR3", GPIO.LOW)

# S1: Buzz initialisation (User feedback and door alarm)
BUZZ_PIN = "P9_14"
BUZZ_VOLUME = 1

def buzz_control(repeat=0, active_time=0, period=0):
    if repeat < 0:
        PWM.stop(BUZZ_PIN)
        return
    PWM.start(BUZZ_PIN, BUZZ_VOLUME)
    PWM.set_frequency(BUZZ_PIN, 500)
    if repeat == 0:
        return
    elif repeat > 1:
        buzz_period_timer_threading = threading.Timer(period, buzz_control, [repeat-1, active_time, period])
        buzz_period_timer_threading.start()
    buzz_active_timer_threading = threading.Timer(active_time, PWM.stop, [BUZZ_PIN])
    buzz_active_timer_threading.start()

def alarm_timer():
    if database["door_broken_into"]:
        buzz_control(repeat=1, active_time=0.4)
        alarm_timer_threading = threading.Timer(0.5, alarm_timer)
        alarm_timer_threading.start()

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

def update_OLED(door_locking_timer_seconds=None, alarm_active=False):
    Draw.rectangle((0, 0, Display.width - 1, Display.height - 1), outline=0, fill=0)
    # Door locking timer
    if door_locking_timer_seconds != None:
        top_string = "Door Locking"
        bottom_string = f"in {door_locking_timer_seconds}"
    # Door is locked but not closed yet
    elif not database["door_closed"] and database["door_locked"] and not database["door_broken_into"]:
        top_string = "Door Open"
        bottom_string = "Lock Active"
    # Default mode, accepting keypad input
    else:
        if alarm_active:
            top_string = "Alarm Active"
        else:
            top_string = "Input Password"
        password_input_length = len(password_input)
        bottom_string = " " + (password_input_length * "* ") + ((6 - password_input_length) * "- ")
    
    Draw.text((oled_x_offset(top_string), 12), " " + top_string, font=Font, fill=1)
    Draw.text((oled_x_offset(bottom_string), 22), " " + bottom_string, font=Font, fill=1)
    Display.image(ImageObj)
    Display.show()

# S3: Analog Key initialisation
AKEY_PIN = "P9_40"
ADC.setup()

key_pressed = [False, False, False, False, False, False]

def check_key_press():
    analog_key_dvalue = ADC.read(AKEY_PIN)
    if analog_key_dvalue > 0.16 and analog_key_dvalue < 0.18: # T6
        if not True in key_pressed:
            key_pressed[0] = True
            keypad_input("1")
    else:
        key_pressed[0] = False
    if analog_key_dvalue > 0.33 and analog_key_dvalue < 0.35: # T5
        if not True in key_pressed:
            key_pressed[1] = True
            keypad_input("2")
    else:
        key_pressed[1] = False
    if analog_key_dvalue > 0.50 and analog_key_dvalue < 0.52: # T4
        if not True in key_pressed:
            key_pressed[2] = True
            keypad_input("3")
    else:
        key_pressed[2] = False
    if analog_key_dvalue > 0.67 and analog_key_dvalue < 0.69: # T3
        if not True in key_pressed:
            key_pressed[3] = True
            keypad_input("4")
    else:
        key_pressed[3] = False
    if analog_key_dvalue > 0.84 and analog_key_dvalue < 0.86: # T2
        if not True in key_pressed:
            key_pressed[4] = True
            keypad_input("C")
    else:
        key_pressed[4] = False
    if analog_key_dvalue > 0.90 and analog_key_dvalue < 1.10: # T1
        if not True in key_pressed:
            key_pressed[5] = True
            keypad_input("E")
    else:
        key_pressed[5] = False

# S4: Reed initialisation (Door opened/ closed detection)
REED_PIN = "P8_10"
GPIO.setup(REED_PIN, GPIO.IN)

def check_door_closed():
    door_closed_current = GPIO.input(REED_PIN)
    if database["door_closed"] == door_closed_current:
        return
    database["door_closed"] = door_closed_current
    # Door broken into
    if not door_closed_current and database["door_locked"] and not database["door_broken_into"]:
        database["door_broken_into"] = True
        alarm_timer()
        update_OLED(alarm_active=True)
    # Door closed normally
    elif door_closed_current and database["door_locked"] and not database["door_broken_into"]:
        update_OLED()

database = {
    "master_password": None,
    "temporary_password": None,
    "door_closed": None,
    "door_locked": False,
    "door_broken_into": False
}

sio = socketio.Client()
@sio.event
def connect():
    TxData = {
        "bbbw_role": "RoomDoor"
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

password_input = ""
def keypad_input(key_input):
    global password_input
    if not database["door_locked"]:
        return
    # Number input
    if key_input in ["1", "2", "3", "4"] and len(password_input) < 6:
        if not database["door_closed"] and not database["door_broken_into"]:
            return
        password_input += key_input
        update_OLED(alarm_active=database["door_broken_into"])
    
    # Clear key
    elif key_input == "C":
        password_input = ""
        update_OLED(alarm_active=database["door_broken_into"])
    
    # Enter key
    # Password accepted
    elif password_input == database["master_password"] \
    or password_input == database["temporary_password"]:
        # Deactivate alarm
        database["door_broken_into"] = False
        database["door_locked"] = False
        password_input = ""
        door_locking_timer()
    # Wrong password
    else:
        password_input = ""
        update_OLED(alarm_active=database["door_broken_into"])

# Locks door automatically
def door_locking_timer(seconds=5):
    if seconds > 0:
        update_OLED(door_locking_timer_seconds=seconds)
        door_locking_timer_threading = threading.Timer(1, door_locking_timer, [seconds - 1])
        door_locking_timer_threading.start()
    else:
        database["door_locked"] = True
        update_OLED()


# SOCKETIO EVENTS

@sio.event
def serverToRoomDoor_updatePasswords(data):
    database["master_password"] = data["master_password"]
    database["temporary_password"] = data["temporary_password"]


# MAIN LOGIC

door_locking_timer()

while True:
    check_door_closed()
    check_key_press()
    time.sleep(0.1)