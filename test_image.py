import cv2

img = cv2.imread("quotex_chart.png")

if img is None:
    print("Image load nahi hui!")
else:
    print("Image successfully load ho gai.")
    print("Image Size:", img.shape)

    cv2.imshow("Chart", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
