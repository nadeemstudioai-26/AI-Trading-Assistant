# ==========================
# AI TRADING ASSISTANT V5
# CLEAN VERSION
# ==========================

import cv2
import datetime
import numpy as np

# ==========================
# CONFIGURATION
# ==========================

ROI_X1 = 100
ROI_Y1 = 200
ROI_X2 = 1130
ROI_Y2 = 720


# ==========================
# LOAD IMAGE
# ==========================

def load_image(path):

    img = cv2.imread(path)

    if img is None:
        print("Image not found")

    return img



# ==========================
# EXTRACT CHART ROI
# ==========================

def extract_chart_roi(img):

    chart = img[
        ROI_Y1:ROI_Y2,
        ROI_X1:ROI_X2
    ]

    return chart
# ==========================
# CREATE CANDLE MASKS
# ==========================

# ==========================
# CREATE CANDLE MASKS
# ==========================

def create_masks(chart):

    hsv = cv2.cvtColor(
        chart,
        cv2.COLOR_BGR2HSV
    )


    # GREEN CANDLES

    lower_green = np.array(
        [45, 60, 60]
    )

    upper_green = np.array(
        [90, 255, 255]
    )


    green_mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )


    # RED CANDLES

    lower_red1 = np.array(
        [0, 70, 70]
    )

    upper_red1 = np.array(
        [15, 255, 255]
    )


    lower_red2 = np.array(
        [170, 70, 70]
    )

    upper_red2 = np.array(
        [180, 255, 255]
    )


    red_mask1 = cv2.inRange(
        hsv,
        lower_red1,
        upper_red1
    )


    red_mask2 = cv2.inRange(
        hsv,
        lower_red2,
        upper_red2
    )


    red_mask = red_mask1 + red_mask2


    return green_mask, red_mask
# ==========================
# FIND CANDLES
# ==========================

def find_candles(mask, color):



    candles = []

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)

        area = cv2.contourArea(contour)


        if area < 20:
            continue


        if 10 <= w <= 60 and 5 <= h <= 120:

            candle = {

                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "color": color,
                "body_size": h

            }

            candles.append(candle)


    return candles
# ==========================
# GET LATEST CANDLE
# ==========================

def get_latest_candle(candles):

    if len(candles) == 0:
        return None


    latest = candles[-1]

    return latest
# ==========================
# GET PREVIOUS CANDLE
# ==========================

def get_previous_candle(candles):

    if len(candles) < 2:
        return None

    return candles[-2]
# ==========================
# TREND DETECTION
# ==========================

def detect_trend(candles):

    if len(candles) < 5:
        return "SIDEWAYS", 0

    last_5 = candles[-5:]

    green = 0
    red = 0

    for candle in last_5:

        if candle["color"] == "GREEN":
            green += 1
        else:
            red += 1

    if green > red:
        strength = int((green / 5) * 100)
        return "UP", strength

    elif red > green:
        strength = int((red / 5) * 100)
        return "DOWN", strength

    else:
        return "SIDEWAYS", 50

# ==========================
# DETECT TWO CANDLE PATTERN
# ==========================

def detect_two_candle_pattern(previous, latest):

    if previous is None or latest is None:
        return "NO DATA"


    prev_color = previous["color"]
    last_color = latest["color"]


    if prev_color == "RED" and last_color == "RED":

        return "Bearish Continuation"


    elif prev_color == "GREEN" and last_color == "GREEN":

        return "Bullish Continuation"


    elif prev_color == "RED" and last_color == "GREEN":

        return "Bullish Reversal"


    elif prev_color == "GREEN" and last_color == "RED":

        return "Bearish Reversal"


    return "NORMAL"

# ==========================
# ADVANCED TREND ANALYSIS
# ==========================

def advanced_trend_analysis(trend, strength):

    if trend == "UP":

        momentum = "BULLISH"
        bias = "BUYERS CONTROL"

    elif trend == "DOWN":

        momentum = "BEARISH"
        bias = "SELLERS CONTROL"

    else:

        momentum = "NEUTRAL"
        bias = "BALANCED"


    if strength >= 80:

        quality = "STRONG"

    elif strength >= 60:

        quality = "MODERATE"

    else:

        quality = "WEAK"


    return momentum, bias, quality
# ==========================
# AI MARKET ANALYSIS
# ==========================

def ai_market_analysis(
        trend,
        strength,
        pattern,
        momentum
    ):

    signal = "WAIT"
    confidence = 50


    # DOWN TREND

    if trend == "DOWN":

        if "Bearish" in pattern and momentum == "BEARISH":

            signal = "SELL"
            confidence += 30


    # UP TREND

    elif trend == "UP":

        if "Bullish" in pattern and momentum == "BULLISH":

            signal = "BUY"
            confidence += 30


    # Strength check

    if strength >= 60:

        confidence += 20


    if confidence > 100:

        confidence = 100


    return signal, confidence
# ==========================
# MAIN
# ==========================

def main():

    print("\n===== AI TRADING ASSISTANT V5 =====")

    img = load_image("quotex_chart.png")

    if img is None:
        return


    chart = extract_chart_roi(img)
    green_mask, red_mask = create_masks(chart)

    green_candles = find_candles(
    green_mask,
    "GREEN"
)


    red_candles = find_candles(
        red_mask,
        "RED"
    )


    all_candles = green_candles + red_candles


    all_candles.sort(
        key=lambda c: c["x"]
    )


    print("\n===== DETECTED CANDLES =====")

    print("Green :", len(green_candles))
    print("Red   :", len(red_candles))
    print("Total :", len(all_candles))

    # ==========================
    # LATEST CANDLE ANALYSIS
    # ==========================

    latest = get_latest_candle(all_candles)


    if latest:

        print("\n===== LATEST CANDLE =====")

        print(
            "Color :",
            latest["color"]
        )

        print(
            "X Position :",
            latest["x"]
        )

        print(
            "Height :",
            latest["h"]
        )


        # ==========================
    # TWO CANDLE ANALYSIS
    # ==========================

    previous = get_previous_candle(all_candles)


    if previous and latest:

        print("\n===== TWO CANDLE ANALYSIS =====")


        print(
            "Previous Candle :",
            previous["color"]
        )


        print(
            "Latest Candle   :",
            latest["color"]
        )


        print(
            "Previous Height :",
            previous["h"]
        )


        print(
            "Latest Height   :",
            latest["h"]
        )


        pattern = detect_two_candle_pattern(
            previous,
            latest
        )

        print(
            "Pattern :",
            pattern
        )
        # ==========================
        # TREND ANALYSIS
        # ==========================

        trend, strength = detect_trend(all_candles)

        print("\n===== TREND ANALYSIS =====")
        print("Trend :", trend)
        print("Strength :", str(strength) + "%")

        # ==========================
        # ADVANCED TREND ANALYSIS
        # ==========================

        momentum, bias, quality = advanced_trend_analysis(
            trend,
            strength
        )

        print("\n===== ADVANCED TREND ANALYSIS =====")
        print("Trend Direction :", trend)
        print("Trend Strength  :", str(strength) + "%")
        print("Momentum        :", momentum)
        print("Market Bias     :", bias)
        print("Trend Quality   :", quality)

        # ==========================
        # AI MARKET ANALYSIS
        # ==========================

        signal, confidence = ai_market_analysis(
            trend,
            strength,
            pattern,
            momentum
        )

        print("\n===== AI MARKET ANALYSIS =====")
        print("Signal :", signal)
        print("Confidence :", str(confidence) + "%")


if __name__ == "__main__":
    main()