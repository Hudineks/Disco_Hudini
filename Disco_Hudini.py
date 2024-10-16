import RPi.GPIO as GPIO
import time

# Nastavení GPIO pinů
RedPin = 17
GreenPin = 27
BluePin = 22
EncPinA = 23
EncPinB = 24
ButtonPin = 25

PWM_FREQ = 1000
current_color = [0, 0, 0]
selected_color = 0
brightness_step = 10

# Potlačení varování o používaných pinech
GPIO.setwarnings(False)

# Resetování GPIO při spuštění
GPIO.cleanup()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RedPin, GPIO.OUT)
    GPIO.setup(GreenPin, GPIO.OUT)
    GPIO.setup(BluePin, GPIO.OUT)
    GPIO.setup(EncPinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(EncPinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    global red_pwm, green_pwm, blue_pwm
    red_pwm = GPIO.PWM(RedPin, PWM_FREQ)
    green_pwm = GPIO.PWM(GreenPin, PWM_FREQ)
    blue_pwm = GPIO.PWM(BluePin, PWM_FREQ)
    red_pwm.start(0)
    green_pwm.start(0)
    blue_pwm.start(0)

def update_led():
    red_pwm.ChangeDutyCycle(current_color[0])
    green_pwm.ChangeDutyCycle(current_color[1])
    blue_pwm.ChangeDutyCycle(current_color[2])
    print(f"R={current_color[0]}, G={current_color[1]}, B={current_color[2]}")

def encoder_callback(channel):
    global current_color
    a_state = GPIO.input(EncPinA)
    b_state = GPIO.input(EncPinB)
    
    if a_state == b_state:
        current_color[selected_color] = min(current_color[selected_color] + brightness_step, 100)
    else:
        current_color[selected_color] = max(current_color[selected_color] - brightness_step, 0)
    
    update_led()

def button_callback(channel):
    global selected_color
    selected_color = (selected_color + 1) % 3
    print(f"Vybraná barva: {'Červená' if selected_color == 0 else 'Zelená' if selected_color == 1 else 'Modrá'}")

def loop():
    GPIO.add_event_detect(EncPinA, GPIO.BOTH, callback=encoder_callback)
    GPIO.add_event_detect(ButtonPin, GPIO.FALLING, callback=button_callback, bouncetime=300)
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    setup()
    loop()
