
import lcd
import time
import RPi.GPIO as GPIO
from gpiozero import Button
from gpiozero import LED
import math
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime
import RPi.GPIO as GPIO
import os
from datetime import datetime
from collections import deque
option= [["Temperature:","Fan:","Fish Tank:","Lamp:","Time:"],["Room:","On","Feed","Light1"],["Fish Tank","Off","Light","Light2"],["Outside:","..","..",".."]]
out="Hello Sean"
times=["06:00:00","12:00:00","18:00:00"]
lcd.lcd_init()
lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
lcd.lcd_string(out,2)
time.sleep(1)
button1 = Button(22)
button2 = Button(27)
button3 = Button(17)
button4 = Button(4)
led1=LED(21)
led2=LED(20)
led3=LED(16)
led4=LED(12)
led5=LED(24)
led1.on()
#led2.on()
led3.on()
led4.on()
led5.on()
x=0
y=0
tic1=0
tic2=0
tic3=0
tic4=0
pretic1=0
pretic2=0
pretic3=0
pretic4=0
temp1=0
flag=0
flag2=0
flag3=0
fdtm=0
override=0
on=0
def temp():
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
	cs = digitalio.DigitalInOut(board.D5)
	mcp = MCP.MCP3008(spi, cs)
	chan = AnalogIn(mcp, MCP.P1)
	temp= round(((1000*chan.voltage)-500)/10)
	pretic2=time.perf_counter()
	return temp


def button1_pressed():
	global tic1,pretic1,out,x,y
	tic1 = time.perf_counter()
	dif= tic1-pretic1
	if dif>0.1:
		if y==0:
			if x==0:
				x=4
			else:
				x=x-1
		else:
			if y==1:
				y=3
			else:
				y=y-1
	out=option[y][x]

def button2_pressed():
	global tic2,pretic2,out,x,y
	tic2 = time.perf_counter()
	dif= tic2-pretic2
	if dif>0.1:
		if y==0:
			if x==4:
				x=0
			else:
				x=x+1
		else:
			if y==3:
				y=1
			else:
				y=y+1
	out=option[y][x]

def button3_pressed():
	global tic3,pretic3,out,x,y,flag,flag2,flag3,override,on
	tic3 = time.perf_counter()
	dif = tic3-pretic3
	if dif>0.1:
		if y == 0 and x<4 :
			y=y+1
		if (out==option[1][1]):
			led1.off() #led1.on()
			override=1
			on=1
		elif (out==option[1][1] and on==1):
			override==0
		if (out==option[2][1] and on==1):
			led1.on() #led1.off()
			override=1
			on=0
		elif (out==option[2][1] and on==0):
			override=0
		if (out==option[1][2]):
			#led2.on() #led2.on()
			#time.sleep(2)
			#led2.off() #led2.off()
			feedfish()
		if (out==option[2][2]):
			if (flag==0):
				led3.off() #led3.on()
				flag=1
			elif (flag==1):
				led3.on() # led3.off()
				flag=0
		if (out==option[1][3]):
			if (flag2==0):
				led4.off() #led4.on()
				flag2=1
			elif(flag2==1):
				led4.on() #led4.off()
				flag2=0
		if (out==option[2][3]):
			if (flag3==0):
				led5.off() #led5.on()
				flag3=1
			elif(flag3==1):
				led5.on() # led5.off()
				flag3=0
	out=option[y][x]

def button4_pressed():
	global tic4,pretic4,out,x,y
	tic4 = time.perf_counter()
	dif = tic4-pretic4
	if dif>0.1:
		if y>0:
			y=0
	out=option[y][x]
def feedfish():
	led2.on()
	time.sleep(1)
	led2.off()
try:
	def run_main():
		global pretic3,pretic4,temp1,times,fdtm,override,on
		heater=0
		out=option[y][x]
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		bang=times.count(current_time)
		pretic1=time.perf_counter()
		dif=pretic3-pretic4
		if dif>900 or pretic4==0:
			temp1=temp()
			pretic4=time.perf_counter()
		if (temp1<=26 and override==0 ): #define override
			led1.off()
			on=1
		elif (temp1>26 and override==0):
			led1.on()
			on=0
		if bang>0:
			feedfish()
		if (out==option[0][0] or out==option[1][0]):
			lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
			lcd.lcd_string(out+str(temp1),1)
		elif (out==option[2][0]):
			lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
			lcd.lcd_string(out+":N/A",1)
		elif (out==option[3][0]):
			temp2=temp1-6
			lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
			lcd.lcd_string(out+str(temp2),1)
		elif (out==option[0][4]):
			lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
			lcd.lcd_string(out+current_time,1)

		else:
			lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
			lcd.lcd_string(out,1)
		button1.when_pressed = button1_pressed
		button2.when_pressed = button2_pressed
		button3.when_pressed = button3_pressed
		button4.when_pressed = button4_pressed
	while True:
		run_main()
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()

