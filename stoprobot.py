'''
Can plot EMG data in 2 different ways
change DRAW_LINES to try each.
Press Ctrl + C in the terminal to exit 
'''

import pygame
from pygame.locals import *
import multiprocessing
from keras.models import load_model
import numpy as np 

from pyomyo import Myo, emg_mode

import socket               # Import socket module
import time 

import urx
import logging
import time


# ------------ Myo Setup ---------------
q = multiprocessing.Queue()
model=load_model("D:/TFM_GV/Pruebas Myo/pesos/MLP_P30-87_LOOS_-0.2709_VAL_-0.90.h5")
def worker(q):
	m = Myo(mode=emg_mode.PREPROCESSED)
	m.connect()
	
	def add_to_queue(emg, movement):
		q.put(emg)

	m.add_emg_handler(add_to_queue)
	
	def print_battery(bat):
		print("Battery level:", bat)

	m.add_battery_handler(print_battery)

	 # Orange logo and bar LEDs
	m.set_leds([128, 0, 0], [128, 0, 0])
	# Vibrate to know we connected okay
	m.vibrate(1)
	
	"""worker function"""
	while True:
		m.run()
	print("Worker Stopped")

last_vals = None


# -------- Main Program Loop -----------
if __name__ == "__main__":
	p = multiprocessing.Process(target=worker, args=(q,))
	p.start()
	robot = urx.URRobot("169.254.12.28")
	logging.basicConfig(level=logging.INFO)
	s = socket.socket()         # Create a socket object
	host = '169.254.12.28' # Get local machine name
	port = 29999                # Reserve a port for your service.

	s.connect((host, port))
	print (s.recv(1024))
	w, h = 800, 600
	

	try:
		while True:
			
			while not(q.empty()):
				emg = list(q.get())
				
				lecture=emg
				data = lecture
				data = np.array(data)
				data = data.astype('float32')
				data = data/255
				predictions = model.predict(np.expand_dims(data,axis=0))
				predicted_classes = np.argmax(predictions, axis=1)
				print("The class is ",predicted_classes)						
				if predicted_classes==1:
					#robot.set_freedrive(True)
					data="play\n"
					s.send(data.encode())
					print (s.recv(1024))

				if predicted_classes==2:
					data="stop\n"
					s.send(data.encode())
					print (s.recv(1024))
					time.sleep(2)
					data="power off\n"
					s.send(data.encode())
					print (s.recv(1024))
					time.sleep(2)
				if predicted_classes==0:
					test=True
	except KeyboardInterrupt:
		print("Quitting")
		pygame.quit()
		s.close()                     # Close the socket when done
		robot.close()
		quit()
