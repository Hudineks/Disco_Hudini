
# Rotary Encoder RGB LED Controller for Raspberry Pi

## Project Overview

This project demonstrates the use of a rotary encoder and a 4-legged RGB LED connected to a Raspberry Pi. The rotary encoder is used to adjust the brightness of individual colors (Red, Green, and Blue) of the LED. The encoder’s button switches between colors. Rotating the encoder adjusts the brightness of the selected color, and the current brightness values are updated in real-time on the RGB LED.

---

## Hardware Requirements
- Raspberry Pi 4 (or similar model)
- 4-legged RGB LED (common anode or common cathode)
- Rotary encoder with push button (e.g., HW-040)
- Breadboard and jumper wires
- Resistors (220Ω recommended for each LED leg)
- Python 3 environment with necessary libraries

---

## Software Requirements
- Python 3
- `lgpio` library for GPIO control
- Git for version control

---

## Goal

The goal of this project is to create a circuit and develop a Python program that allows users to control the brightness of an RGB LED using a rotary encoder. The button on the encoder is used to switch between Red, Green, and Blue colors, while rotating the encoder adjusts the brightness of the currently selected color.

---

## Setup Instructions

### 1. Wiring the Hardware

Connect the components as follows:

- **RGB LED**:
  - Red leg → GPIO 17 (through a resistor)
  - Green leg → GPIO 22 (through a resistor)
  - Blue leg → GPIO 27 (through a resistor)
  - Common leg (anode/cathode) → Ground or VCC depending on the LED type

- **Rotary Encoder**:
  - Pin A → GPIO 23
  - Pin B → GPIO 24
  - Button pin → GPIO 25
  - GND pin → Ground on Raspberry Pi

#### Possible Circuit Diagram:
(Currently missing – please update with a clear image of the wiring diagram.)

---

### 2. Python Script

The Python script controls the RGB LED and listens to the rotary encoder events. The main functionalities include:
- **Brightness Adjustment**: Rotating the encoder increases or decreases the brightness of the selected color.
- **Color Selection**: Pressing the encoder button switches between the three color channels (Red, Green, and Blue).
- **Console Output**: The current brightness levels for each color are printed to the console for debugging purposes.

---

### 3. How to Run

1. Clone this repository to your Raspberry Pi:
   ```bash
   git clone https://github.com/Hudineks/Disco_Hudini
   ```
2. Navigate to the project directory:
   ```bash
   cd Disco_Hudini
   ```
3. Install the required Python libraries:
   ```bash
   pip install lgpio
   ```
4. Run the Python script:
   ```bash
   python3 main.py
   ```

---

## Performance and Limitations

### How the Approach Works:
- The rotary encoder provides smooth and precise control over the brightness levels of the RGB LED.
- Pressing the button effectively switches between the Red, Green, and Blue channels.

### Known Limitations:
- **Fast Rotation**: If the rotary encoder is turned too quickly, some steps may be skipped, leading to less precise brightness adjustments.
- **Slow Rotation**: The encoder works best with moderate to slow rotation speeds. Extremely slow rotations may not register properly.
- **Debouncing**: Poorly debounced signals might cause erratic behavior; ensure the encoder has proper hardware or software debouncing implemented.

---

## License

This project is open-source and available under the MIT License.

For any issues or contributions, feel free to open a pull request or an issue on GitHub.

---
