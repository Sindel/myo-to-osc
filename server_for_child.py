"""Myo-to-OSC application.
Connects to a Myo, then sends EMG and IMU data as OSC messages to localhost:3000
"""
import datetime
import math
import logging
import argparse
import sys
import time
import subprocess
import pythonosc
import unittest
import asyncio
import socket
import os
from pythonosc import dispatcher
from pythonosc import osc_packet
from pythonosc import osc_server
import shlex



parser = argparse.ArgumentParser(description='Connects to a Myo, then sends EMG and IMU data as OSC messages to localhost:3000.')
parser.add_argument('-l', '--log', dest='logging', action="store_true", help='Save Myo data to a log file.')
parser.add_argument('-d', '--discover', dest='discover', action='store_true', help='Search for available Myos and print their names and MAC addresses.')
parser.add_argument('-a', '--address', nargs='+', dest='address', help='Myo MAC addresses to connect to, in format "XX:XX:XX:XX:XX:XX".')
parser.add_argument('-i', '--ip', dest='ipAddress', default='localhost', help='An IP address to connect to, in format "XXX.XXX.X.XXX".')
parser.add_argument('-p', '--port', dest='port', default=3000, help='The port to connect to, in format "XXXX".')

args = parser.parse_args()

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]
ip = str(get_ip_address())
port = 2000
server_address = tuple([ip, port])
os.chdir(os.path.dirname(os.path.realpath(__file__)))
command_line = "python3 childProc.py -i 192.168.1.138 -p 7110 -a f7:9a:4a:68:04:8c d9:16:12:8b:cd:aa"


def handlerRun(*msg):
	print("run", msg[1])
	global pro
	pro = subprocess.Popen(command_line, shell=True)
	print("ran")

def handlerKill(*msg):
	print("kill", msg[1])	
	pro.terminate()
	print("killed")

print("Now running...")
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/run", handlerRun)
dispatcher.map("/kill", handlerKill)
loop = asyncio.get_event_loop()
server = osc_server.AsyncIOOSCUDPServer(server_address, dispatcher, loop)
print("aboutToServe")
server.serve()
print("nowServing")

try:
	loop.run_forever()
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	pass
finally:
	loop.stop()
	print("\nDisconnected")


# TODO:
#   - move classification if then to myohw.py
#   - experiment connecting to multiple myos.
