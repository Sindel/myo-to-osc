"""Myo-to-OSC application.
Connects to a Myo, then sends EMG and IMU data as OSC messages to localhost:3000
"""
import datetime
import math
import logging
import argparse
import sys
import time
import signal

def signal_term_handler(signal, frame):
    print( 'got SIGTERM')
    sys.exit()

signal.signal(signal.SIGTERM, signal_term_handler)

print("Now running...")
try:
    while True:
        time.sleep(2)
        print(1)
except KeyboardInterrupt:
    pass
finally:
    print("\nDisconnected")
    print("\nEsciti")

# TODO:
#   - move classification if then to myohw.py
#   - experiment connecting to multiple myos.
