import RPi.GPIO as GPIO

IR_PIN = 17  # Change to the GPIO pin you connected your IR sensor to

def setup_ir():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_PIN, GPIO.IN)

def object_detected():
    return GPIO.input(IR_PIN) == GPIO.LOW  # LOW means object is detected

def cleanup_ir():
    GPIO.cleanup(IR_PIN)
