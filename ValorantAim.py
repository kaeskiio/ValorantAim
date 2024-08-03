import tkinter as tk
import keyboard
import winsound
import time
import cv2
import numpy as np
import threading
import win32api
import random
import time
import numpy as np
from mss import mss
import threading
import PIL.Image
import serial
import screeninfo

# Adjustable Variables
FOV = 100
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
COM_PORT = "COM8"

# Additional Variables
ENABLE_VISUALIZER = False
SPEED_X = 1  # Speed factor for the X-axis movement
SPEED_Y = 0.4  # Speed factor for the Y-axis movement

class ScreenGrabber:
    def __init__(self, x, y, grabzone):
        self.x = x
        self.y = y
        self.grabzone = grabzone
        self.screen = np.zeros((grabzone, grabzone, 3), np.uint8)
        self.pillow = None
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()
        self.lock = threading.Lock()

    def update(self):
        while True:
            with mss() as sct:
                monitor = {
                    "top": self.y,
                    "left": self.x,
                    "width": self.grabzone,
                    "height": self.grabzone,
                }
                self.lock.acquire()
                self.pillow = sct.grab(monitor)
                self.screen = np.array(sct.grab(monitor))
                self.lock.release()

    def get_screen(self):
        return self.screen

    def get_pillow(self):
        return PIL.Image.frombytes(
            "RGB", self.pillow.size, self.pillow.bgra, "raw", "BGRX"
        )


class Mouse:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.timeout = 1
        self.ser.port = COM_PORT
        self.ser.open()

    def move(self, x, y):
        if x < 0:
            x = x + 256
        if y < 0:
            y = y + 256

        self.ser.write(b"M" + bytes([int(x), int(y)]))

    def click(self):
        self.ser.write(b"C")

    def close(self):
        self.ser.close()

    def __del__(self):
        self.close()


