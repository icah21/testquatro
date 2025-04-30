import time
import threading
import RPi.GPIO as GPIO
from stepper_motor import StepperMotor
from ir_sensor import IRSensor

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Initialize IR sensor and stepper motor
ir_sensor = IRSensor(pin=17)
motor = StepperMotor(in1=18, in2=23, in3=24, in4=25)

# Shared state
current_angle = 0

def motor_thread_func():
    global current_angle
    while True:
        if ir_sensor.is_object_detected():
            print("Object detected!")

            # Rotate to 90 degrees
            current_angle = motor.go_to_angle(current_angle, 90)
            time.sleep(3)

            # Rotate to 180 degrees
            current_angle = motor.go_to_angle(current_angle, 180)
            time.sleep(2)

            # Return to 0 degrees
            current_angle = motor.go_to_angle(current_angle, 0)
            time.sleep(2)
        else:
            time.sleep(0.1)

def main():
    try:
        motor_thread = threading.Thread(target=motor_thread_func)
        motor_thread.daemon = True  # Ensures the thread exits with the main program
        motor_thread.start()

        while True:
            time.sleep(1)  # Keep main thread alive

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
