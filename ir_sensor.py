import RPi.GPIO as GPIO
import time

IR_PIN = 17  # Update this GPIO pin if needed

def setup_ir():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_PIN, GPIO.IN)

def object_detected():
    return GPIO.input(IR_PIN) == GPIO.LOW  # LOW means object detected

def cleanup_ir():
    GPIO.cleanup(IR_PIN)
