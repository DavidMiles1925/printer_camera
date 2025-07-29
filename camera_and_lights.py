import os
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
from datetime import datetime

from temp import read_temp
from config import SINGLE_RECORDING_TIME, LIGHT_PIN_1, LIGHT_PIN_2, DISABLE_CAMERA

pins = [
    LIGHT_PIN_1, LIGHT_PIN_2
]

light_is_on = False

if DISABLE_CAMERA == False:
    picam2 = Picamera2()

    PHOTO_DIR = "photos"
    os.makedirs(PHOTO_DIR, exist_ok=True)

    VIDEO_DIR = "recordings"
    os.makedirs(VIDEO_DIR, exist_ok=True)

def setup_pins():
    GPIO.setmode(GPIO.BCM)

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

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
    time.sleep(2)

def capture_video(filename="video", duration=10):
    h264_path = os.path.join(VIDEO_DIR, f"{filename}.h264")
    mp4_path = os.path.join(VIDEO_DIR, f"{filename}.mp4")

    print(f"Recording video: {h264_path} for {duration} seconds")

    config = picam2.create_video_configuration()
    picam2.configure(config)

    encoder = H264Encoder()
    output = FileOutput(h264_path)

    picam2.start_recording(encoder, output)
    time.sleep(duration)
    picam2.stop_recording()

    print("Converting to MP4...")
    conversion_command = f"ffmpeg -y -i {h264_path} -c copy {mp4_path}"
    os.system(conversion_command)

    os.remove(h264_path)

    print(f"Video saved to {mp4_path}\n")
    time.sleep(2)


def main():
    try: 
        global light_is_on

        setup_pins()

        while True:
            temps = read_temp()

            clear_screen()

            print(f"Current Temperature is {round(temps[1], 1)}°F ({round(temps[0], 1)}°C)\n")
            print("What would you like to do?\n")
            print(f"1. {'Take a photo' if DISABLE_CAMERA == False else 'Camera Disabled'}")
            print(f"2. {'Record a video' if DISABLE_CAMERA == False else 'Camera Disabled'} ({SINGLE_RECORDING_TIME if DISABLE_CAMERA == False else ''} {'seconds' if DISABLE_CAMERA == False else ''})")
            print("3. Toggle light (currently: {})".format("ON" if light_is_on else "OFF"))
            print("4. Exit\n")
            choice = input("Enter your choice (1/2/3/4): ").strip()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if choice == "1":
                if DISABLE_CAMERA:
                    print("Camera is currently disabled. Enable DISABLE_CAMERA in config.py")
                    time.sleep(3)
                else:
                    capture_photo(f"photo_{timestamp}.jpg")
            elif choice == "2":
                if DISABLE_CAMERA:
                    print("Camera is currently disabled. Enable DISABLE_CAMERA in config.py")
                    time.sleep(3)
                else:
                    capture_video(f"video_{timestamp}", duration=SINGLE_RECORDING_TIME)
            elif choice == "3":
                light_is_on = not light_is_on
                set_light(light_is_on)
                time.sleep(1)
            elif choice == "4":
                print("Exiting program.")
                GPIO.cleanup()
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.\n")
                time.sleep(2)

    except Exception as e:
        print ("A top-level exception occured.")
        GPIO.cleanup()
        print(e.with_traceback)

    except KeyboardInterrupt:
        print("Program was closed with Ctrl-C")
        GPIO.cleanup()


if __name__ == "__main__":
    main()
