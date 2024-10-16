import RPi.GPIO as GPIO
import time

# Nastavení GPIO pinů
RedPin = 17
GreenPin = 22
BluePin = 27
EncPinA = 23
EncPinB = 24
ButtonPin = 25

PWM_FREQ = 1000
current_color = [0, 0, 0]  # RGB hodnoty (0-100 pro PWM)
selected_color = 0  # Index aktuálně vybrané barvy (0=Red, 1=Green, 2=Blue)
brightness_step = 10  # Krok změny jasu (0-100)

# Potlačení varování o používání stejných pinů
GPIO.setwarnings(False)
# Resetování GPIO při spuštění
GPIO.cleanup()

def setup():
    GPIO.setmode(GPIO.BCM)
    
    # Nastavení pinů pro RGB LED
    GPIO.setup(RedPin, GPIO.OUT)
    GPIO.setup(GreenPin, GPIO.OUT)
    GPIO.setup(BluePin, GPIO.OUT)
    
    # Nastavení pinů pro enkodér a tlačítko
    GPIO.setup(EncPinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(EncPinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Nastavení PWM pro LED
    global red_pwm, green_pwm, blue_pwm
    red_pwm = GPIO.PWM(RedPin, PWM_FREQ)
    green_pwm = GPIO.PWM(GreenPin, PWM_FREQ)
    blue_pwm = GPIO.PWM(BluePin, PWM_FREQ)
    red_pwm.start(0)
    green_pwm.start(0)
    blue_pwm.start(0)

def update_led():
    """Aktualizuje LED podle aktuálních hodnot RGB."""
    red_pwm.ChangeDutyCycle(current_color[0])
    green_pwm.ChangeDutyCycle(current_color[1])
    blue_pwm.ChangeDutyCycle(current_color[2])
    print(f"R={current_color[0]}, G={current_color[1]}, B={current_color[2]}")

# Sledování předchozích stavů enkodéru
last_a_state = GPIO.LOW
last_rotary_time = 0

def encoder_callback(channel):
    """Callback pro změnu stavu enkodéru."""
    global last_a_state, last_rotary_time, current_color, selected_color
    
    # Zamezení častým změnám (debounce)
    current_time = time.time()
    if current_time - last_rotary_time < 0.1:  # 100 ms debounce
        return
    last_rotary_time = current_time
    
    a_state = GPIO.input(EncPinA)
    b_state = GPIO.input(EncPinB)
    
    # Detekce rotace enkodéru podle Gray kódu
    if a_state != last_a_state:  # Změna stavu enkodéru
        if a_state == b_state:
            # Otáčení ve směru hodinových ručiček
            current_color[selected_color] = min(current_color[selected_color] + brightness_step, 100)
        else:
            # Otáčení proti směru hodinových ručiček
            current_color[selected_color] = max(current_color[selected_color] - brightness_step, 0)
        
        update_led()  # Aktualizace LED
    
    last_a_state = a_state

def button_callback(channel):
    """Callback pro tlačítko enkodéru (změna vybrané barvy)."""
    global selected_color
    selected_color = (selected_color + 1) % 3  # Přepínání mezi R, G, B
    print(f"Vybraná barva: {'Červená' if selected_color == 0 else 'Zelená' if selected_color == 1 else 'Modrá'}")

def loop():
    """Hlavní smyčka programu pro zpracování událostí."""
    GPIO.add_event_detect(EncPinA, GPIO.BOTH, callback=encoder_callback)
    GPIO.add_event_detect(ButtonPin, GPIO.FALLING, callback=button_callback, bouncetime=300)
    
    try:
        while True:
            time.sleep(0.1)  # Malé zpoždění pro úsporu CPU
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    setup()
    loop()