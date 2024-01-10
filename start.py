import time
import json
import os
import csv
from device import Device
from datetime import datetime
import subprocess
from flask import Flask

DEVICE_SERIAL = None
FREQUENCY = 0.5
LOCAL_VH_SAVE_PATH = "./captured_data/view_hierarchy" 
LOCAL_SCREENSHOT_SAVE_PATH = "./captured_data/screenshot"
CSV_FILE_PATH = "./captured_data/captured_states.csv"

def get_available_devices():
    """
    Get a list of device serials connected via adb
    :return: list of str, each str is a device serial number
    """
    r = subprocess.check_output(["adb", "devices"])
    if not isinstance(r, str):
        r = r.decode()
    devices = []
    for line in r.splitlines():
        segs = line.strip().split()
        if len(segs) == 2 and segs[1] == "device":
            devices.append(segs[0])
    return devices

def append_to_csv(data_row, file_path):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_row)

def capture_view_hierarchy_loop(device):
    interval = 1.0 / FREQUENCY
    data_capture_allowed = False

    print("Monitoring started. Waiting for valid data...")

    while True:
        tag = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")[:-3]
        
        if not data_capture_allowed:
            view_hierarchy = device.get_views()
            if view_hierarchy is not None:
                data_capture_allowed = True
                break
            else:
                time.sleep(interval)
                continue
        
        if data_capture_allowed:
            print("Now capturing data...")
            break

    print("Finished capturing data preparation")                

# if __name__ == '__main__':
#     if DEVICE_SERIAL is None:
#         devices = get_available_devices()
#         if len(devices) == 0:
#             print("No device connected.")
#             exit(1)
#         DEVICE_SERIAL = devices[0]
#         print("Using device: %s" % DEVICE_SERIAL)

#     device = Device(device_serial=DEVICE_SERIAL)
#     device.connect()
#     print("Device connected successfully.")

#     try:
#         capture_view_hierarchy_loop(device)
#     except KeyboardInterrupt:
#         print("Monitoring stopped.")
#         device.disconnect()
#     finally:
#         device.disconnect()

app = Flask(__name__)

device = None

def setup():
    global device
    DEVICE_SERIAL = None
    if DEVICE_SERIAL is None:
        devices = get_available_devices()
        if len(devices) == 0:
            print("No device connected.")
            exit(1)
        DEVICE_SERIAL = devices[0]
        print("Using device: %s" % DEVICE_SERIAL)

    device = Device(device_serial=DEVICE_SERIAL)
    device.connect()
    print("Device connected successfully.")

    try:
        capture_view_hierarchy_loop(device)
    except KeyboardInterrupt:
        print("Monitoring stopped.")
        device.disconnect()

@app.route('/get_view')
def get_view():
    global device
    return device.get_views()

if __name__ == '__main__':
    setup()
    app.run(debug=True)