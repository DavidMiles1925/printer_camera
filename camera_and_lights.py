import os
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
from datetime import datetime

from config import SINGLE_RECORDING_TIME, LIGHT_PIN_1, LIGHT_PIN_2

pins = [
    LIGHT_PIN_1, LIGHT_PIN_2
]

def setup_pins():
    GPIO.setmode(GPIO.BCM)

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

# Track light state
light_is_on = False


# Initialize camera
picam2 = Picamera2()

# Ensure the 'photos' directory exists
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

# Ensure the 'recordings' directory exists
VIDEO_DIR = "recordings"
os.makedirs(VIDEO_DIR, exist_ok=True)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def set_light(on: bool):
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)

    print("Lights turned", "ON" if on else "OFF")



def capture_photo(filename="photo.jpg"):
    filepath = os.path.join(PHOTO_DIR, filename)

    print(f"Capturing photo: {filepath}")
    picam2.start()

    time.sleep(2)  # Camera warm-up

    picam2.capture_file(filepath)
    picam2.stop()
    print("Photo saved.\n")

def capture_video(filename="video.h264", duration=10):
    filepath = os.path.join(VIDEO_DIR, filename)
    print(f"Recording video: {filepath} for {duration} seconds")

    config = picam2.create_video_configuration()
    picam2.configure(config)

    encoder = H264Encoder()
    output = FileOutput(filepath)

    picam2.start_recording(encoder, output)
    time.sleep(duration)
    picam2.stop_recording()
    print("Video saved.\n")


def main():
    global light_is_on  # so we can modify it inside the function

    setup_pins()

    while True:
        clear_screen()
        print("What would you like to do?")
        print("1. Take a photo")
        print("2. Record a video (10 seconds)")
        print("3. Toggle light (currently: {})".format("ON" if light_is_on else "OFF"))
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ").strip()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if choice == "1":
            capture_photo(f"photo_{timestamp}.jpg")
        elif choice == "2":
            capture_video(f"video_{timestamp}.h264", duration=SINGLE_RECORDING_TIME)
        elif choice == "3":
            light_is_on = not light_is_on
            set_light(light_is_on)
            time.sleep(1)
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.\n")
            time.sleep(2)


if __name__ == "__main__":
    main()
