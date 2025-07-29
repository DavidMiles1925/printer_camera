import os
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
from datetime import datetime

from config import SINGLE_RECORDING_TIME

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
    while True:
        clear_screen()
        print("What would you like to do?")
        print("1. Take a photo")
        print("2. Record a video (10 seconds)")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if choice == "1":
            capture_photo(f"photo_{timestamp}.jpg")
        elif choice == "2":
            capture_video(f"video_{timestamp}.mp4", duration=SINGLE_RECORDING_TIME)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()
