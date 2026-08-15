import cv2
import numpy as np
import mss

with mss.mss() as sct:

    monitor = {
        "top": 120,
        "left": 70,
        "width": 1060,
        "height": 600
    }

    while True:

        screenshot = sct.grab(monitor)

        img = np.array(screenshot)

        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        cv2.imshow("Live Quotex Chart", img)

        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()