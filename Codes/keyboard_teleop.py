#!/usr/bin/env python
# license removed for brevity
import rospy
import serial
import struct
import math
import time

import pygame, time
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Pygame Keyboard Test')
pygame.mouse.set_visible(0)
pygame.key.set_repeat(1,1)
global run_program
run_program=True


def write_Int16(data,ser):
    ser.write(struct.pack('>B',(data>>8)&0xFF))
    ser.write(struct.pack('>B',data&0xFF))

def write_Byte(data,ser):
    ser.write(struct.pack('>B',(data)&0xFF))

def move_x_right():
	print('Moving X to Right')

def move_x_left():
	print('Moving X to Left')

def move_y_back():
	print('Moving Y  Back')

def move_y_front():
	print('Moving Y Front')

def move_z_up():
	print('Moving Z Up')

def move_z_down():
	print('Moving Z Down')

def move_u_up():
	print('Moving U Up')

def move_u_down():
	print('Moving U Down')

def move_v_right():
	print('Moving V to Right')

def move_v_left():
	print('Moving V to Left')

#Declaring global variables
global pulses
global dir_ena


def key_pressed_listener():

	#Initializing global varibales
	global pulses
	global dir_ena
	global run_program
	pulses = [0,0,0,0,0]
	dir_ena = 0
	enable = 1
	
	#Starting Serial Interface
	print ('Starting connection to arduino')	
	ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.005)
	rospy.sleep(3.0)
	print('Connected to Arduino')	
	print('You can now control Robot using KeyBoard')

	while (run_program==True):

		tm = time.clock()

		write_Int16(pulses[0],ser)
		write_Int16(pulses[1],ser)
		write_Int16(pulses[2],ser)
		write_Int16(pulses[3],ser)
		write_Int16(pulses[4],ser)
		write_Byte(dir_ena,ser)
		pulses = [0,0,0,0,0]
		#dir_ena = 0
		n = ser.inWaiting()
		if(n>0):
			if(n==1):
				sensor_val = ord(ser.read(n))
				#print(sensor_val)
			else:
				#Clearing buffer in case of wrong data from arduino
				ser.read(n)

    		for event in pygame.event.get():

        		if (pygame.key.get_pressed()[pygame.K_q]):
				run_program=False
				print('Existing')

        		if (pygame.key.get_pressed()[pygame.K_LEFT] and pygame.key.get_pressed()[pygame.K_x]):
            			#move_x_left()
				print('Moving X to Left')
				pulses[0]=5
				dir_ena = 0b00100001

        		if (pygame.key.get_pressed()[pygame.K_RIGHT] and pygame.key.get_pressed()[pygame.K_x]):
           			#move_x_right()
				print('Moving X to Right')
				pulses[0]=5
				dir_ena = 0b00100000

			if (pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_y]):
            			#move_y_back()
				print('Moving Y Back')
				pulses[1]=5
				dir_ena = 0b00100000

			if (pygame.key.get_pressed()[pygame.K_DOWN] and pygame.key.get_pressed()[pygame.K_y]):
            			#move_y_front()
				print('Moving Y Front')
				pulses[1]=5
				dir_ena = 0b00100010

			if (pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_z]):
            			#move_z_up()
				print('Moving Z Up')
				pulses[2]=5
				dir_ena = 0b00100000

			if (pygame.key.get_pressed()[pygame.K_DOWN] and pygame.key.get_pressed()[pygame.K_z]):
            			#move_z_down()
				print('Moving Z Down')
				pulses[2]=5
				dir_ena = 0b00100100
		
			if (pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_u]):
            			move_u_up()
				pulses[3]=5
				dir_ena = 0b00100000

			if (pygame.key.get_pressed()[pygame.K_DOWN] and pygame.key.get_pressed()[pygame.K_u]):
            			move_u_down()
				pulses[3]=5
				dir_ena = 0b00101000
			
			if (pygame.key.get_pressed()[pygame.K_LEFT] and pygame.key.get_pressed()[pygame.K_v]):
            			move_v_left()
				pulses[4]=5
				dir_ena = 0b00100000

        		if (pygame.key.get_pressed()[pygame.K_RIGHT] and pygame.key.get_pressed()[pygame.K_v]):
           			move_v_right()
				pulses[4]=5
				dir_ena = 0b00110000

		tm = time.clock()-tm
		time.sleep(0.01-tm)


	


if __name__ == '__main__':
	try:
		key_pressed_listener()
	except rospy.ROSInterruptException:
		pass

