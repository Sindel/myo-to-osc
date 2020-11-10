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
import os
import socket
from pythonosc import dispatcher
from pythonosc import osc_packet
from pythonosc import osc_server
import shlex



parser = argparse.ArgumentParser(description='Connects to a Myo, then sends EMG and IMU data as OSC messages to localhost:3000.')
parser.add_argument('-l', '--log', dest='logging', action="store_true", help='Save Myo data to a log file.')
parser.add_argument('-d', '--discover', dest='discover', action='store_true', help='Search for available Myos and print their names and MAC addresses.')
parser.add_argument('-a', '--address', nargs='+', default="f7:9a:4a:68:04:8c", dest='address', help='Myo MAC addresses to connect to, in format "XX:XX:XX:XX:XX:XX".')
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
#command_line = "python3 myo_to_osc_other_IP_1_test.py -i localhost -p 7110 -a f7:9a:4a:68:04:8c -m /dev/ttyACM0"
command_line1 = "python3 myo_to_osc_other_IP_1_test.py -i "+args.ipAddress + " -p "+args.port+" -a "+ str(args.address[0])+" -m "+"/dev/ttyACM0"
process_args1 = shlex.split(command_line1)
instance1 = subprocess.Popen(process_args1)

command_line2 = "python3 myo_to_osc_other_IP_1_test.py -i "+args.ipAddress + " -p "+args.port+" -a "+ str(args.address[1])+" -m "+"/dev/ttyACM0"
process_args2 = shlex.split(command_line2)
instance2 = subprocess.Popen(process_args2)

#pro = subprocess.Popen(command_line, shell=True)

"""
def handlerRun(*msg):
	print("run", msg[1])
	global pro
	pro = subprocess.Popen(command_line, shell=True)
	print("ran")

def handlerKill(*msg):
	print("kill", msg[1])	
	pro.terminate()
	print("killed")
"""

def handlerFunc(*msg):
	print("received message ", msg)
	mac_address = msg[1]
	if mac_address == args.address[0]:
		process = instance1
	if mac_address == args.address[1]:
		process = instance2
	
	if msg[2]==1:
		#global pro

		command_line_local = "python3 myo_to_osc_other_IP_1_test.py -i "+args.ipAddress + " -p "+args.port+" -a "+ str(mac_address)+" -m "+"/dev/ttyACM0"
		shlexed_args = shlex.split(command_line_local)
		print("ran "+str(mac_address))
		#pro = subprocess.Popen(shlexed_args)
		if mac_address == args.address[0]:
			global instance1
			instance1 = subprocess.Popen(shlexed_args)
		if mac_address == args.address[1]:
			global instance2
			instance2 = subprocess.Popen(shlexed_args)

	if msg[2]==0: 
		#pro.terminate()
		process.terminate()
		print("killed "+str(mac_address))





print("Now running...")
dispatcher = dispatcher.Dispatcher()
#dispatcher.map("/run", handlerRun)
#dispatcher.map("/kill", handlerKill)
dispatcher.map("/myo/activate", handlerFunc)
loop = asyncio.get_event_loop()
server = osc_server.AsyncIOOSCUDPServer(server_address, dispatcher, loop)
print("aboutToServe")
server.serve()
print("nowServing")

try:
	loop.run_forever()
except KeyboardInterrupt:
	pass
finally:
	loop.stop()
	print("\nDisconnected")


# TODO:
#   - move classification if then to myohw.py
#   - experiment connecting to multiple myos.
