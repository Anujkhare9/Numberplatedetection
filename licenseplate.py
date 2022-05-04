import cv2  # for importing the image
import imutils  # for resizing the image
import pytesseract  # for converting image text to string

# extracting the path where the tesseract path is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# taking in our image and resizing its width
path = r'C:\Users\shria\Downloads\test.jpg'
image = cv2.imread(path)
image = imutils.resize(image, width=400)
cv2.imshow('original image', image)
cv2.waitKey(0)

# converting the image to greyscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("grayed image", gray_image)
cv2.waitKey(0)

# reducing the noise in the image
gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
cv2.imshow("smoothened image", gray_image)
cv2.waitKey(0)

# detecting the edges of the smoothened image
edged = cv2.Canny(gray_image, 30, 200)
cv2.imshow("edged image", edged)
cv2.waitKey(0)

# finding the contours from the edged image
cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1 = image.copy()
cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)
cv2.imshow("contours", image1)
cv2.waitKey(0)

# sorting the identified contours
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
screenCnt = None
image2 = image.copy()
cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)
cv2.imshow("Top 30 contours", image2)
cv2.waitKey(0)

# now we will run a for loop on our contours tp find the best possinle contours of number plate
count = 0
name = 1  # name of our duplicate croped image

for i in cnts:
    perimeter = cv2.arcLength(i, True)
    # perimeter is also used as arclength and we can find directly using arclength function
    approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
    # approxPolyDp we have used because it approximated the curve of number plate with more precsion

    if (len(approx) == 4):  # it means our number plate has 4 corners
        NumberPlateCount = approx
        # now we will crop the rectangle part
        x, y, w, h = cv2.boundingRect(i)
        crp_img = image[y:y + h, x:x + w]
        cv2.imwrite(str(name) + '.png', crp_img)
        name += 1
        break

# now we will draw the contour in our image as number plate
cv2.drawContours(image, [NumberPlateCount], -1, (0, 255, 0), 3)
cv2.imshow("image with detected license plate", image)
cv2.waitKey(0)

# we will crop the only part of our image
crop_img_loc = '1.png'
cv2.imshow("Cropped image", cv2.imread(crop_img_loc))
plate = pytesseract.image_to_string(crop_img_loc, lang='eng')
print("Number Plate IS ", plate)
cv2.waitKey(0)
