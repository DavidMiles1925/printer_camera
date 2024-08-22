TIME_BETWEEN_VIDEOS = 5

LOG_DIRECTORY_PATH = "/home/pidgey/printer_camera/logs"

##############################
##############################
#####                    #####
#####    VIDEO SETUP     #####
#####                    #####
##############################
##############################


FILENAME_PREFIX = "print"

DIRECTORY_NAME_PREFIX = "print"

SAVE_DIRECTORY_PATH = "/home/pidgey/printer_camera/recordings/"

CAMERA_SLEEP_TIME = 6


    # Convert H264 to MP4
    #conversion_command = f"ffmpeg -i {output} -c copy {mp4_output}"
    #os.system(conversion_command)

    # Delete the original H264 file after conversion
    #os.remove(output)

    #https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf