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
def extract_chart_roi(img):
    chart = img[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]
    return chart

# ==========================
# Create Green & Red Masks
# ==========================
def create_masks(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Green Range
    lower_green = np.array([45, 60, 60])
    upper_green = np.array([90, 255, 255])

    # Red Range
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
    green_mask = cv2.morphologyEx(
    green_mask,
    cv2.MORPH_CLOSE,
    kernel
)

    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)

    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    return green_mask, red_mask
    # ======================================
# Find Candles
# ======================================

def find_candles(mask, img, color_name, box_color):

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    print(f"\n{color_name} Contours Found: {len(contours)}")

    candles = []

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 20:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        print(f"Area={area:.1f}  x={x}  y={y}  w={w}  h={h}")

        if 40 <= w <= 55 and 4 <= h <= 100:

            candles.append({
                "color": color_name,
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "center_x": x + (w // 2),
                "center_y": y + (h // 2),
                "body_height": h,
                "body_width": w,
                "upper_wick": 0,
                "lower_wick": 0
            })

            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                box_color,
                2
            )

    return candles


# ======================================
# Count Candles
# ======================================

def count_candles(candles):
    return len(candles)


# ======================================
# Detect Trend
# ======================================

def detect_trend(green_count, red_count):

    if green_count > red_count:
        return "UP"

    elif red_count > green_count:
        return "DOWN"

    else:
        return "SIDEWAYS"
        # ======================================
# Sort Candles Left to Right
# ======================================

def sort_candles(candles):

    return sorted(
        candles,
        key=lambda candle: candle["x"]
    )
# ======================================
# Get Latest Candle
# ======================================

def get_latest_candle(candles):

    if len(candles) == 0:
        return None

    candles = sort_candles(candles)

    return candles[-1]


# ======================================
# Get Previous Candle
# ======================================

def get_previous_candle(candles):

    if len(candles) < 2:
        return None

    candles = sort_candles(candles)

    return candles[-2]

    if len(candles) == 0:
        return None

    candles = sort_candles(candles)

    return candles[-1]

# ======================================
# Main Function
# ======================================

def main():

    # Load Image
    img = load_image("quotex_chart.png")

    if img is None:
        return

    # Extract Chart ROI
    chart = extract_chart_roi(img)

    # Save ROI for debugging
    cv2.imwrite("chart_roi.png", chart)

    # Create Masks
    green_mask, red_mask = create_masks(chart)

    # Detect Candles
    green_candles = find_candles(
        
        green_mask,
        chart,
        "GREEN",
        (0, 255, 0)
    )
def calculate_wicks(mask, candle):
    print("calculate_wicks called")

        x = candle["x"]
        y = candle["y"]
        w = candle["w"]
        h = candle["h"]

        roi = mask[y:y+h, x:x+w]

        points = cv2.findNonZero(roi)

        if points is None:
            return candle

        top = points[:, 0, 1].min()
        bottom = points[:, 0, 1].max()

        candle["high"] = y + top
        candle["low"] = y + bottom

        candle["upper_wick"] = top
        candle["lower_wick"] = (h - 1) - bottom

        return candle

    red_candles = find_candles(
        red_mask,
        chart,
        "RED",
        (0, 0, 255)
    )
    for candle in green_candles:
        calculate_wicks(green_mask, candle)
        

    for candle in red_candles:
        calculate_wicks(red_mask, candle)
    # Count Candles
    green_count = count_candles(green_candles)
    red_count = count_candles(red_candles)

    print("Green Candles:", green_count)
    print("Red Candles:", red_count)

    # Detect Trend
    trend = detect_trend(green_count, red_count)

    # Combine All Candles
    all_candles = green_candles + red_candles

    latest = get_latest_candle(all_candles)
    previous = get_previous_candle(all_candles)

    print("\nPrevious Candle")
    print(previous)

    print("\nLatest Candle")
    print(latest)
    if latest:

        print("\nHigh:", latest["high"])
        print("Low:", latest["low"])
        print("Upper Wick:", latest["upper_wick"])
        print("Lower Wick:", latest["lower_wick"])

    print("\nCurrent Trend:", trend)
    

    # Show Trend
    cv2.putText(
        chart,
        "Trend: " + trend,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # Show Images
    cv2.imshow("Detected Candles", chart)
    cv2.imshow("Green Mask", green_mask)
    cv2.imshow("Red Mask", red_mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # ======================================
# Start Program
# ======================================

if __name__ == "__main__":
    main()
    