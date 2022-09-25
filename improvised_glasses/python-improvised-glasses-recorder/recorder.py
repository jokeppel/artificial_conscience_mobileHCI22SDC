"""
Script allows to record data from the Magic glasses via USB port 
"""

## configuration

show_serial_ports= False # IMPORTANT: if true, the available ports are printed to the console

# port value from console needs to be set below (examples of how the port value may look in comment)
arduino_port = "COM4" # for windows, e.g., "COM1"; for mac/linux, e.g., "/dev/cu.usbmodem12345"
arduino_baudrate = 115200

delimiter = ';'

## end of configuration



## imports
import os
from os import path

import sys
import csv
import glob
import threading
import numpy as np

import tkinter as tk
from tkinter import ttk

from datetime import datetime

# pip install pyserial (in case the following two imports fail)
import serial
import serial.tools.list_ports as ports 



## variables for status
isConnected = False
isRecording = False

## store collected Bluno data
csv_lines = []

## generate header for storage file (CSV)
features = [
    "id", 
    "userName", "activityName", 
    "accX", "accY", "accZ", 
    "gyroX", "gyroY", "gyroZ", 
    "time"]


## get folder for recordings (create if it does not exist yet)
recording_folder = path.join(path.curdir, 'recordings')
if not path.exists(recording_folder):
    os.mkdir(recording_folder)

## prints all available ports into the console (if settings is set to True)
if show_serial_ports:
    def serial_ports():
        """
        Function from Stackoverflow
        https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    print("Available ports are: ")
    print(serial_ports())

## method that sets the status label according to the current status
def set_state(state):
    label_status_value['text'] = f"{state}"

## method called to start connecting to the magic glasses
def connect():
    set_state(f"Connecting to Port: {arduino_port}")
    connect_thread = threading.Thread(target=connect_glasses_thread, daemon=True)
    connect_thread.start()

## method that starts the connection to the magic glasses (called as a thread)
def connect_glasses_thread():
    global isRecording, isConnected, csv_lines
    glasses_device  = serial.Serial(port=arduino_port, baudrate=arduino_baudrate, timeout=.1)
    glasses_device.flushInput()
    isConnected = False
    tries = 0
    while not isConnected and tries <= 30:
        line = str(glasses_device.readline())
        if line.find('Glasses setup done') != -1:
            isConnected = True
        tries = tries + 1
    if isConnected:
        button_connect['state'] = "disabled"
        set_state(f"Connected to Port: {arduino_port}")
        print(delimiter.join(features))
        startTime = 0
        while isConnected:
            telemetry_line = str(glasses_device.readline())
            if isRecording:
                if telemetry_line.find(',') != -1:
                    telemetry_data = telemetry_line.split(',')
                    if len(telemetry_data) > 9:
                        time = int(remove_escape_sequence(telemetry_data[9]))
                        if len(csv_lines) <= 0:
                            startTime = time
                        row = [len(csv_lines), entry_user.get(), entry_activity.get(), float(telemetry_data[1]), float(telemetry_data[2]), float(telemetry_data[3]), float(telemetry_data[5]), float(telemetry_data[6]), float(telemetry_data[7]), time - startTime]
                        csv_lines.append(row)
                        print(row)
    else:
        button_connect['state'] = "normal"
        set_state("Disconnected")

## method that processes a switch in recording status
def toggle_recording():
    global isRecording, isConnected, csv_lines, count
    if not isConnected:
        return

    if not isRecording:
        isRecording = True
        button_record['text'] = "Stop Recording"
        set_state(f"Recording from Port: {arduino_port}")
    else:
        isRecording = False
        button_record['text'] = "Record activity"
        if not isConnected:
            button_connect['state'] = "normal"
            set_state(f"Disconnected")
        else:
            if len(csv_lines) > 0:
                now = datetime.now()
                with open(path.join(recording_folder, f"recording-" + now.strftime("%Y%m%d-%H%M%S") + ".csv"), "w", newline='') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter=delimiter)
                    csv_writer.writerow(features)
                    csv_writer.writerows(csv_lines)
                csv_lines = []
            button_connect['state'] = "disabled"
            set_state(f"Connected to Port: {arduino_port}")

## method that cleans string of escape sequences at the end of a line
def remove_escape_sequence(val):
    str_val = str(val)
    str_val = str_val.replace("'", "")
    str_val = str_val.replace("\\n", "")
    str_val = str_val.replace("\\r", "")
    return str_val


## graphical user interface

# create window frame
root = tk.Tk()
root.wm_title("Activity | Recorder")
root.minsize(width=350, height=220)

# create status label
frame_status = tk.Frame()
label_status = tk.Label(master=frame_status, text="Status:", width=15)
label_status.pack(side=tk.LEFT, padx=10)
label_status_value = tk.Label(master=frame_status, text="Disconnected")
label_status_value.pack(side=tk.LEFT, padx=10)
frame_status.pack(padx=10, pady=10)

# create button to connect to magic glasses
frame_connect = tk.Frame()
button_connect = tk.Button(master=frame_connect, text="Connect", command=connect)
button_connect.pack()
separator = ttk.Separator(master=frame_connect, orient='horizontal')
separator.pack(fill='x', ipady=15)
frame_connect.pack()

# create entry field for user name
frame_user = tk.Frame()
label_user = tk.Label(master=frame_user, text="Name of User:", width=15)
label_user.pack(side=tk.LEFT, padx=10)
entry_user = tk.Entry(master=frame_user)
entry_user.insert(0, "User #1")
entry_user.pack(side=tk.LEFT, padx=10)
frame_user.pack(padx=10, pady=5)

# create entry field for activity name
frame_activity = tk.Frame()
label_activity = tk.Label(master=frame_activity, text="Name of activity:", width=15)
label_activity.pack(side=tk.LEFT, padx=10)
entry_activity = tk.Entry(master=frame_activity)
entry_activity.insert(0, "Drinking")
entry_activity.pack(side=tk.LEFT, padx=10)
frame_activity.pack(padx=10, pady=5)

# create button to start and stop recording
frame_record = tk.Frame()
button_record = tk.Button(master=frame_record, text="Record activity", command=toggle_recording)
button_record.pack()
frame_record.pack(pady=10)

# GUI life loop
root.mainloop()