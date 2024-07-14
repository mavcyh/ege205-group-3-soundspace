import datetime
from datetime import timedelta
import threading
import time
from Adafruit_BBIO.SPI import SPI
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

# S1: BarGraph initialisation (Volume level indicator)
GPIO.setup("P9_14", GPIO.OUT)
GPIO.setup("P9_12", GPIO.OUT)
GPIO.output("P9_14", GPIO.HIGH)
GPIO.output("P9_12", GPIO.HIGH)
BarGraphSPI = SPI(1,0)
BarGraphSPI.mode = 0

def barGraph_control(bar_count):
    if bar_count == 0:
        BarGraphSPI.writebytes([0x00, 0x00, 0x00])
    elif bar_count == 1:
        BarGraphSPI.writebytes([0x00, 0x00, 0x01])
    elif bar_count == 2:
        BarGraphSPI.writebytes([0x00, 0x00, 0x03])
    elif bar_count == 3:
        BarGraphSPI.writebytes([0x00, 0x00, 0x07])
    elif bar_count == 4:
        BarGraphSPI.writebytes([0x00, 0x00, 0x0F])
    elif bar_count == 5:
        BarGraphSPI.writebytes([0x00, 0x40, 0x1F])
    elif bar_count == 6:
        BarGraphSPI.writebytes([0x00, 0xC0, 0x3F])
    elif bar_count == 7:
        BarGraphSPI.writebytes([0x01, 0xC0, 0x7F])
    elif bar_count == 8:
        BarGraphSPI.writebytes([0x03, 0xC0, 0xFF])
    elif bar_count == 9:
        BarGraphSPI.writebytes([0x07, 0xC0, 0xFF])
    elif bar_count == 10:
        BarGraphSPI.writebytes([0x0F, 0xC0, 0xFF])
    
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

def update_OLED(seconds=0, status=None, end=False):
    Draw.rectangle((0, 0, Display.width - 1, Display.height - 1), outline=0, fill=0)
    if not end:
        time_left = f"{str(int(seconds/360)).zfill(2)}H {str(int(seconds/60)).zfill(2)}M {str(seconds%60).zfill(2)}S"
        Draw.text((oled_x_offset(status), 12), " " + status, font=Font, fill=1)
        Draw.text((oled_x_offset(time_left), 22), " " + time_left, font=Font, fill=1)
    else:
        Draw.text((53, 12), " See you", font=Font, fill=1)
        Draw.text((44, 20), " again soon!", font=Font, fill=1)
    Display.image(ImageObj)
    Display.show()

# S3: Buzz initialisation (Alarm for volume related penalties)
BUZZ_PIN = "P8_19"
buzz_volume = 0.3

def buzz_control(repeat=0, active_time=0, period=0):
    if repeat < 0:
        PWM.stop(BUZZ_PIN)
        return
    PWM.start(BUZZ_PIN, buzz_volume)
    PWM.set_frequency(BUZZ_PIN, 500)
    if repeat == 0:
        return
    elif repeat > 1:
        buzz_period_timer = threading.Timer(period, buzz_control, [repeat-1, active_time, period])
        buzz_period_timer.start()
    buzz_active_timer = threading.Timer(active_time, PWM.stop, [BUZZ_PIN])
    buzz_active_timer.start()


# S4: Mic initialisation (Detection of volume level)
MIC_PIN = "P9_39"
ADC.setup()

database = {
    "current_datetime_second": None,
    "volume_level_total": 0,
    "volume_level_count": 0,
    "last_average_volume_level": None,
    "maximum_volume_level": 10,
    "pack_up_duration": 30,
    "leave_duration": 30,
    "session_active": False,
    "session_end_datetime": None
}

