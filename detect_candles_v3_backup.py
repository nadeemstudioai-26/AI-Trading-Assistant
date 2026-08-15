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
# ==========================
# Extract Chart ROI
# ==========================
def extract_chart_roi(img):

    chart = img[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]

    return chart
    # ==========================
# Create HSV Masks
# ==========================
def create_masks(chart):

    hsv = cv2.cvtColor(chart, cv2.COLOR_BGR2HSV)

    # Green candle range
    lower_green = np.array([45, 60, 60])
    upper_green = np.array([90, 255, 255])

    # Red candle range (lower hue)
    lower_red1 = np.array([0, 70, 70])
    upper_red1 = np.array([15, 255, 255])

    # Red candle range (upper hue)
    lower_red2 = np.array([170, 70, 70])
    upper_red2 = np.array([180, 255, 255])

    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    return green_mask, red_mask
# ==========================
# Find Candle Contours
# ==========================
# ==========================
# Calculate Candle Wick
# ==========================
    # ==========================
# Real Wick Detection
# ==========================

    # ==========================
# Color Based Wick Detection
# ==========================
# ==========================
# Find Candle Contours
# ==========================
def find_candles(mask, color):

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candles = []

    for contour in contours:

        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)

        print(f"Bounding Box -> W={w}, H={h}, Area={area}")

        if area < 20:
            continue

        if x < 20:
            continue

        if h > 120:
            continue

        if 40 <= w <= 55 and 20 <= h <= 100:

            candles.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "color": color,

            "high": y,
            "low": y + h,

            "body_size": 0,
            "upper_wick": 0,
            "lower_wick": 0
        })

    return candles

