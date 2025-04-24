import RPi.GPIO as GPIO
import time

# GPIO pins for the ULN2003 connected to the 28BYJ-48 motor
IN1 = 18
IN2 = 23
IN3 = 24
IN4 = 25

# 512 steps = 360 degrees => 1.422 steps per degree
DEGREES_TO_STEPS = lambda deg: int(deg * 512 / 360)

# Half-step sequence
SEQUENCE = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]

def setup_motor():
    GPIO.setmode(GPIO.BCM)
    for pin in [IN1, IN2, IN3, IN4]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def move_stepper(steps, delay=0.002):
    for _ in range(abs(steps)):
        for halfstep in SEQUENCE if steps > 0 else reversed(SEQUENCE):
            for pin, val in zip([IN1, IN2, IN3, IN4], halfstep):
                GPIO.output(pin, val)
            time.sleep(delay)

def rotate_to_position(current_deg, target_deg):
    steps = DEGREES_TO_STEPS(target_deg - current_deg)
    move_stepper(steps)
    return target_deg  # new current_deg

def cleanup_motor():
    for pin in [IN1, IN2, IN3, IN4]:
        GPIO.output(pin, 0)
    GPIO.cleanup([IN1, IN2, IN3, IN4])
