import lgpio
import time

# Pin definitions (adjust as needed)
ROTARY_CLK_PIN = 17  # Rotary encoder CLK pin
ROTARY_DT_PIN = 27   # Rotary encoder DT pin
BUTTON_PIN = 22      # Rotary encoder push button
LED_R_PIN = 23       # Red channel
LED_G_PIN = 24       # Green channel
LED_B_PIN = 25       # Blue channel

# Initial setup
h = lgpio.gpiochip_open(0)  # Open GPIO chip
lgpio.gpio_claim_input(h, ROTARY_CLK_PIN)
lgpio.gpio_claim_input(h, ROTARY_DT_PIN)
lgpio.gpio_claim_input(h, BUTTON_PIN)

lgpio.gpio_claim_output(h, LED_R_PIN)
lgpio.gpio_claim_output(h, LED_G_PIN)
lgpio.gpio_claim_output(h, LED_B_PIN)

# Initial values
current_color = [255, 0, 0]  # Red, Green, Blue
brightness = 255
last_clk = lgpio.gpio_read(h, ROTARY_CLK_PIN)

def set_led_color(color, brightness):
    """ Set LED color with brightness adjustment. """
    r = int(color[0] * (brightness / 255))
    g = int(color[1] * (brightness / 255))
    b = int(color[2] * (brightness / 255))
    
    lgpio.gpio_write(h, LED_R_PIN, r)
    lgpio.gpio_write(h, LED_G_PIN, g)
    lgpio.gpio_write(h, LED_B_PIN, b)

def change_color():
    """ Cycle through primary colors: Red, Green, Blue. """
    global current_color
    if current_color == [255, 0, 0]:  # Red
        current_color = [0, 255, 0]  # Green
    elif current_color == [0, 255, 0]:  # Green
        current_color = [0, 0, 255]  # Blue
    else:
        current_color = [255, 0, 0]  # Red

def read_encoder():
    """ Read rotary encoder to adjust brightness. """
    global last_clk, brightness
    clk_state = lgpio.gpio_read(h, ROTARY_CLK_PIN)
    dt_state = lgpio.gpio_read(h, ROTARY_DT_PIN)
    
    if clk_state != last_clk:
        if dt_state != clk_state:
            brightness += 10
        else:
            brightness -= 10
        
        brightness = max(0, min(brightness, 255))  # Keep brightness within bounds
        last_clk = clk_state
        print(f"Brightness: {brightness}")
        set_led_color(current_color, brightness)

# Main loop
try:
    print("Rotary encoder and RGB LED program started.")
    set_led_color(current_color, brightness)
    
    while True:
        read_encoder()
        
        # Button pressed: change color
        if lgpio.gpio_read(h, BUTTON_PIN) == 0:
            change_color()
            print(f"Color changed to: {current_color}")
            set_led_color(current_color, brightness)
            time.sleep(0.3)  # Debounce delay
        
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

finally:
    lgpio.gpiochip_close(h)  # Close GPIO chip
