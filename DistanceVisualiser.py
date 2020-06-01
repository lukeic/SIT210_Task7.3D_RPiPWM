import RPi.GPIO as GPIO
import time

PIN_TRIGGER = 7
PIN_ECHO = 11
PIN_LED = 13
OUT_PINS = [ PIN_TRIGGER, PIN_LED ]
SENSOR_MAX_RANGE = 4000
ULTRASONIC_SOUND_CMPS = 34300

pulse_start = 0
pulse_end = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUT_PINS, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def calculate_distance():
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * ULTRASONIC_SOUND_CMPS) / 2
    return round(distance)


try:
    led = GPIO.PWM(PIN_LED, 50)
    led.start(0)

    while(1):
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(PIN_ECHO) == 1:
            pulse_end = time.time()

        distance_cm = calculate_distance()
        distance_percent = (distance_cm / SENSOR_MAX_RANGE) * 100

        print("Distance {}cm ({}%)".format(distance_cm, distance_percent))

        led.ChangeDutyCycle(distance_percent)
except KeyboardInterrupt:
    led.stop()
    GPIO.cleanup()

