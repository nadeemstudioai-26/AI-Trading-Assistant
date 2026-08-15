import mss
import cv2
import numpy as np
import time

print("5 seconds me screenshot liya jayega...")
time.sleep(5)

with mss.mss() as sct:
    monitor = sct.monitors[1]

    screenshot = sct.grab(monitor)

    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    cv2.imwrite("quotex_chart.png", img)

print("Screenshot saved as quotex_chart.png")
