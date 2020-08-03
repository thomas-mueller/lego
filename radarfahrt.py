#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# -----------------------------------------------
# Imports

import time
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveSteering
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sound import Sound
from ev3dev2.led import Leds

# -----------------------------------------------
# Funktionen
def wiederholt_messen(sensor, messung, wiederholungen=10):
	sensor_function = getattr(sensor, messung)
	messung = None
	for wiederholung in range(wiederholungen):
		messung = sensor_function
	return messung


# -----------------------------------------------
# Initialisierungen

leds = Leds()
#sound = Sound()

fahrwerkssteurerung = MoveSteering(OUTPUT_B, OUTPUT_C)
m_motor = MediumMotor(OUTPUT_A)
touch_sensor = TouchSensor(INPUT_1)
color_sensor = ColorSensor(INPUT_4)
ultrasonic_sensor = UltrasonicSensor(INPUT_3)
#gyros_sensor = GyroSensor(INPUT_2)

# -----------------------------------------------
# Aktionen
leds.animate_flash("GREEN", sleeptime=0.1, duration=1)
print("Startbereit")

#sound.speak("Welcome! Lets start!")

startzeit = time.perf_counter()

#m_motor.on_for_degrees(SpeedPercent(15), 45)                   
#m_motor.on_for_degrees(SpeedPercent(15), -90)
#m_motor.on_for_degrees(SpeedPercent(15), 45)

fahrwerkssteurerung.on(0, SpeedPercent(8))

while True: 
	winkel_liste = [-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100]
	abstandsmessungen = {}
	m_motor.on_to_position(SpeedPercent(100), winkel_liste[0])
	for winkel in winkel_liste:
		print("winkel:", winkel)
		m_motor.on_to_position(SpeedPercent(10), winkel)
#		time.sleep(0.5)
		abstand = wiederholt_messen(ultrasonic_sensor, "distance_centimeters_continuous", 10)
		print("abstand:", abstand)
		abstandsmessungen[winkel] = abstand
	m_motor.on_to_position(SpeedPercent(100), winkel_liste[0])
	print("abstandsmessungen:", abstandsmessungen)
	winkel_groester_abstand, groester_abstand = max(abstandsmessungen.items(), key=lambda messung: messung[1])
	print("winkel_groester_abstand:", winkel_groester_abstand)
	print("groester_abstand:", groester_abstand)
	if winkel_groester_abstand < 0 :
		fahrwerkssteurerung.on(steering=90, speed=SpeedPercent(8))
		print("1")
	else :
		fahrwerkssteurerung.on(steering=-90, speed=SpeedPercent(8))
		print("2")
	
#	fahrwerkssteurerung.on(steering=90, speed=SpeedPercent(8))
	time.sleep(abs(winkel_groester_abstand/50))
	fahrwerkssteurerung.on(0, SpeedPercent(8))
	print("hallo")
	laufzeit = time.perf_counter() - startzeit
	if laufzeit > 60:
		break

fahrwerkssteurerung.off()
#while True:
#	abstand1 = wiederholt_messen(ultrasonic_sensor, "distance_centimeters_continuous", 10)
#	print("gerade aus:", abstand1)
#	m_motor.on_to_position(SpeedPercent(100), 60)    
#	abstand2 = wiederholt_messen(ultrasonic_sensor, "distance_centimeters_continuous", 10)
#	print("rechts:", abstand2)
#	m_motor.on_to_position(SpeedPercent(100), -120)
#	abstand3 = wiederholt_messen(ultrasonic_sensor, "distance_centimeters_continuous", 10)
#	print("links:", abstand3)
#	m_motor.on_to_position(SpeedPercent(100), 60)
#	kleinster_abstand = min(abstand1, abstand2, abstand3)
#	fahrwerkssteurerung.on(0, SpeedPercent(min(50, kleinster_abstand-5)))
#	if (kleinster_abstand <5 ) :
#		fahrwerkssteurerung.off()
#		break
#	
#	laufzeit = time.perf_counter() - startzeit
#	if laufzeit > 10:
#		break


