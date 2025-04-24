import threading
import time
import ir_sensor
import stepper_motor

current_position = 0
object_detected_flag = False

def ir_thread():
    global object_detected_flag
    ir_sensor.setup_ir()
    try:
        while True:
            if ir_sensor.object_detected():
                object_detected_flag = True
            else:
                object_detected_flag = False
            time.sleep(0.1)
    except KeyboardInterrupt:
        ir_sensor.cleanup_ir()

def motor_thread():
    global current_position, object_detected_flag
    stepper_motor.setup_motor()
    try:
        while True:
            if object_detected_flag:
                # Always return to 0 before starting
                if current_position != 0:
                    current_position = stepper_motor.rotate_to_position(current_position, 0)
                    time.sleep(1)

                # Go to 90°
                current_position = stepper_motor.rotate_to_position(current_position, 90)
                time.sleep(10)

                # Go to 180°
                current_position = stepper_motor.rotate_to_position(current_position, 180)
                time.sleep(5)

                # Return to 0°
                current_position = stepper_motor.rotate_to_position(current_position, 0)
                time.sleep(5)
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        stepper_motor.cleanup_motor()

if __name__ == "__main__":
    ir_t = threading.Thread(target=ir_thread)
    motor_t = threading.Thread(target=motor_thread)

    ir_t.start()
    motor_t.start()

    ir_t.join()
    motor_t.join()
