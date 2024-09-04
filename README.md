# Printer Camera

## Project Description

This project was conceived because I have a resin 3D printer that I want to run outside. Because the printer is outside, I need to leave it blocked from sunlight. Therefore, I cannot check on the print by lifting the lid (at least not during the daytime).

I have added a temperature sensor (in developmment) to be able to monitor how hot the internals of the printer may be getting. See the notes below.

## Acceptance Criteria

Upon completion the unit will

- ✔ Turn on a camera on a set interval
- ✔ Turn on a camera with ad hoc command
- ✔ Turn on light(s) before recording with the camera
- ✔ Store videos on SSD to be accessed via SSH
- NEW: Record temperature in a log to be accessed via SSH

## Developer Notes

The majority of the code as repurposed from the motion_camera repository. Look there for more detailed documetnation.

### Temperature Sensor: DS18B20

`temp.py` to be tested independently before adding functionallity to `main.py`.

Datasheet is included in the repository.

#### Wiring

#### One-Wire Interface

This needs to be enabled to read the data pin. Do this in the RPi config.

**[Documentation](https://pinout.xyz/pinout/1_wire)** can be found here.

**[Tutorial](https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/)** can be found here.

1. Add to /boot/config.txt

```bash
sudo nano /boot/config.txt
```

`dtoverlay=w1-gpio`

2. Reboot

```bash
sudo reboot
```

3. We need to add a bootable kernal to Linux:

```bash
sudo modprobe w1-gpio
sudo modprobe w1-therm
```

4. Change directories and check for attached device:

```bash
cd /sys/bus/w1/devices
ls
```

5. Enter device directory:

```bash
cd 28-XXXXXXXXXXXX
```

6. Check raw temperature readout:

```bash
cat w1_slave
```

#### Code for Temp Sensor

The library `temp.py` was created using code from the tutorial referenced above.

The above steps will need to be completed before the code can be run.

### Pin assignments:

LED1: BCM 13
LED2: BCM 6

PiCamera must be properly connected or program will not run.

### Dependencies:

picamera2
ffmpeg
