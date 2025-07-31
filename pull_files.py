# This file is only to be used from a windows machine that has been paired with a Pi via SSH Key

import os
from scp import SCPClient
from time import sleep

try:
    from paramiko import SSHClient, AutoAddPolicy
except:
    print("\nparmiko not installed\n")
    pass

from config import REMOTE_HOST, REMOTE_PATH_PHOTO, REMOTE_PATH_VIDEO, LOCAL_PATH, PI_USERNAME

def progress(filename, size, sent):
    percent = (sent / size) * 100 if size != 0 else 100
    print(f"\rTransferring {filename}: {percent:.1f}% ({sent}/{size} bytes)", end="")

def fetch_files():
    
        print(f"Connecting to {REMOTE_HOST}...")

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(REMOTE_HOST, username=PI_USERNAME)  # No password needed with SSH key

        with SCPClient(ssh.get_transport(), progress=progress) as scp:
            print(f"Fetching files...")
            scp.get(REMOTE_PATH_PHOTO, LOCAL_PATH, recursive=True)
            scp.get(REMOTE_PATH_VIDEO, LOCAL_PATH, recursive=True)

        ssh.close()
        print(f"\n\nDone! Files copied to {LOCAL_PATH}")
        sleep(2)


if __name__ == "__main__":
    print("program started")
    sleep(1)

    try:
        fetch_files()

    except NameError as e:
        print(e.__class__)
        print(e)
        print("\n\n")
        print("HOW TO SOLVE:")
        print("If 'paramiko not installed' is displayed above, run this command:\n\n")
        print("pip install paramiko\n\n")
        print("Press any key...")
        input()


    except FileNotFoundError as e:
        print(e.__class__)
        print(e)
        print("\n\n")
        print("HOW TO SOLVE:")
        print("Please configure WIN_USERNAME in the config.py file.")
        print("Press any key...")
        input()

    except TimeoutError as e:
        print(e.__class__)
        print(e)
        print("\n\n")
        print("HOW TO SOLVE:")
        print("Please check REMOTE_HOST in the config.py file.")
        print("Please check that the device is turned on.")
        print("Press any key...")
        input()

    except Exception as e:
        print(e)
        print(e.__class__)

        if str(e) == "Authentication failed.":
            print("\n\n")
            print("HOW TO SOLVE:")
            print("Please configure PI_USERNAME in the config.py file.")

        print("Press any key...")
        input()
