import RPi.GPIO as GPIO
import time

angles = [0.00]*3

angles[0] = 90
angles[1] = 90
angles[2] = 90

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Pin definitions for three servos
servo_pins = [17, 27, 22]

# Set all GPIO pins for servos as output
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)

# Create PWM instances for each servo, set frequency to 50Hz (common for servos)
servo_pwm = [GPIO.PWM(pin, 50) for pin in servo_pins]

# Start PWM with 0 duty cycle (servos are initially in a neutral position)
for pwm in servo_pwm:
    pwm.start(0)

# Function to set the servo angle (0 to 180 degrees)
def set_angle(servo_index, angle):
    # Formula to convert angle to duty cycle for PWM signal
    duty_cycle = float(angle) / 18 + 2
    servo_pwm[servo_index].ChangeDutyCycle(duty_cycle)

# Function to stop PWM
def stop_servos():
    for pwm in servo_pwm:
        pwm.stop()

# Main function to control servos
def control_servos():
    try:
        a = 90
        # Set each servo to a different static angle
        angles = [a, a, a]

        # Set all servos to their desired angles
        for i in range(3):  # Loop through each servo
            angle = angles[i]
            print(f"Setting Servo {i+1} to {angle}°")
            set_angle(i, angle)

        # Allow servos to stay at their positions for a while
        time.sleep(2)  # Give servos time to stabilize at their positions

    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        stop_servos()
        GPIO.cleanup()

# Run the control function
if __name__ == "__main__":
    control_servos()