sio = socketio.Client()
@sio.event
def connect():
    TxData = {
        "bbbw_role": "SessionInfo"
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

MIC_MINIMUM_VALUE = 0.009035409428179264
MIC_MAXIMUM_VALUE = 0.010989011265337467
def update_volume_level_total():
    if not database["session_active"]:
        return
    rerun_timer = threading.Timer(0.05, update_volume_level_total)
    rerun_timer.start()
    raw_mic_value = ADC.read(MIC_PIN)
    # The volume level is found using a 1-10 scale of where the digital value of the mic output is at from the min to max value.
    # The first part of the expression has a theoretical value of 0 to 1.
    volume_level = ((raw_mic_value - MIC_MINIMUM_VALUE) / (MIC_MAXIMUM_VALUE - MIC_MINIMUM_VALUE) * 10)
    if volume_level < 0:
        volume_level = 0
    print(f"RAW VALUE: {raw_mic_value}, VOLUME LEVEL: {volume_level: .2f}")
    database["volume_level_total"] += volume_level
    database["volume_level_count"] += 1

def update_average_volume_level():
    if not database["session_active"]:
        return
    rerun_timer = threading.Timer(0.5, update_average_volume_level)
    rerun_timer.start()
    if database["volume_level_count"] > 0:
        average_volume_level = int(database["volume_level_total"] / database["volume_level_count"])
        if average_volume_level < 0:
            average_volume_level = 0
        # Depending on the maximum volume level set (1-10)
        # the magnitude of the average volume level is multiplied
        # so that the maximum is always 10 on the bar graph.
        barGraph_control(int(average_volume_level * (10 / database["maximum_volume_level"])))
        database["volume_level_total"] = 0
        database["volume_level_count"] = 0
        database["last_average_volume_level"] = average_volume_level

def update_session_info():
    if datetime.datetime.now().second != database["current_datetime_second"]:
        database["current_datetime_second"] = datetime.datetime.now().second
        seconds_left = int((database["session_end_datetime"] - datetime.datetime.now()).total_seconds())
        
        # Time still left in session for playing
        if seconds_left > (database["pack_up_duration"] + database["leave_duration"]):
            update_OLED(seconds_left - (database["pack_up_duration"] + database["leave_duration"]), "Time Left")
        # Time for packing up
        elif seconds_left > database["leave_duration"]:
            update_OLED(seconds_left - database["leave_duration"], "Pack Up")
        # Time for leaving studio
        elif seconds_left > 0:
            update_OLED(seconds_left, "Leave within")
        # Session ended
        else:
            # Cancel all rerun_timers
            database["session_active"] = False
            update_OLED(end=True)
            barGraph_control(0)
            return
        # Update server with volume level data
        last_average_volume_level = database["last_average_volume_level"]
        if last_average_volume_level != None:
            sio.emit("bbbwSessionInfo_updateVolumeLevel", {"volume_level": last_average_volume_level})
    rerun_timer = threading.Timer(0.1, update_session_info)
    rerun_timer.start()


# SOCKETIO EVENTS

@sio.event
def serverToSessionInfo_connected(data):
    # If None, there is no session active as of time of connection. If not, there is a session active.
    session_duration_left = data["session_duration_left"]
    if session_duration_left != None:
        serverToSessionInfo_updateSession({"session_duration": session_duration_left})
    database["maximum_volume_level"] = data["maximum_volume_level"]
    
@sio.event
def serverToSessionInfo_updateSession(data):
    # Finds datetime of end of session (accurate for BBBW) using length of session in seconds
    database["session_end_datetime"] = datetime.datetime.now() + timedelta(seconds=data["session_duration"])
    if not database["session_active"]:
        database["session_active"] = True
        update_volume_level_total()
        update_average_volume_level()
        update_session_info()

@sio.event
def serverToSessionInfo_updateMaximumVolumeLevel(data):
    database["maximum_volume_level"] = data["maximum_volume_level"]

@sio.event
def serverToSessionInfo_maximumVolumeExceeded(data):
    print("Volume level exceeded maximum.")

# MAIN LOGIC

update_OLED(end=True)

while True:
    time.sleep(0.1)