class SykoFire:
    def __init__(self, x, y, grabzone):
        self.mouse = Mouse()
        self.grabber = ScreenGrabber(x, y, grabzone)
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        self.lock = threading.Lock()
        self.toggled = True  # Program starts activated
        self.y_offset = 0
        self.x_speed = SPEED_X
        self.y_speed = SPEED_Y
        self.target_color = "yellow"  # Initial target color setting

        # Create GUI window
        self.create_gui()

        # Immediately start scanning
        self.scan()

    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("Adjustments")

        # Create Y offset adjuster
        self.label_y = tk.Label(self.window, text="Y Offset")
        self.label_y.grid(row=0, column=0, padx=10, pady=10)

        self.btn_y_up = tk.Button(self.window, text="▲", command=self.on_y_offset_up)
        self.btn_y_up.grid(row=0, column=1, padx=5)

        self.label_y_value = tk.Label(self.window, text="Y Offset: 0")
        self.label_y_value.grid(row=0, column=2)

        self.btn_y_down = tk.Button(self.window, text="▼", command=self.on_y_offset_down)
        self.btn_y_down.grid(row=0, column=3, padx=5)

        # Create X speed adjuster
        self.label_x = tk.Label(self.window, text="X Speed")
        self.label_x.grid(row=1, column=0, pady=5)

        self.btn_x_up = tk.Button(self.window, text="▲", command=self.on_x_speed_up)
        self.btn_x_up.grid(row=1, column=1, padx=5)

        self.label_x_value = tk.Label(self.window, text="X Speed: 1.0")
        self.label_x_value.grid(row=1, column=2)

        self.btn_x_down = tk.Button(self.window, text="▼", command=self.on_x_speed_down)
        self.btn_x_down.grid(row=1, column=3, padx=5)

        # Create Y speed adjuster
        self.label_y_speed = tk.Label(self.window, text="Y Speed")
        self.label_y_speed.grid(row=2, column=0, pady=5)

        self.btn_y_speed_up = tk.Button(self.window, text="▲", command=self.on_y_speed_up)
        self.btn_y_speed_up.grid(row=2, column=1, padx=5)

        self.label_y_speed_value = tk.Label(self.window, text="Y Speed: 0.4")
        self.label_y_speed_value.grid(row=2, column=2)

        self.btn_y_speed_down = tk.Button(self.window, text="▼", command=self.on_y_speed_down)
        self.btn_y_speed_down.grid(row=2, column=3, padx=5)

        # Create target color selection
        self.label_color = tk.Label(self.window, text="Target Color")
        self.label_color.grid(row=3, column=0, pady=5)

        self.var_target_color = tk.StringVar()
        self.var_target_color.set("yellow")

        self.radio_yellow = tk.Radiobutton(
            self.window,
            text="Yellow",
            variable=self.var_target_color,
            value="yellow",
            command=self.on_color_selection,
        )
        self.radio_yellow.grid(row=3, column=1, columnspan=2, sticky="w")

        self.radio_purple = tk.Radiobutton(
            self.window,
            text="Purple",
            variable=self.var_target_color,
            value="purple",
            command=self.on_color_selection,
        )
        self.radio_purple.grid(row=3, column=1, columnspan=2, sticky="e")

    def on_y_offset_up(self):
        self.y_offset += 1
        self.label_y_value.config(text=f"Y Offset: {self.y_offset}")

    def on_y_offset_down(self):
        self.y_offset -= 1
        self.label_y_value.config(text=f"Y Offset: {self.y_offset}")

    def on_x_speed_up(self):
        self.x_speed += 0.1
        self.label_x_value.config(text=f"X Speed: {self.x_speed:.1f}")

    def on_x_speed_down(self):
        self.x_speed -= 0.1
        self.label_x_value.config(text=f"X Speed: {self.x_speed:.1f}")

    def on_y_speed_up(self):
        self.y_speed += 0.1
        self.label_y_speed_value.config(text=f"Y Speed: {self.y_speed:.1f}")

    def on_y_speed_down(self):
        self.y_speed -= 0.1
        self.label_y_speed_value.config(text=f"Y Speed: {self.y_speed:.1f}")

    def on_color_selection(self):
        self.target_color = self.var_target_color.get()

    def toggle(self):
        self.lock.acquire()
        self.toggled = not self.toggled
        self.lock.release()

    def run(self):
        while True:
            if keyboard.is_pressed("ctrl+alt"):
                self.toggle()
                if self.toggled:
                    print("Enabled")
                    winsound.Beep(440, 75)
                    winsound.Beep(700, 100)
                else:
                    print("Disabled")
                    winsound.Beep(440, 75)
                    winsound.Beep(200, 100)
                while keyboard.is_pressed("ctrl+alt"):
                    pass
            if win32api.GetAsyncKeyState(0x06) < 0 and self.toggled:
                self.scan()
            time.sleep(0.005)

    def scan(self):
        if self.target_color == "yellow":
            lower_hsv = np.array([30, 125, 150])
            upper_hsv = np.array([30, 255, 255])
        elif self.target_color == "purple":
            lower_hsv = np.array([140, 110, 150])
            upper_hsv = np.array([150, 195, 255])
        else:
            return

        hsv = cv2.cvtColor(self.grabber.get_screen(), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=3)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        mid = self.grabber.grabzone / 2

        if len(contours) != 0:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"]) / (random.randint(12, 13) / 10) + self.y_offset
            
            x_movement = (cX - mid) * self.x_speed
            y_movement = (cY - mid) * self.y_speed
            self.mouse.move(x_movement, y_movement)

        # Visualize targets
        if ENABLE_VISUALIZER:
            target_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)  # Define thresh within the same scope
            cv2.drawContours(target_image, contours, -1, (0, 255, 0), 2)

            screen_info = screeninfo.get_monitors()[0]
            screen_width = screen_info.width
            screen_height = screen_info.height

            cv2.namedWindow("Detected Targets", cv2.WINDOW_NORMAL)
            cv2.moveWindow("Detected Targets", screen_info.x, screen_info.y)

            cv2.imshow("Detected Targets", target_image)
            cv2.waitKey(1)

    def close(self):
        self.mouse.ser.close()
        self.toggled = False

    def __del__(self):
        self.close()


def main():
    x = int(SCREEN_WIDTH / 2 - FOV / 2)
    y = int(SCREEN_HEIGHT / 2 - FOV / 2)

    syko_fire = SykoFire(x, y, FOV)

    print("SykoFire is ready!")
    print("Reminder: Make game window Fullscreen")
    print("Reminder: Make enemy Yellow or Purple")
    print("Reminder: Use 'Target Color' setting to choose the target color")

    try:
        syko_fire.window.mainloop()
    except KeyboardInterrupt:
        print("Exiting")
        syko_fire.close()
        del syko_fire
    except:
        syko_fire.close()
        del syko_fire
        raise

if __name__ == "__main__":
    main()
