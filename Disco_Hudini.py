import lgpio
import time

# Definování GPIO pinů
RedPin = 17
GreenPin = 27
BluePin = 22
EncPinA = 23
EncPinB = 24
ButtonPin = 25

PWM_FREQ = 1000  # Frekvence PWM
brightness_step = 10  # Krok pro zvýšení/snížení jasu

# Inicializace GPIO
h = lgpio.gpiochip_open(0)  # Otevření GPIO čipu

# Nastavení pinů pro enkodér a tlačítko
lgpio.gpio_claim_input(h, EncPinA)
lgpio.gpio_claim_input(h, EncPinB)
lgpio.gpio_claim_input(h, ButtonPin)

# Nastavení výstupních pinů pro RGB LED
lgpio.gpio_claim_output(h, RedPin)
lgpio.gpio_claim_output(h, GreenPin)
lgpio.gpio_claim_output(h, BluePin)

# Nastavení PWM na jednotlivé piny
lgpio.tx_pwm(h, RedPin, PWM_FREQ, 0)
lgpio.tx_pwm(h, GreenPin, PWM_FREQ, 0)
lgpio.tx_pwm(h, BluePin, PWM_FREQ, 0)

# Výchozí barvy
current_color = [0, 0, 0]  # R, G, B jasy v procentech (0-100)
selected_color = 0  # 0 = červená, 1 = zelená, 2 = modrá

# Funkce pro aktualizaci PWM signálu pro LED
def update_led():
    lgpio.tx_pwm(h, RedPin, PWM_FREQ, current_color[0])
    lgpio.tx_pwm(h, GreenPin, PWM_FREQ, current_color[1])
    lgpio.tx_pwm(h, BluePin, PWM_FREQ, current_color[2])
    print(f"R={current_color[0]}%, G={current_color[1]}%, B={current_color[2]}%")

# Funkce pro změnu jasu vybrané barvy
def adjust_brightness(direction):
    global current_color
    if direction == "up":
        current_color[selected_color] = min(current_color[selected_color] + brightness_step, 100)
    elif direction == "down":
        current_color[selected_color] = max(current_color[selected_color] - brightness_step, 0)
    update_led()

# Funkce pro čtení stavu enkodéru
last_state = 0
def read_encoder():
    global last_state
    state_a = lgpio.gpio_read(h, EncPinA)
    state_b = lgpio.gpio_read(h, EncPinB)
    encoder_value = (state_a << 1) | state_b  # Spojení stavů pinů A a B do jednoho čísla

    if last_state != encoder_value:
        if last_state == 0b00 and encoder_value == 0b01:  # Rotace doprava
            return "up"
        elif last_state == 0b00 and encoder_value == 0b10:  # Rotace doleva
            return "down"
    last_state = encoder_value
    return None

# Funkce pro debounce tlačítka
def debounce_button():
    if lgpio.gpio_read(h, ButtonPin) == 0:
        time.sleep(0.05)  # 50ms debounce
        if lgpio.gpio_read(h, ButtonPin) == 0:
            return True
    return False

# Hlavní smyčka
try:
    print("Program spuštěn. Otáčej enkodérem a stiskni tlačítko pro změnu barvy.")
    while True:
        # Zpracování rotace enkodéru
        direction = read_encoder()
        if direction:
            adjust_brightness(direction)

        # Zpracování tlačítka (změna barvy)
        if debounce_button():
            selected_color = (selected_color + 1) % 3  # Přepínání mezi R, G, B
            color_name = ["Red", "Green", "Blue"][selected_color]
            print(f"Vybraná barva: {color_name}")
            time.sleep(0.5)  # Malý delay pro zabránění dvojímu stisku

        time.sleep(0.1)  # Pauza pro snížení zátěže CPU

except KeyboardInterrupt:
    print("Ukončuji program.")

finally:
    # Vyčištění GPIO a zavření připojení
    lgpio.gpiochip_close(h)
