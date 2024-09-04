from datetime import datetime
import RPi.GPIO as GPIO
import os
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from time import sleep
from logger import write_to_log

from config import TIME_BETWEEN_VIDEOS, FILENAME_PREFIX, DIRECTORY_NAME_PREFIX, SAVE_DIRECTORY_PATH, CAMERA_RECORDING_TIME, LIGHTING_ON

LIGHT_1_PIN = 6
LIGHT_2_PIN = 13

video_counter = 0
recordings_path_str = "none"

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(bitrate=1000000)

# Adds zeros to the video number in the filename.
#   - This was done to ensure videos stayed in chronological
#     order, even when displayed alphabetically.
def add_zeros_to_number(num, amt):
    num_str = str(num)

    num_zeros = amt - len(num_str)

    if num_zeros > 0:
        return '0' * num_zeros + num_str
    else:
        return num_str

def setup_pins():
    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(LIGHT_1_PIN, GPIO.OUT)
    GPIO.output(LIGHT_1_PIN, GPIO.LOW)

    GPIO.setup(LIGHT_2_PIN, GPIO.OUT)
    GPIO.output(LIGHT_2_PIN, GPIO.LOW)

def set_up_folder():
    global recordings_path_str
    folder_time = datetime.now().strftime("%m.%d.%Y")

    recordings_path_str = f"{SAVE_DIRECTORY_PATH}{DIRECTORY_NAME_PREFIX}{folder_time}"
    
    if os.path.isdir(recordings_path_str) ==  False:
        os.mkdir(recordings_path_str)

    os.chdir(recordings_path_str)

def run_camera():
    switch_lights(True)
    global video_counter

    timestamp = datetime.now().strftime("%H.%M.%S")

    video_counter_str = add_zeros_to_number(video_counter, 3)

    output = FILENAME_PREFIX + "_" + timestamp + ".h264"
    mp4_output = f"{video_counter_str}-{FILENAME_PREFIX}-[{timestamp}].mp4"

    print("Camera Running")

    picam2.start_recording(encoder, output)

    sleep(CAMERA_RECORDING_TIME)
    
    picam2.stop_recording()

    switch_lights(False)

    print(f"Recorded {output}\nConverting to MP4...")

    # Convert H264 to MP4
    conversion_command = f"ffmpeg -i {output} -c copy {mp4_output}"
    os.system(conversion_command)

    # Delete the original H264 file after conversion
    os.remove(output)

    video_counter = video_counter + 1

    print(f"Recorded {mp4_output}")
    write_to_log(f"Camera Off: Recorded {mp4_output}")

    

def switch_lights(light):
    if LIGHTING_ON == True:
        if light == True:
            GPIO.output(LIGHT_1_PIN, GPIO.HIGH)
            GPIO.output(LIGHT_2_PIN, GPIO.HIGH)

        if light == False:
            GPIO.output(LIGHT_1_PIN, GPIO.LOW)
            GPIO.output(LIGHT_2_PIN, GPIO.LOW)

if __name__ == "__main__":
    try:
        print("Program Started")
        write_to_log("Program Started")
        setup_pins()
        
        while True:
            write_to_log("Running Camera")
            set_up_folder()
            run_camera()
            sleep(TIME_BETWEEN_VIDEOS)

    except KeyboardInterrupt:
        print("Program terminated with ctrl+c")
        write_to_log("Program terminated with ctrl+c")
        GPIO.cleanup()

    except Exception as e:
        write_to_log(f"Error: {e}")
        print(f"Error: {e}")