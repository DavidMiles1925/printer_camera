# This device has 3 primary functions it can be used for:
#   -   Video Recording
#   -   Temperature Logging
#   -   Lighting the Chamber

TIME_BETWEEN_LOOP_ITERATIONS = 885 # Seconds between checks for feature activation (not including the length of the video recording)


##############################
##############################
#####                    #####
#####    VIDEO SETUP     #####
#####                    #####
##############################
##############################

VIDEO_RECORDING_ON = True

FILENAME_PREFIX = "Mars_5" # Do NOT include spaces in the name.

CAMERA_RECORDING_TIME = 15

DIRECTORY_NAME_PREFIX = FILENAME_PREFIX

SAVE_DIRECTORY_PATH = "/home/pidgey/printer_camera/recordings/"

LIGHTING_ON = True

LIGHT_ALWAYS_ON = True



    #https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf


##############################
##############################
#####                    #####
#####        Temp        #####
#####                    #####
##############################
##############################

TEMPERATURE_LOGGING_ON = True


##############################
##############################
#####                    #####
#####        LOGS        #####
#####                    #####
##############################
##############################

LOG_DIRECTORY_PATH = "/home/pidgey/printer_camera/logs"


##############################
##############################
#####                    #####
#####       CAMERA       #####
#####                    #####
##############################
##############################

SINGLE_RECORDING_TIME = 5
LIGHT_PIN_1 = 17
LIGHT_PIN_2 = 26
DISABLE_CAMERA = False


##############################
##############################
#####                    #####
#####     PULL FILES     #####
#####                    #####
##############################
##############################

REMOTE_HOST = "192.168.1.161"
USERNAME = "pidgey"
REMOTE_PATH_PHOTO = "/home/pidgey/printer_camera/photos/"
REMOTE_PATH_VIDEO = "/home/pidgey/printer_camera/recordings/"
LOCAL_PATH = "C:/Users/astro/Downloads"