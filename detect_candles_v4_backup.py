import cv2
import numpy as np
import datetime
import os
# ==========================
# CHART ROI
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
        print("Error: quotex_chart.png not found!")
        return None

    return img
    # ==========================
# EXTRACT CHART ROI
# ==========================

def extract_chart_roi(img):

    chart = img[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]

    return chart
    # ==========================
# CREATE HSV MASKS
# ==========================

def create_masks(chart):

    hsv = cv2.cvtColor(chart, cv2.COLOR_BGR2HSV)

    lower_green = np.array([45,60,60])
    upper_green = np.array([90,255,255])

    lower_red1 = np.array([0,70,70])
    upper_red1 = np.array([15,255,255])

    lower_red2 = np.array([170,70,70])
    upper_red2 = np.array([180,255,255])

    green_mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
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

    red_mask = cv2.bitwise_or(
        red_mask1,
        red_mask2
    )

    return green_mask, red_mask

# ==========================
# FIND CANDLES
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

        if area < 20:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        if x < 20:
            continue

        if h > 120:
            continue

        if not (40 <= w <= 55 and 20 <= h <= 100):
            continue

        candles.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "color": color,
            "body_size": 0,
            "upper_wick": 0,
            "lower_wick": 0,
            "high": y,
            "low": y + h
        })

    return candles
# ==========================
# DETECT REAL WICK
# ==========================

