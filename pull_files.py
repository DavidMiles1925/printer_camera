# This file is only to be used from a windows machine that has been paired with a Pi via SSH Key

import os
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from time import sleep

from config import REMOTE_HOST, REMOTE_PATH_PHOTO, REMOTE_PATH_VIDEO, LOCAL_PATH, PI_USERNAME

def progress(filename, size, sent):
    percent = (sent / size) * 100 if size != 0 else 100
    print(f"\rTransferring {filename}: {percent:.1f}% ({sent}/{size} bytes)", end="")

def fetch_files():
    try:
        print(f"Connecting to {REMOTE_HOST}...")

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(REMOTE_HOST, username=PI_USERNAME)  # No password needed with SSH key

        with SCPClient(ssh.get_transport(), progress=progress) as scp:
            print(f"Fetching files...")
            scp.get(REMOTE_PATH_PHOTO, LOCAL_PATH, recursive=True)
            scp.get(REMOTE_PATH_VIDEO, LOCAL_PATH, recursive=True)

        ssh.close()
        print(f"Done! Files copied to {LOCAL_PATH}")
    except Exception as e:
        print(e)
        sleep(5)

if __name__ == "__main__":
    print("program started")
    sleep(1)
    fetch_files()
