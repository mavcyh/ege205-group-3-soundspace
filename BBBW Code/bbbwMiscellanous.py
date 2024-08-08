import sched
import threading
import time
import math
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import board
import adafruit_bme680
import adafruit_lsm9ds1
import digitalio
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

i2c = board.I2C()

# S1: Environment initialisation
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, 0x77)

# S2: Motion initialisation (detection of motion in room)
MOTION_PIN = "P9_15"
GPIO.setup(MOTION_PIN, GPIO.IN)

# S3: 9DOF initialisation (detection of equipment drops)
lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c, 0x1C, 0x6A)

# S3: Buzz initialisation (door break in alarm)
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

database = {
    "INSTRUMENT_LOCKER_NUMBER": 1,
    "locker_locked": True,
    "instrument_name": None,
    "session_end_datetime": None,
    "session_active": None
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

motion_detected = None
def update_room_state():
    global motion_detected
    scheduler.enter(1, 1, update_room_state)
    motion_detected = GPIO.input(MOTION_PIN)
    TxData = {
        "humidity_level": int(bme680.relative_humidity),
        "motion_detected": motion_detected
    }
    sio.emit("bbbwMiscellanous_updateRoomState", TxData)
    
    
# SOCKETIO EVENTS

@sio.event
def serverToMiscellanous_connected(data):
    database["session_active"] = data["session_active"]
    print("Session active." if database["session_active"] else "No session active.")


# MAIN LOGIC

update_room_state()
scheduler_thread = threading.Thread(target=scheduler.run)
scheduler_thread.start()

while True:
    if motion_detected:
        buzz_control(repeat = -1 if database["session_active"] else 0)
    else:
        buzz_control(repeat = -1)
        
    for i in range(5):
        x, y, z = lsm9ds1.acceleration
        ix = x
        iy = y
        iz = z
        time.sleep(0.15)
        x, y, z = lsm9ds1.acceleration
        accel_change = math.sqrt(((ix-x)**2 + (iy-y)**2 + (iz-z)**2))
        if accel_change > 10:
            sio.emit("bbbwMiscellanous_deviceDropped")
        # print(accel_change)