def detect_real_wick(chart, candle):

    x = candle["x"]
    y = candle["y"]
    w = candle["w"]
    h = candle["h"]

    candle_roi = chart[y:y+h, x:x+w]

    if candle_roi.size == 0:
        return candle

    hsv = cv2.cvtColor(candle_roi, cv2.COLOR_BGR2HSV)

    if candle["color"] == "GREEN":
        lower = np.array([45, 60, 60])
        upper = np.array([90, 255, 255])
    else:
        lower = np.array([0, 70, 70])
        upper = np.array([15, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    points = np.where(mask > 0)

    if len(points[0]) == 0:
        return candle

    top = int(points[0].min())
    bottom = int(points[0].max())

    total_height = bottom - top

    candle["high"] = y + top
    candle["low"] = y + bottom

    candle["body_size"] = int(total_height * 0.70)

    wick = total_height - candle["body_size"]

    candle["upper_wick"] = wick // 2
    candle["lower_wick"] = wick - candle["upper_wick"]

    return candle

# ==========================
# PRINT CANDLE INFO
# ==========================

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


        
def main():

    img = load_image("quotex_chart.png")

    if img is None:
        return

    chart = extract_chart_roi(img)

    green_mask, red_mask = create_masks(chart)

    cv2.imshow("Green Mask", green_mask)
    cv2.imshow("Red Mask", red_mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Detect Candles
    green_candles = find_candles(green_mask, "GREEN")
    red_candles = find_candles(red_mask, "RED")

    # Merge & Sort
    all_candles = green_candles + red_candles
    all_candles.sort(key=lambda c: c["x"])

    # Detect Wick
    for candle in all_candles:
        detect_real_wick(chart, candle)

    # Summary
    print("\n===== DETECTED CANDLES =====")
    print("Green :", len(green_candles))
    print("Red   :", len(red_candles))
    print("Total :", len(all_candles))

    # Print All Candles
    for i, candle in enumerate(all_candles, start=1):
        print(f"\nCandle {i}")
        print_candle_info(candle)

    # Latest Candle Pattern
    if len(all_candles) >= 1:

        latest = all_candles[-1]
        if len(all_candles) >= 1:

            latest = all_candles[-1]

        print("\n===== TEST LATEST =====")
        print(latest)

        latest_pattern = detect_candle_pattern(latest)

        print("\n===== TEST LATEST =====")
        print(latest)

        print("\n===== TEST LATEST =====")
        print(latest)

        print("\n===== LATEST CANDLE DATA =====")
        print_candle_info(latest)

        latest_pattern = detect_candle_pattern(latest)

        print("\n===== LATEST CANDLE PATTERN =====")
        print("Pattern :", latest_pattern)

    # Two Candle Analysis
    if len(all_candles) >= 2:

        previous = all_candles[-2]
        latest = all_candles[-1]
        print("\n===== TEST LATEST =====")
        print(latest)

        print("\n===== TWO CANDLE ANALYSIS =====")

        print("Previous Candle :", previous["color"])
        print("Latest Candle   :", latest["color"])

        print("\nPrevious Body :", previous["body_size"])
        print("Latest Body   :", latest["body_size"])

        if latest["body_size"] > previous["body_size"]:
            strength = "Strong"
        else:
            strength = "Weak"

        print("\nCandle Strength :", strength)

        if previous["color"] == "GREEN" and latest["color"] == "GREEN":
            pattern = "Bullish Continuation"

        elif previous["color"] == "RED" and latest["color"] == "RED":
            pattern = "Bearish Continuation"

        elif previous["color"] == "RED" and latest["color"] == "GREEN":
            pattern = "Bullish Reversal"

        elif previous["color"] == "GREEN" and latest["color"] == "RED":
            pattern = "Bearish Reversal"

        else:
            pattern = "NORMAL"

        print("Pattern :", pattern)

        trend, trend_strength = detect_trend(all_candles)
        support, resistance = detect_support_resistance(all_candles)
        breakout_status = detect_breakout(
            latest,
            support,
            resistance
        )

        print("\n===== BREAKOUT ANALYSIS =====")
        print("Status :", breakout_status)


        print("\n===== SUPPORT & RESISTANCE =====")

        print("Support :", support)
        print("Resistance :", resistance)

        
        trend, signal, ai_confidence = ai_signal_engine(
            previous,
            latest,
            pattern,
            strength
        )

        trend, trend_strength = detect_trend(all_candles)


        # Confidence Engine V3
        confidence = calculate_confidence(
            trend_strength,
            pattern,
            strength,
            breakout_status,
            signal
        )

        
        print("\n===== AI TRADE SIGNAL =====")

        print("Trend :", trend)
        print("Trend Strength :", str(trend_strength) + "%")
        print("Pattern :", pattern)
        print("Signal :", signal)
        print("Confidence :", str(confidence) + "%")


    reasons = generate_reason(
        trend,
        trend_strength,
        pattern,
        strength,
        previous,
        latest,
        breakout_status,
        confidence,
        signal
    )

    print("\n===== AI REASONING =====")

    for reason in reasons:
        print(reason)

    action, risk = trading_safety(
        signal,
        confidence,
        latest,
        support,
        resistance,
        breakout_status
    )

    print("\n===== TRADE DECISION =====")

    print("Signal :", signal)
    print("Confidence :", str(confidence) + "%")
    print("Risk Level :", risk)
    print("Action :", action)
    save_trade_journal(
        signal,
        trend,
        trend_strength,
        pattern,
        confidence,
        risk,
        action,
        breakout_status,
        support,
        resistance,
        reasons
    )
# ==========================
# AI TRADING JOURNAL
# ==========================

# ==========================
# AI TRADING JOURNAL V2
# ==========================

    now = datetime.datetime.now()

    with open("trading_journal.txt", "a") as file:

        file.write("\n==========================\n")
        
        file.write(
            f"Time : {now}\n"
        )

        file.write(
            f"Signal : {signal}\n"
        )

        file.write(
            f"Trend : {trend}\n"
        )

        file.write(
            f"Trend Strength : {trend_strength}%\n"
        )

        file.write(
            f"Pattern : {pattern}\n"
        )

        file.write(
            f"Confidence : {confidence}%\n"
        )

        file.write(
            f"Risk Level : {risk}\n"
        )

        file.write(
            f"Action : {action}\n"
        )

        file.write(
            f"Breakout Status : {breakout_status}\n"
        )

        file.write(
            f"Support : {support}\n"
        )

        file.write(
            f"Resistance : {resistance}\n"
        )

        file.write("\nAI Reasoning:\n")

        for reason in reasons:

            file.write(
                f"- {reason}\n"
            )
        file.write("Trade Result : PENDING\n")
        file.write("Profit/Loss : 0\n")


        file.write(
            "==========================\n"
        )
        
        if signal == "SELL":

            print("\nDecision Reason:")
            print("Bearish momentum detected with continuation pattern.")


        elif signal == "BUY":

            print("\nDecision Reason:")
            print("Bullish momentum detected with continuation pattern.")
        
# ==========================
# AI REASONING MODULE
# ==========================

# ==========================
# AI REASONING V2
# ==========================

def generate_reason(
        trend,
        trend_strength,
        pattern,
        strength,
        previous,
        latest,
        breakout_status,
        confidence,
        signal
    ):

    reasons = []


    # Trend

    if trend == "DOWN":

        reasons.append(
            "✓ Down trend confirmed"
        )

    elif trend == "UP":

        reasons.append(
            "✓ Up trend confirmed"
        )

    else:

        reasons.append(
            "✓ Market is sideways"
        )


    reasons.append(
        f"✓ Trend Strength : {trend_strength}%"
    )


    # Pattern

    reasons.append(
        f"✓ Pattern detected : {pattern}"
    )


    # Candle

    reasons.append(
        f"✓ Candle Strength : {strength}"
    )


    # Candle Colors

    reasons.append(
        f"✓ Previous Candle : {previous['color']}"
    )

    reasons.append(
        f"✓ Latest Candle : {latest['color']}"
    )


    # Breakout

    if breakout_status != "NO BREAKOUT":

        reasons.append(
            f"✓ Market Level Reaction : {breakout_status}"
        )


    # Confidence

    reasons.append(
        f"✓ AI Confidence : {confidence}%"
    )


    # Final Signal

    reasons.append(
        f"✓ Final Signal : {signal}"
    )


    return reasons

    reasons = []

    if trend == "DOWN":
        reasons.append("Trend Direction : DOWN")

    elif trend == "UP":
        reasons.append("Trend Direction : UP")

    else:
        reasons.append("Trend Direction : SIDEWAYS")


    reasons.append(
        f"Trend Strength : {trend_strength}%"
    )

    reasons.append(
        f"Pattern : {pattern}"
    )

    reasons.append(
        f"Candle Strength : {strength}"
    )

    reasons.append(
        f"Previous Candle : {previous['color']}"
    )

    reasons.append(
        f"Latest Candle : {latest['color']}"
    )

    return reasons
# ==========================
# TRADING SAFETY LAYER
# ==========================
# ==========================
# TRADING SAFETY V2
# ==========================

def trading_safety(
        signal,
        confidence,
        latest,
        support,
        resistance,
        breakout_status
    ):


    latest_price = latest["low"]


    # ==========================
    # SUPPORT / RESISTANCE FILTER
    # ==========================

    support_distance = abs(latest_price - support)
    resistance_distance = abs(latest_price - resistance)



    # SELL Protection

    if signal == "SELL":

        if support_distance < 30:

            return "NO TRADE - NEAR SUPPORT", "HIGH"



    # BUY Protection

    if signal == "BUY":

        if resistance_distance < 30:

            return "NO TRADE - NEAR RESISTANCE", "HIGH"



    # ==========================
    # BREAKOUT CONFIRMATION
    # ==========================

    if signal == "SELL" and breakout_status == "RESISTANCE REJECTION":

        if confidence >= 75:

            return "TAKE TRADE", "LOW"


    if signal == "BUY" and breakout_status == "SUPPORT BOUNCE":

        if confidence >= 75:

            return "TAKE TRADE", "LOW"



    # ==========================
    # NORMAL CONFIDENCE CHECK
    # ==========================

    if confidence >= 80:

        return "TAKE TRADE", "MEDIUM"


    elif confidence >= 60:

        return "WAIT / CAUTION", "MEDIUM"


    else:

        return "NO TRADE", "HIGH"
# ==========================
# TREND DETECTION MODULE
# ==========================

def detect_trend(candles):

    if len(candles) < 5:
        return "SIDEWAYS", 50

    last_five = candles[-5:]

    green = 0
    red = 0

    for candle in last_five:

        if candle["color"] == "GREEN":
            green += 1

        elif candle["color"] == "RED":
            red += 1


    total = green + red


    if green > red:

        strength = int((green / total) * 100)
        return "UP", strength


    elif red > green:

        strength = int((red / total) * 100)
        return "DOWN", strength


    else:

        return "SIDEWAYS", 50

# ==========================
# SUPPORT & RESISTANCE MODULE
# ==========================
# ==========================
# BREAKOUT DETECTION MODULE
# ==========================

def detect_breakout(
        latest,
        support,
        resistance
    ):

    high = latest["high"]
    low = latest["low"]
    color = latest["color"]


    # Resistance Break
    if high > resistance:

        return "RESISTANCE BREAKOUT"


    # Support Break
    elif low < support:

        return "SUPPORT BREAKDOWN"


    # Resistance Rejection
    elif high == resistance and color == "RED":

        return "RESISTANCE REJECTION"


    # Support Bounce
    elif low == support and color == "GREEN":

        return "SUPPORT BOUNCE"


    else:

        return "NO BREAKOUT"
# ==========================
# SUPPORT & RESISTANCE V2
# ==========================

# ==========================
# SUPPORT & RESISTANCE V3
# ==========================

def detect_support_resistance(candles):

    if len(candles) < 5:
        return None, None


    highs = []
    lows = []


    for candle in candles[-10:]:

        highs.append(candle["high"])
        lows.append(candle["low"])


    resistance = max(highs)
    support = min(lows)


    return support, resistance


    # Recent market area
    recent_highs = highs[-10:]
    recent_lows = lows[-10:]


    resistance = max(recent_highs)
    support = min(recent_lows)


    return support, resistance

# ==========================
# CONFIDENCE ENGINE V2
# ==========================

# ==========================
# CONFIDENCE ENGINE V3
# ==========================

# ==========================
# CONFIDENCE ENGINE V4
# ==========================

# ==========================
# CONFIDENCE ENGINE V5
# ==========================

def calculate_confidence(
        trend_strength,
        pattern,
        candle_strength,
        breakout_status,
        signal
    ):

    score = 0


    # Trend Score (40%)

    trend_score = int(trend_strength * 0.40)

    score += trend_score



    # Pattern Score (25%)

    if pattern == "Bullish Continuation" or pattern == "Bearish Continuation":

        score += 25

    elif pattern == "Bullish Reversal" or pattern == "Bearish Reversal":

        score += 20

    else:

        score += 10



    # Candle Score (15%)

    if candle_strength == "Strong":

        score += 15

    elif candle_strength == "Weak":

        score += 8

    else:

        score += 5



    # Breakout Score (10%)

    if breakout_status in [
        "RESISTANCE REJECTION",
        "SUPPORT BOUNCE",
        "RESISTANCE BREAKOUT",
        "SUPPORT BREAKDOWN"
    ]:

        score += 10

    else:

        score += 5



    # Market Reaction Bonus (10%)

    if signal == "SELL" and breakout_status == "RESISTANCE REJECTION":

        score += 10


    elif signal == "BUY" and breakout_status == "SUPPORT BOUNCE":

        score += 10


    else:

        score += 5



    return score    

    score = 0


    # Trend Score (40%)
    trend_score = int(trend_strength * 0.40)

    score += trend_score


    # Pattern Score (40%)
    if pattern == "Bullish Continuation" or pattern == "Bearish Continuation":

        score += 40


    elif pattern == "Bullish Reversal" or pattern == "Bearish Reversal":

        score += 30


    else:

        score += 20



    # Candle Strength Score (20%)

    if candle_strength == "Strong":

        score += 20

    elif candle_strength == "Weak":

        score += 10

    else:

        score += 5



    return score
               
# ==========================
# AI SIGNAL ENGINE
# ==========================

def ai_signal_engine(previous, latest, pattern, strength):

    trend = "SIDEWAYS"
    signal = "HOLD"
    confidence = 50

    # Bearish Condition
    if pattern == "Bearish Continuation":

        trend = "DOWN"
        signal = "SELL"

        if strength == "Strong":
            confidence = 85
        else:
            confidence = 85


    # Bullish Condition
    elif pattern == "Bullish Continuation":

        trend = "UP"
        signal = "BUY"

        if strength == "Strong":
            confidence = 85
        else:
            confidence = 70


    # Reversal Conditions

    elif pattern == "Bullish Reversal":

        trend = "UP"
        signal = "BUY"
        confidence = 60


    elif pattern == "Bearish Reversal":

        trend = "DOWN"
        signal = "SELL"
        confidence = 60


    return trend, signal, confidence

# ==========================
# SINGLE CANDLE PATTERN
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
def save_trade_journal(
        signal,
        trend,
        trend_strength,
        pattern,
        confidence,
        risk,
        action,
        breakout_status,
        support,
        resistance,
        reasons
    ):

if __name__ == "__main__":
    main()