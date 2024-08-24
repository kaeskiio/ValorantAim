# Valorant Aim Soft Aimer

## Overview

This project demonstrates the integration of software and hardware to create a soft aim assist for the game Valorant using Python and Arduino. It highlights technical skills in programming, image processing, and hardware interfacing. **Note: This project is for educational purposes only and should not be used to gain unfair advantages in games.**

## Files

- **`ValorantAim.py`**: Python script for processing screen captures to identify targets.
- **`ValorantAim.ino`**: C++ script in Arduino IDE for interfacing with a microcontroller to simulate mouse movements for aim adjustment.

## Technical Skills Demonstrated

- **Python Programming**: Utilizes libraries for image processing and screen capture to identify targets on the screen.
- **C++ and Arduino IDE**: Programs a microcontroller to simulate mouse inputs based on data received from the Python script.
- **Hardware-Software Integration**: Combines software logic with hardware control to adjust aim in real-time.
- **Ethical Considerations**: Emphasizes the impact of cheats on fair play and the gaming community.

## Getting Started

### Prerequisites

- Python 3.x
- Arduino IDE
- Compatible microcontroller (e.g., [Arduino Leonardo:](https://www.amazon.com/Arduino-org-A000057-Arduino-Leonardo-Headers/dp/B008A36R2Y/ref=pd_bxgy_d_sccl_1/133-9690621-7191529?pd_rd_i=B008A36R2Y&psc=1))
- [USB Host Shield](https://www.amazon.com/Compatible-Arduino-Support-Android-Function/dp/B08PNVKKBH/ref=sr_1_1?dib=eyJ2IjoiMSJ9.vxEQnO9htL-9Odp7SHmx-ouVjMMbBI_u_Ekc9qCw4A3_8LVHBqK50jAzujtkDdixTzB8tN5ZbxJhehcNAISYPLYBftHhIWjI1LSlV4E5TI2AX2MhVlfgShxJ1A2SF3gwzWXaOxta5Fbh5P9fsx6nGQSbcsVkJPfA_myHL4to6EAMrZIRgA4ThSx-f_5Lb7EuI8ZRKidor2xZmqonXsALSyKpYMnZbRSwVg8N9tHZfZWZlgCkdJ_bOCbT-OUbA627IfbYCShqrEWNe-Vnrv7YjHl5kswt0Bb9HZK5vuzdrjc.43IBYDTU_0r06u1TRvP5E5WlxfHb0plU67j60wvpjiI&dib_tag=se&hvadid=604584067670&hvdev=c&hvlocphy=9027845&hvnetw=g&hvqmt=e&hvrand=2236715263586918760&hvtargid=kwd-295686902150&hydadcr=18034_13447342&keywords=usb%2Bhost%2Bshield%2Barduino&qid=1722365698&s=electronics&sr=1-1&th=1)
- USB cable 
- Valorant installed on your PC

## How It Works

### Python Script (`ValorantAim.py`)

- **Screen Capture**: Captures the current screen frame using libraries like `pyautogui` and `opencv-python`.
- **Target Detection**: Processes the captured image to identify targets using techniques such as color detection and contour finding.
- **Aim Adjustment Calculation**: Calculates the necessary movements to align the crosshair with the detected target and sends this data to the Arduino.

### Arduino Script (`ValorantAim.ino`)

- **Mouse Simulation**: Uses the Arduino Mouse library to simulate mouse movements based on the data received from the Python script.
- **Serial Communication**: Receives aim adjustment data from the Python script via serial communication and moves the mouse accordingly.

## Ethical Considerations

While this project demonstrates technical proficiency, it is important to understand the ethical implications of creating and using cheats in games. Cheating undermines fair play, affects the gaming experience of others, and is often against the terms of service of the game. This project should be used responsibly and with an understanding of these considerations.
