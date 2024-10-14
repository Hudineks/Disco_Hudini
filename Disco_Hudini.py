import lgpio
import time

# Definice GPIO pinů
RedPin = 17
GreenPin = 27
BluePin = 22
EncPinA = 23
EncPinB = 24
ButtonPin = 25

# Nastavení frekvence PWM a kroku jasu
PWM_FREQ = 1000
brightness_step = 10

# Výchozí nastavení barev (0-100)
current_color = [0, 0, 0]  # R, G, B
selected_color = 0  # 0 = R, 1 = G, 2 = B

# Inicializace GPIO
h = lgpio.gpiochip_open(0)  # Otevře přístup k GPIO čipu

# Nastavení pinů pro vstup a výstup
lgpio.gpio_claim_input(h, EncPinA)
lgpio.gpio_claim_input(h, EncPinB)
lgpio.gpio_claim_input(h, ButtonPin)

lgpio.gpio_claim_output(h, RedPin)
lgpio.gpio_claim_output(h, GreenPin)
lgpio.gpio_claim_output(h, BluePin)

# Nastavení PWM na výstupních pinech
lgpio.tx_pwm(h, RedPin, PWM_FREQ, 0)
lgpio.tx_pwm(h, GreenPin, PWM_FREQ, 0)
lgpio.tx_pwm(h, BluePin, PWM_FREQ, 0)

# Funkce pro aktualizaci jasu LED
def update_led():
    lgpio.tx_pwm(h, RedPin, PWM_FREQ, current_color[0])
    lgpio.tx_pwm(h, GreenPin, PWM_FREQ, current_color[1])
    lgpio.tx_pwm(h, BluePin, PWM_FREQ, current_color[2])
    print(f"R={current_color[0]}, G={current_color[1]}, B={current_color[2]}")

# Funkce pro změnu jasu na základě otočení enkodéru
def adjust_brightness(direction):
    global current_color
    if direction == "up":
        current_color[selected_color] = min(current_color[selected_color] + brightness_step, 100)
    elif direction == "down":
        current_color[selected_color] = max(current_color[selected_color] - brightness_step, 0)
    update_led()

# Funkce pro detekci změny na enkodéru
def read_encoder():
    state_a = lgpio.gpio_read(h, EncPinA)
    state_b = lgpio.gpio_read(h, EncPinB)
    if state_a == 0 and state_b == 1:
        return "up"
    elif state_a == 1 and state_b == 0:
        return "down"
    return None

# Hlavní smyčka
try:
    print("Program spuštěn. Stiskni tlačítko pro změnu barvy.")

    while True:
        # Čtení z enkodéru
        direction = read_encoder()
        if direction:
            adjust_brightness(direction)

        # Zjištění, jestli bylo stisknuto tlačítko
        if lgpio.gpio_read(h, ButtonPin) == 0:  # Tlačítko stisknuto
            selected_color = (selected_color + 1) % 3  # Přepínání mezi R, G, B
            color_name = ["Red", "Green", "Blue"][selected_color]
            print(f"Vybraná barva: {color_name}")
            time.sleep(0.5)  # Debounce pro tlačítko

        time.sleep(0.1)  # Krátká pauza pro snížení zátěže CPU

except KeyboardInterrupt:
    pass

finally:
    # Ukončení a čištění GPIO
    lgpio.gpiochip_close(h)
