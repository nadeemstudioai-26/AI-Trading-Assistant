import cv2
import numpy as np

# Image Load
img = cv2.imread("quotex_chart.png")

if img is None:
    print("Error: quotex_chart.png not found!")
    exit()

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# ==========================
# GREEN RANGE
# ==========================
lower_green = np.array([45, 60, 60])
upper_green = np.array([90, 255, 255])

# ==========================
# RED RANGE
# ==========================
lower_red1 = np.array([0, 70, 70])
upper_red1 = np.array([15, 255, 255])

lower_red2 = np.array([170, 70, 70])
upper_red2 = np.array([180, 255, 255])

# Create Masks
green_mask = cv2.inRange(hsv, lower_green, upper_green)

red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

red_mask = cv2.bitwise_or(red_mask1, red_mask2)

# Remove Noise
kernel = np.ones((3,3), np.uint8)

green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)

red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

# Show Results

# Find Green Candle Contours
green_contours, _ = cv2.findContours(
    green_mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

for cnt in green_contours:
    x, y, w, h = cv2.boundingRect(cnt)

    if w > 5 and h > 5:   # چھوٹے Noise کو Ignore کریں
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

# Find Red Candle Contours
red_contours, _ = cv2.findContours(
    red_mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

for cnt in red_contours:
    x, y, w, h = cv2.boundingRect(cnt)

    if w > 5 and h > 5:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
green_count = 0

for cnt in green_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 5 and h > 5:
        green_count += 1

red_count = 0

for cnt in red_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 5 and h > 5:
        red_count += 1

print("Green Candles:", green_count)
print("Red Candles:", red_count)
if green_count > red_count:
    trend = "UP"
elif red_count > green_count:
    trend = "DOWN"
else:
    trend = "SIDEWAYS"

print("Current Trend:", trend)
cv2.putText(
    img,
    "Trend: " + trend,
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 255, 255),
    2
)
cv2.imshow("Detected Candles", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
# Show Final Result
cv2.imshow("Detected Candles", img)
cv2.imshow("Green Mask", green_mask)
cv2.imshow("Red Mask", red_mask)

cv2.waitKey(0)
cv2.destroyAllWindows()