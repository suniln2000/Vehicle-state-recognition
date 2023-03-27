import cv2
import pytesseract
import imutils
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Define the state codes and their corresponding state names
states = {
    'AP': 'Andhra Pradesh','AR': 'Arunachal Pradesh','AS': 'Assam','BR': 'Bihar','CT': 'Chhattisgarh','GA': 'Goa',
    'GJ': 'Gujarat','HR': 'Haryana','HP': 'Himachal Pradesh','JK': 'Jammu and Kashmir','JH': 'Jharkhand','KA': 'Karnataka',
    'KL': 'Kerala','MP': 'Madhya Pradesh','MH': 'Maharashtra','MN': 'Manipur','ML': 'Meghalaya','MZ': 'Mizoram',
    'NL': 'Nagaland','OD': 'Odisha','PB': 'Punjab','RJ': 'Rajasthan','SK': 'Sikkim','TN': 'Tamil Nadu','TS': 'Telangana',
    'TR': 'Tripura','UK': 'Uttarakhand','UP': 'Uttar Pradesh','WB': 'West Bengal','DL': 'Delhi'
}

# Create a file dialog to select an image
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Image files", "*.jpg"), ("all files", "*.*")))


# Load the input image
image = cv2.imread(file_path)
image = imutils.resize(image, width=500)

# Convert the image to grayscale and apply bilateral filtering
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Detect edges using Canny edge detection
edge = cv2.Canny(gray, 170, 200)

# Find contours in the edge map
cnts, new = cv2.findContours(edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Draw the contours on a copy of the input image
image1 = image.copy()
cv2.drawContours(image1, cnts, -1, (0, 225, 0), 3)

# Select the 30 largest contours
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]

NumberPlateCount = None

# Draw the 30 largest contours on another copy of the input image
image2 = image.copy()
cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)

# Iterate over the contours and select the one with 4 corners as the number plate
for i in cnts:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
    if len(approx) == 4:
        NumberPlateCount = approx
        x, y, w, h = cv2.boundingRect(i)
        crp_img = image[y:y + h, x:x + w]
        cv2.imwrite("cropped_image.png", crp_img)
        break

# If a number plate is found, perform OCR on the cropped image
if NumberPlateCount is not None:
    cv2.drawContours(image, [NumberPlateCount], -1, (0, 255, 0), 3)
    cv2.imshow("Number Plate Detected", image)
    text = pytesseract.image_to_string("cropped_image.png", lang="eng")
    print("Number is: " + text)
    
    # Extract the state code from the number plate text
    state_code = text[:2]
    state_name = states.get(state_code, "Unknown")
    print("State is: " + state_name)
    
    cv2.imshow("Cropped Image", cv2.imread("cropped_image.png"))
    cv2.waitKey(0)
else:
    print("No number plate detected.")
