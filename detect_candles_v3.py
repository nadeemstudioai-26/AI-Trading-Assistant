import cv2
import numpy as np

# ==========================
# Chart ROI
# ==========================
ROI_X1 = 100
ROI_Y1 = 200
ROI_X2 = 1130
ROI_Y2 = 720

# ==========================
# Load Image
# ==========================
def load_image(path):

    img = cv2.imread(path)

    if img is None:
        print("Error: quotex_chart.png not found!")
        return None

    return img


# ==========================
# Extract Chart ROI
# ==========================
def extract_chart_roi(img):

    chart = img[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]

    return chart
    
    img = cv2.imread(path)

    if img is None:
        print("Error: quotex_chart.png not found!")
        return None

    return img
# ==========================
# Create Green & Red Masks
# ==========================
def create_masks(img):

# ==========================
# Find Candles
# ==========================
def find_candles(mask, img, color_name, box_color):

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candles = []

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 20:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        # Filter real candle bodies
        if 40 <= w <= 55 and 4 <= h <= 100:

            candle = {
                "color": color_name,
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "center_x": x + (w // 2),
                "center_y": y + (h // 2),
                "body_width": w,
                "body_height": h
            }

            candles.append(candle)

            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                box_color,
                2
            )

    return candles
    # ==========================
# Count Candles
# ==========================
def count_candles(candles):
    return len(candles)


# ==========================
# Detect Trend
# ==========================
def detect_trend(green_count, red_count):

    if green_count > red_count:
        return "UP"

    elif red_count > green_count:
        return "DOWN"

    return "SIDEWAYS"


# ==========================
# Sort Candles
# ==========================
def sort_candles(candles):

    return sorted(
        candles,
        key=lambda candle: candle["x"]
    )
    # ==========================
# Latest Candle
# ==========================
def get_latest_candle(candles):

    if not candles:
        return None

    candles = sort_candles(candles)

    return candles[-1]


# ==========================
# Previous Candle
# ==========================
def get_previous_candle(candles):
    # ==========================
# Main Function
# ==========================
def main():

    # Load Image
    img = load_image("quotex_chart.png")

    if img is None:
        return

    # Extract Chart ROI
    chart = extract_chart_roi(img)

    # Create Masks
    green_mask, red_mask = create_masks(chart)

    # Detect Candles
    green_candles = find_candles(
        green_mask,
        chart,
        "GREEN",
        (0, 255, 0)
    )

    red_candles = find_candles(
        red_mask,
        chart,
        "RED",
        (0, 0, 255)
    )

    # Count Candles
    green_count = count_candles(green_candles)
    red_count = count_candles(red_candles)

    # Detect Trend
    trend = detect_trend(green_count, red_count)

    # Combine All Candles
    all_candles = green_candles + red_candles

    latest = get_latest_candle(all_candles)
    previous = get_previous_candle(all_candles)

    print("Green Candles:", green_count)
    print("Red Candles:", red_count)

    print("\nPrevious Candle")
    print(previous)

    print("\nLatest Candle")
    print(latest)

    print("\nCurrent Trend:", trend)

    # Show Result
    cv2.imshow("Detected Candles", chart)
    cv2.imshow("Green Mask", green_mask)
    cv2.imshow("Red Mask", red_mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(candles) < 2:
        return None

    candles = sort_candles(candles)

    return candles[-2]

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Green Range
    lower_green = np.array([45, 60, 60])
    upper_green = np.array([90, 255, 255])

    # Red Range
    lower_red1 = np.array([0, 70, 70])
    upper_red1 = np.array([15, 255, 255])

    lower_red2 = np.array([170, 70, 70])
    upper_red2 = np.array([180, 255, 255])

    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # Noise Reduction
    kernel = np.ones((3, 3), np.uint8)

    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)

    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    return green_mask, red_mask
    # ==========================
# Start Program
# ==========================
if __name__ == "__main__":
    main()