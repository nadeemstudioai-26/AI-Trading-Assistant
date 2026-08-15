import cv2

img = cv2.imread("quotex_chart.png")

if img is None:
    print("Image load nahi hui!")
    exit()

print("Image Size:", img.shape)

# Mouse coordinates
def mouse(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        temp = img.copy()
        cv2.putText(temp, f"X:{x}  Y:{y}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.imshow("Chart Detector", temp)

cv2.namedWindow("Chart Detector")
cv2.setMouseCallback("Chart Detector", mouse)

cv2.imshow("Chart Detector", img)
cv2.waitKey(0)
cv2.destroyAllWindows()