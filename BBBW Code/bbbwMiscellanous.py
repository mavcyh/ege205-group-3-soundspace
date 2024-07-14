import sched
import threading
import time
import math
import Adafruit_BBIO.GPIO as GPIO
import board
import adafruit_bme680
import adafruit_lsm9ds1
import digitalio
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

i2c = board.I2C()

# S1: Environment initialisation
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, 0x77)

# S2: Motion initialisation (detection of motion in room)
MOTION_PIN = "P8_18"
GPIO.setup(MOTION_PIN, GPIO.IN)

# S3: 9DOF initialisation (detection of equipment drops)
lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c, 0x1C, 0x6A)
    

database = {
    "INSTRUMENT_LOCKER_NUMBER": 1,
    "locker_locked": True,
    "instrument_name": None,
    "session_end_datetime": None
}
sio = socketio.Client()
@sio.event
def connect():
    TxData = {
        "bbbw_role": "Miscellanous",
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

scheduler = sched.scheduler(time.time, time.sleep)

def update_room_state():
    scheduler.enter(1, 1, update_room_state)
    humidity_level = int(bme680.relative_humidity)
    TxData = {
        "humidity_level": humidity_level,
        "motion_detected": GPIO.input(MOTION_PIN)
    }
    sio.emit("bbbwMiscellanous_updateRoomState", TxData)
    
    
# SOCKETIO EVENTS

@sio.event
def serverToMiscellanous_connected(data):
    database["session_active"] = data["session_active"]


# MAIN LOGIC

update_room_state()
scheduler_thread = threading.Thread(target=scheduler.run)
scheduler_thread.start()

while True:
    device_dropped = False
    for i in range(5):
        x, y, z = lsm9ds1.acceleration
        ix = x
        iy = y
        iz = z
        time.sleep(0.15)
        x, y, z = lsm9ds1.acceleration
        accel_change = math.sqrt(((ix-x)**2 + (iy-y)**2 + (iz-z)**2))
        if accel_change > 10:
            device_dropped = True
        print(accel_change)
    if device_dropped:
        sio.emit("bbbwMiscellanous_deviceDropped")