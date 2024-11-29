import cv2
import pandas as pd

cap = cv2.VideoCapture(0)

cap.set(3, 720)
cap.set(4, 1280)

b = g = r = 0

def drawSquare(img, x, y):
    YELLOW = (0, 255, 255)
    BLUE = (255, 225, 0)

    cv2.line(img, (x - 150, y - 150), (x - 100, y - 150), YELLOW, 2)
    cv2.line(img, (x - 150, y - 150), (x - 150, y - 100), BLUE, 2)
    
    cv2.line(img, (x + 150, y - 150), (x + 100, y - 150), YELLOW, 2)
    cv2.line(img, (x + 150, y - 150), (x + 150, y - 100), BLUE, 2)
    
    cv2.line(img, (x + 150, y + 150), (x + 100, y + 150), YELLOW, 2)
    cv2.line(img, (x + 150, y + 150), (x + 150, y + 100), BLUE, 2)

    cv2.line(img, (x - 150, y + 150), (x - 100, y + 150), YELLOW, 2)
    cv2.line(img, (x - 150, y + 150), (x - 150, y + 100), BLUE, 2)

    cv2.circle(img, (x, y), 5, (255, 255, 153), -1)

# Reading the csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv("colors.csv", names=index, header=None)

# Function get BGR values from camera
def getBGR(x, y):
    global b, g, r
    b, g, r = img[y, x]
    b, g, r = int(b), int(g), int(r)
    return b, g, r

# Function to calculate minimum distance fromm all color and return the most matching color
def getColorName(b, g, r):
    minimum = 1000 
    for i in range(len(csv)):
        d = abs(b - int(csv.loc[i, "B"])) + abs(g - int(csv.loc[i, "G"])) + abs(r - int(csv.loc[i, "R"])) # maximum = 255 + 255 + 255 = 765 (d = ||b-B|| + ||g-G|| + ||r-R||)
        if (d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    # print(minimum)
    return cname

# Put text on the image
def putText(img, x, y):
    cv2.rectangle(img, (x - 150, y - 220), (x + 300, y - 170), (b,g,r), -1)
    text = getColorName(b, g, r) + " | R=" + str(r) + " G=" + str(g) + " B=" + str(b)
    cv2.putText(img, text, (x - 140, y - 190), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)


while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    x, y = int(img.shape[1]/2), int(img.shape[0]/2)
    # print(x, y)
    getBGR(x, y)
    getColorName(b, g, r)
    drawSquare(img, x, y)
    putText(img, x, y)
    cv2.imshow('Detector Color', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break