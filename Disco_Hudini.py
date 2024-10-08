import RPi.GPIO as GPIO
import time

#nastavení GPIO pinů

RedPin = 17
GreenPin = 27
BluePin = 22
EncPinA = 23
EncPinB = 24
ButtPin = 25

#frekvence pro neblikání
PWM_FREQ = 1000

#Ini. cond.
currentColor = [0, 0, 0]
selectedColor = 0
brightnessStep = 10

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RedPin, GPIO.OUT)
    GPIO.setup(GreenPin, GPIO.OUT)
    GPIO.setup(BluePin, GPIO.OUT)
    GPIO.setup(EncPinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(EncPinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ButtPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)



    global red_pwm, green_pwm, blue_pwm
    red_pwm = GPIO.PWM(RedPin, PWM_FREQ)
    green_pwm = GPIO.PWM(GreenPin, PWM_FREQ)
    blue_pwm = GPIO.PWM(BluePin, PWM_FREQ)
    red_pwm.start(0)
    green_pwm.start(0)
    blue_pwm.start(0)

def update_led():
    """Aktualizace barev LED podle aktuálního stavu"""
    red_pwm.ChangeDutyCycle(current_color[0])
    green_pwm.ChangeDutyCycle(current_color[1])
    blue_pwm.ChangeDutyCycle(current_color[2])
    print(f"Aktuální barva: R={current_color[0]}, G={current_color[1]}, B={current_color[2]}")

def encoder_callback(channel):
    """Zpracování otáčení enkodéru"""
    global current_color
    a_state = GPIO.input(EncPinA)
    b_state = GPIO.input(EncPinB)
    
    # Otočení doprava
    if a_state == b_state:
        current_color[selected_color] = min(current_color[selected_color] + brightnessStep, 100)
    else:
        current_color[selected_color] = max(current_color[selected_color] - brightnessStep, 0)
    
    update_led()

def button_callback(channel):
    """Přepínání mezi barvami po stisknutí tlačítka"""
    global selected_color
    selected_color = (selected_color + 1) % 3  # Cyklování mezi červenou, zelenou a modrou
    print(f"Vybraná barva: {'Červená' if selected_color == 0 else 'Zelená' if selected_color == 1 else 'Modrá'}")

def loop():
    """Hlavní smyčka programu"""
    GPIO.add_event_detect(EncPinA, GPIO.BOTH, callback=encoder_callback)
    GPIO.add_event_detect(ButtPin, GPIO.FALLING, callback=button_callback, bouncetime=300)
    
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







