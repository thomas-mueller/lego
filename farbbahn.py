#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# -----------------------------------------------
# Imports

import time
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveSteering
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sound import Sound
from ev3dev2.led import Leds

# -----------------------------------------------
# Funktionen
def farbe_messen(color_sensor, anzahl_versuche=5):
	farbzahl, farbe = None, None
	for versuch in range(anzahl_versuche):
		farbzahl = color_sensor.color
		farbe = color_sensor.color_name
	return farbzahl, farbe


# -----------------------------------------------
# Initialisierungen

leds = Leds()
#sound = Sound()

fahrwerkssteurerung = MoveSteering(OUTPUT_B, OUTPUT_C)

touch_sensor = TouchSensor(INPUT_1)
color_sensor = ColorSensor(INPUT_3)
ultrasonic_sensor = UltrasonicSensor(INPUT_4)
gyros_sensor = GyroSensor(INPUT_2)

# -----------------------------------------------
# Aktionen
leds.animate_flash("GREEN", sleeptime=0.1, duration=1)
print("Startbereit")

#sound.speak("Welcome! Lets start!")

startzeit = time.perf_counter()
fahrwerkssteurerung.on(0, SpeedPercent(15))

letzte_farbzahl = -1
while True:
	farbzahl, farbe = farbe_messen(color_sensor, anzahl_versuche = 10)
	print(farbzahl, farbe)
	if farbzahl == 5 :
		fahrwerkssteurerung.on(20, SpeedPercent(15))
	elif (letzte_farbzahl != 5) or (letzte_farbzahl != 6) :
		fahrwerkssteurerung.on(-20, SpeedPercent(15))
	
	if (farbzahl == 6) and (letzte_farbzahl == 5) :
		fahrwerkssteurerung.on(20, SpeedPercent(15))
	elif (farbzahl == 6) and ((letzte_farbzahl != 5) or (letzte_farbzahl != 6)) :
		print("ich bin hier")
		fahrwerkssteurerung.on(-20, SpeedPercent(15))
	
	if farbzahl != letzte_farbzahl:
		letzte_farbzahl = farbzahl
		
	laufzeit = time.perf_counter() - startzeit
	if laufzeit > 10:
		break

fahrwerkssteurerung.off()

#if touch_sensor.is_pressed:
#touch_sensor.wait_for_pressed()
	
#	print("ist gedrueckt")
#time.sleep(1)
#fahrwerkssteurerung.on_for_seconds(SpeedPercent(70), SpeedPercent(70), 3)
#else:
#	print("ist nicht gedrueckt")
	
#ultrasonic_sensor.MODE_US_DIST_CM








