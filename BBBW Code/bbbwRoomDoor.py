import threading
import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
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

# 3x4 matrix keypad initalisation
ROWS = ["P8_13", "P8_11", "P8_9", "P8_7"]
COLS = ["P8_12", "P8_10", "P8_8"]
KEYS = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]
key_pressed = [
    [False, False, False],
    [False, False, False],
    [False, False, False],
    [False, False, False]
]
for row in ROWS:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.HIGH)
for col in COLS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def check_key_press():
    for row_idx, row in enumerate(ROWS):
        GPIO.output(row, GPIO.LOW)
        for col_idx, col in enumerate(COLS):
            if GPIO.input(col) == GPIO.LOW:
                if not key_pressed[row_idx][col_idx]:
                    key_input = KEYS[row_idx][col_idx]
                    keypad_input(key_input)
                key_pressed[row_idx][col_idx] = True
            else:
                key_pressed[row_idx][col_idx] = False
        GPIO.output(row, GPIO.HIGH)

# Buzz initialisation (User feedback and door alarm)
BUZZ_PIN = "P9_16"
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

# OLED initialisation (Screen)
Pin_DC = digitalio.DigitalInOut(board.P9_14)
Pin_DC.direction = digitalio.Direction.OUTPUT
Pin_DC.value = False
Pin_RESET = digitalio.DigitalInOut(board.P9_12)
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

# Reed initialisation (Door opened/ closed detection)
REED_PIN = "P9_15"
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
        sio.emit("bbbwRoomDoor_DoorState", {"door_state": "BROKEN INTO"})
    # Door opened normally
    elif not door_closed_current and not database["door_locked"] and not database["door_broken_into"]:
        sio.emit("bbbwRoomDoor_DoorState", {"door_state": "OPENED"})
    # Door closed normally
    elif door_closed_current and database["door_locked"] and not database["door_broken_into"]:
        update_OLED()
        sio.emit("bbbwRoomDoor_DoorState", {"door_state": "CLOSED"})

database = {
    "master_password": "123456",
    "temporary_password": "",
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
    if key_input != "*" and key_input != "#":
        if len(password_input) >= 6:
            return
        if not database["door_closed"] and not database["door_broken_into"]:
            return
        password_input += key_input
        update_OLED(alarm_active=database["door_broken_into"])
    
    # Clear key
    elif key_input == "*":
        password_input = ""
        update_OLED(alarm_active=database["door_broken_into"])
    
    # Enter key
    # Password accepted
    elif password_input == database["master_password"] \
    or password_input == database["temporary_password"]:
        # Deactivate alarm
        door_locking_timer()
        database["door_broken_into"] = False
        database["door_locked"] = False
        password_input = ""
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
        if database["door_broken_into"] or database["door_closed"] != current_door_closed:
            database["door_closed"] = GPIO.input(REED_PIN)
            sio.emit("bbbwRoomDoor_DoorState", {"door_state": "CLOSED" if database["door_closed"] else "OPENED"})
        database["door_locked"] = True
        update_OLED()
        time.sleep(1)


# SOCKETIO EVENTS

@sio.event
def serverToRoomDoor_updateTemporaryPassword(data):
    database["temporary_password"] = data["temporary_password"]
    print("Temporary password updated.")

@sio.event
def serverToRoomDoor_updateMasterPassword(data):
    database["master_password"] = data["master_password"]
    print("Master password updated.")


# MAIN LOGIC

door_locking_timer()

while True:
    check_door_closed()
    check_key_press()
    time.sleep(0.1) 