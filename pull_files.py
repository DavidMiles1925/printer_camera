# This file is only to be used from a windows machine that has been paired with a Pi via SSH Key

from scp import SCPClient
from scp import SCPException
from time import sleep

try:
    from paramiko import SSHClient, AutoAddPolicy
    from paramiko.ssh_exception import AuthenticationException
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
            if REMOTE_PATH_PHOTO:
                scp.get(REMOTE_PATH_PHOTO, LOCAL_PATH, recursive=True)
            if REMOTE_PATH_VIDEO:
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
        print("If 'paramiko not installed' is displayed above, run this command:\n")
        print("pip install paramiko\n")
        print("Press any key...")
        input()


    except FileNotFoundError as e:
        print(e.__class__)
        print(e)
        print("\n\n")
        print("HOW TO SOLVE:")
        print("Configure WIN_USERNAME in the config.py file.\n")
        print("Press any key...")
        input()

    except TimeoutError as e:
        print(e.__class__)
        print(e)
        print("\n\n")
        print("HOW TO SOLVE:")
        print("Please check that the device is turned on.")
        print("Check REMOTE_HOST in the config.py file.\n")
        print("Press any key...")
        input()

    except SCPException as e:
        print(e.__class__)
        print(e)
        print("\n\n")
        print("HOW TO SOLVE:")
        print("If 'No such file or directory' is displayed above...")
        print("    Check that the file paths in config.py are correct.")
        print("    Check the file path exists.\n")
        print("Otherwise, retry running program. This error can be caused by a dropped connection.\n")
        print("Press any key...")
        input()

    except AuthenticationException as e:
        print(e.__class__)
        print(e)
        print("\n\n")
        print("HOW TO SOLVE:")
        print("Please configure PI_USERNAME in the config.py file.\n")
        print("Press any key...")
        input()

    except Exception as e:
        print(e.__class__)
        print(e)
        print("\n\n")
        print("Press any key...")
        input()