# ==========================
# Count Candles
# ==========================
# ==========================
# Calculate Wicks
# ==========================
# ==========================
# Real Wick Detection
# ==========================
# ==========================
# Real Wick Detection
# ==========================
def detect_real_wick(chart, candle):

    x = candle["x"]
    y = candle["y"]
    w = candle["w"]
    h = candle["h"]

    candle_roi = chart[y:y+h, x:x+w]

    if candle_roi.size == 0:
        return candle


    # Convert HSV
    hsv = cv2.cvtColor(candle_roi, cv2.COLOR_BGR2HSV)


    if candle["color"] == "RED":

        lower = np.array([0,70,70])
        upper = np.array([15,255,255])

    else:

        lower = np.array([45,60,60])
        upper = np.array([90,255,255])


    mask = cv2.inRange(hsv, lower, upper)


    points = np.where(mask > 0)
    print(
        "Checking candle:",
        candle["x"],
        "Pixels:",
        len(points[0])
)

    if len(points[0]) > 0:


        top = points[0].min()
        bottom = points[0].max()

        body_top = top + int((bottom - top) * 0.15)
        body_bottom = bottom - int((bottom - top) * 0.15)

        candle["body_top"] = body_top + y
        candle["body_bottom"] = body_bottom + y
        
        print("Wick Detection OK:", candle["x"])

        total_height = bottom - top


        body = int(total_height * 0.7)
        candle["body_size"] = body

        wick = total_height - body


        if wick > 0:

            candle["upper_wick"] = wick // 2
            candle["lower_wick"] = wick - (wick // 2)


        candle["high"] = top + y
        candle["low"] = bottom + y


    return candle
# ==========================
# Print Candle Information
# ==========================
    # ==========================
# Candle Pattern Detection
# ==========================
# ==========================
# Advanced Candle Pattern Detection
# ==========================
def detect_candle_pattern(candle):

    body = candle["body_size"]
    upper = candle["upper_wick"]
    lower = candle["lower_wick"]


    # Doji
    if body <= 10 and upper > 5 and lower > 5:
        return "DOJI"


    # Hammer
    if lower >= body * 2 and upper <= body:
        return "HAMMER"


    # Shooting Star
    if upper >= body * 2 and lower <= body:
        return "SHOOTING STAR"


    return "NORMAL"


# Two Candle Pattern Detection
# ==========================

def detect_two_candle_pattern(previous, latest):

    if (
        previous["color"] == "RED"
        and latest["color"] == "GREEN"
        and latest["body_size"] > previous["body_size"]
    ):
        return "BULLISH ENGULFING"

    if (
        previous["color"] == "GREEN"
        and latest["color"] == "RED"
        and latest["body_size"] > previous["body_size"]
    ):
        return "BEARISH ENGULFING"


    return "NO ENGULFING"

# ==========================
# Support & Resistance
# ==========================
def detect_support_resistance(candles):

    if len(candles) < 5:
        return None, None

    highs = []
    lows = []

    for candle in candles:

        highs.append(candle["high"])
        lows.append(candle["low"])


    resistance = max(highs)
    support = min(lows)


    return support, resistance

    if (
        previous["color"] == "RED"
        and latest["color"] == "GREEN"
        and latest["body_size"] > previous["body_size"]
    ):
        return "BULLISH ENGULFING"


    if (
        previous["color"] == "GREEN"
        and latest["color"] == "RED"
        and latest["body_size"] > previous["body_size"]
    ):
        return "BEARISH ENGULFING"


    return "NO ENGULFING"
    # ==========================
# Trend Strength
# ==========================
def detect_trend_strength(candles):

    if len(candles) < 5:
        return "NOT ENOUGH DATA", 0

    last_five = candles[-5:]

    green = 0
    red = 0

    for candle in last_five:

        if candle["color"] == "GREEN":
            green += 1
        else:
            red += 1

    total = green + red

    if green > red:
        trend = "BULLISH"
        strength = int((green / total) * 100)

    elif red > green:
        trend = "BEARISH"
        strength = int((red / total) * 100)

    else:
        trend = "SIDEWAYS"
        strength = 50

    return trend, strength

    print("Body Top   :", candle.get("body_top", 0))
    print("Body Bottom:", candle.get("body_bottom", 0))

def print_candle_info(candle):
    print("\n==========================")
    print("Color       :", candle["color"])
    print("X Position  :", candle["x"])
    print("Width       :", candle["w"])
    print("Height      :", candle["h"])
    print("Body Size   :", candle["body_size"])
    print("High        :", candle["high"])
    print("Low         :", candle["low"])
    print("Upper Wick  :", candle["upper_wick"])
    print("Lower Wick  :", candle["lower_wick"])
    print("==========================")

def count_candles(green_contours, red_contours):

    green_count = len(green_contours)
    red_count = len(red_contours)

    total_count = green_count + red_count

    return green_count, red_count, total_count
    # ==========================
# Main Function
# ==========================
def main():

    # Load Image
    img = load_image("quotex_chart.png")

    if img is None:
        return

    # Extract Chart
    chart = extract_chart_roi(img)

    # Create Masks
    green_mask, red_mask = create_masks(chart)

    cv2.imshow("Green Mask", green_mask)
    cv2.imshow("Red Mask", red_mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Find Candles
    green_candles = find_candles(green_mask, "GREEN")
    red_candles = find_candles(red_mask, "RED")

    # Merge & Sort
    all_candles = green_candles + red_candles
    all_candles.sort(key=lambda c: c["x"])

    # Detect Real Wick
    for candle in all_candles:
        detect_real_wick(chart, candle)

    # Print All Candles
    print("\nDetected Candle Data:\n")

    for i, candle in enumerate(all_candles):

        print(f"\nCandle {i+1}")
        print_candle_info(candle)

    # Pattern Detection
    if len(all_candles) >= 2:

        previous = all_candles[-2]
        latest = all_candles[-1]

        print("\n===== LATEST CANDLE =====")
        print_candle_info(latest)

        pattern = detect_candle_pattern(latest)
        two_pattern = detect_two_candle_pattern(previous, latest)

        print("Candle Pattern :", pattern)
        print("Two Candle Pattern :", two_pattern)

        print("\n=== Pattern Detection ===")
        print(f"{previous['color']} -> {latest['color']}")

        print("Previous Body :", previous["body_size"])
        print("Latest Body   :", latest["body_size"])

        if latest["body_size"] > previous["body_size"]:
            print("Latest Candle Body : Bigger")
            print("Candle Strength : Strong")

        elif latest["body_size"] < previous["body_size"]:
            print("Latest Candle Body : Smaller")
            print("Candle Strength : Weak")

        else:
            print("Latest Candle Body : Same")
            print("Candle Strength : Neutral")

        if previous["color"] == "RED" and latest["color"] == "RED":
            print("Pattern : Bearish Continuation")

        elif previous["color"] == "GREEN" and latest["color"] == "GREEN":
            print("Pattern : Bullish Continuation")

        elif previous["color"] == "RED" and latest["color"] == "GREEN":
            print("Pattern : Bullish Reversal")

        elif previous["color"] == "GREEN" and latest["color"] == "RED":
            print("Pattern : Bearish Reversal")


    trend, strength = detect_trend_strength(all_candles)

    print("\n===== TREND ANALYSIS =====")
    print("Trend    :", trend)
    print("Strength :", f"{strength}%")

    support, resistance = detect_support_resistance(all_candles)

    print("\n===== MARKET LEVELS =====")
    print("Support    :", support)
    print("Resistance :", resistance)

if __name__ == "__main__":
    main()
