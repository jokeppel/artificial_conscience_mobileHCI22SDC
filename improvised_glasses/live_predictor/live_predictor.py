"""Artificial Conscience Glasses
Script allows to predict data from the Glasses via USB port 

"""

## configuration

show_serial_ports= False # IMPORTANT: if true, the available ports are printed to the console

# port value from console needs to be set below (examples of how the port value may look in comment)
arduino_port = "COM4" # for windows, e.g., "COM1"; for mac/linux, e.g., "/dev/cu.usbmodem12345"
arduino_baudrate = 115200

delimiter = ';'

## end of configuration



## imports
import pickle
import os
from os import path

import sys
import csv
import glob
import threading
import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import ttk
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier

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
    "userName", "gestureName", 
    "accX", "accY", "accZ", 
    "gyroX", "gyroY", "gyroZ", 
    "time"]

model = None


## get folder for model (create if it does not exist yet)
recording_folder = path.join(path.curdir, 'model')
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

## method called to start connecting to the Glasses
def connect():
    set_state(f"Connecting to Port: {arduino_port}")
    connect_thread = threading.Thread(target=connect_wand_thread, daemon=True)
    connect_thread.start()

## method that starts the connection to the Glasses (called as a thread)
def connect_wand_thread():
    global isRecording, isConnected, csv_lines, model
    wand_device  = serial.Serial(port=arduino_port, baudrate=arduino_baudrate, timeout=.1)
    wand_device.flushInput()
    isConnected = False
    tries = 0
    while not isConnected and tries <= 30:
        line = str(wand_device.readline())
        if line.find('Glasses setup done') != -1:
            isConnected = True
        tries = tries + 1
    if isConnected:
        button_connect['state'] = "disabled"
        set_state(f"Connected to Port: {arduino_port}")
        print(delimiter.join(features))
        startTime = 0
        while isConnected:
            telemetry_line = str(wand_device.readline())
            if isRecording:
                if model is not None:
                    # gather data
                    if telemetry_line.find(',') != -1:
                        telemetry_data = telemetry_line.split(',')
                        if len(telemetry_data) > 9:
                            time = int(remove_escape_sequence(telemetry_data[9]))
                            if len(csv_lines) <= 0:
                                startTime = time
                            row = [len(csv_lines), entry_user.get(), entry_gesture.get(), float(telemetry_data[1]), float(telemetry_data[2]), float(telemetry_data[3]), float(telemetry_data[5]), float(telemetry_data[6]), float(telemetry_data[7]), time - startTime]
                            csv_lines.append(row)
                            #print(row)
                    if len(csv_lines) == 20:
                        #preprocess data
                        #pandas dataframe from csv_lines
                        df = pd.DataFrame(csv_lines, columns=features)
                        df.drop('time', inplace=True, axis=1)
                        df.drop('id', inplace=True, axis=1)
                        df.drop('userName', inplace=True, axis=1)
                        df.drop('gestureName', inplace=True, axis=1)

                        arr2d = df.to_numpy()
                        arr1d = arr2d.flatten()

                        #predict
                        prediction = model.predict(np.array([arr1d]))
                        print(prediction)
                        #clear csv_lines
                        csv_lines = []
    else:
        button_connect['state'] = "normal"
        set_state("Disconnected")

## method that processes a switch in recording status
def toggle_recording():
    global isRecording, isConnected, csv_lines, count, model
    if not isConnected:
        return

    if not isRecording:
        isRecording = True
        button_record['text'] = "Stop Recording"
        set_state(f"Recording from Port: {arduino_port}")
        if path.exists(recording_folder + "/" + "model.sav"):
            # load model
            model = pickle.load(open(recording_folder + "/" + "model.sav", 'rb'))
        else:
            # show no model available
            set_state("No model available")
            isRecording = False
            button_record['text'] = "Start Recording"
    else:
        isRecording = False
        button_record['text'] = "Record gesture"
        if not isConnected:
            button_connect['state'] = "normal"
            set_state(f"Disconnected")
        else:
            if len(csv_lines) > 0:
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
root.wm_title("Glasses | Recorder")
root.minsize(width=350, height=220)

# create status label
frame_status = tk.Frame()
label_status = tk.Label(master=frame_status, text="Status:", width=15)
label_status.pack(side=tk.LEFT, padx=10)
label_status_value = tk.Label(master=frame_status, text="Disconnected")
label_status_value.pack(side=tk.LEFT, padx=10)
frame_status.pack(padx=10, pady=10)

# create button to connect to Glasses
frame_connect = tk.Frame()
button_connect = tk.Button(master=frame_connect, text="Connect", command=connect)
button_connect.pack()
separator = ttk.Separator(master=frame_connect, orient='horizontal')
separator.pack(fill='x', ipady=15)
frame_connect.pack()

# create entry field for user name
frame_user = tk.Frame()
label_user = tk.Label(master=frame_user, text="Name of user:", width=15)
label_user.pack(side=tk.LEFT, padx=10)
entry_user = tk.Entry(master=frame_user)
entry_user.insert(0, "user #1")
entry_user.pack(side=tk.LEFT, padx=10)
frame_user.pack(padx=10, pady=5)

# create entry field for gesture name
frame_gesture = tk.Frame()
label_gesture = tk.Label(master=frame_gesture, text="Name of gesture:", width=15)
label_gesture.pack(side=tk.LEFT, padx=10)
entry_gesture = tk.Entry(master=frame_gesture)
entry_gesture.insert(0, "Drinking")
entry_gesture.pack(side=tk.LEFT, padx=10)
frame_gesture.pack(padx=10, pady=5)

# create button to start and stop recording
frame_record = tk.Frame()
button_record = tk.Button(master=frame_record, text="Record gesture", command=toggle_recording)
button_record.pack()
frame_record.pack(pady=10)

# GUI life loop
root.mainloop()