#!/usr/bin/python3

#Noah Maceri
#6/27/2021

import PySimpleGUI as gui
import time
from datetime import datetime
import subprocess
import os

gui.theme('DarkGrey2')
#Create layout
layout = [
    [
        [gui.Text("Options",justification='center',size=(200,1))],
        [gui.Button("S-OP25",size=(200,1),key="op25")],
        [gui.Button("K-OP25",size=(200,1),key="kill_op25")],
        [gui.Button("S-GUI",size=(200,1),key="gui")],
        [gui.Button("K-GUI",size=(200,1),key="kill_gui")],
        [gui.Button("Close",size=(200,1),key="exit")],
        [gui.Text(" ")],
        [gui.Text("",size=(200,11), key="logger")]
    ]
]

# Create the window
window = gui.Window("OP25 GUI", layout,size=(200, 400))

# Create an event loop
string_buf = []
string_counter = 0
global op25_proc
global firefox_proc

while True:
    event, values = window.read()
    if event == "op25":
        if string_counter <= 5:
            string_buf.append(datetime.now().strftime("%H:%M:%S") + " | Staring OP25...\n")
        else:
            string_buf.pop(0)
            string_buf.append(datetime.now().strftime("%H:%M:%S") + " | Staring OP25...\n")
        string_counter += 1
        window["logger"].update('\n'.join(map(str, string_buf)))
        print("opening thread for op25")
        #CHANGE THIS TO BE YOUR OP25 INSTANCE
        op25_proc = subprocess.Popen("cd ~/op25/op25/gr-op25_repeater/apps/ && ./rx.py --args 'rtl' -N 'LNA:47' -S 2400000 -o 25000 -T trunk.tsv -U -x 2.0 2>stderr.2 -l http:0.0.0.0:8080", shell=True)

    if event == "kill_op25":
        if string_counter <= 5:
            string_buf.append(datetime.now().strftime("%H:%M:%S") + " | Killing OP25...\n")
        else:
            string_buf.pop(0)
            string_buf.append(datetime.now().strftime("%H:%M:%S") + " | Killing OP25...\n")
        string_counter += 1
        window["logger"].update('\n'.join(map(str, string_buf)))

        print("killing thread for op25")

        op25_proc.kill()
        os.system("kill " + str(op25_proc.pid + 1))


    if event == "gui":
        if string_counter <= 5:
            string_buf.append(datetime.now().strftime("%H:%M:%S") + " | Staring webgui...\n")
        else:
            string_buf.pop(0)
            string_buf.append(datetime.now().strftime("%H:%M:%S") + " | Staring webgui...\n")
        string_counter += 1
        window["logger"].update('\n'.join(map(str, string_buf)))

        firefox_proc = subprocess.Popen("firefox -height 400 -width 600 localhost:8080", shell=True)

    if event == "kill_gui":
            if string_counter <= 5:
                string_buf.append(datetime.now().strftime("%H:%M:%S") + " | Killing webgui...\n")
            else:
                string_buf.pop(0)
                string_buf.append(datetime.now().strftime("%H:%M:%S") + " | Killing webgui...\n")
            string_counter += 1
            window["logger"].update('\n'.join(map(str, string_buf)))

            firefox_proc.kill()
            os.system("kill " + str(firefox_proc.pid + 1))



    if event == gui.WIN_CLOSED or event == "exit":
        break

window.close()