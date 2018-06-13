import cv2
import os
from PIL import Image
import numpy as np
import functions
import re

class Template:
    txt_value = []
    img_rbg = ""
    img_gray = ""
    img_canny = ""
    tW = None
    tH = None
    cnts = 0
    startX = 0
    startY = 0
    endX = 0
    endY = 0

    def __init__(self):
        self.img_rbg = ""
        self.img_canny = ""
        self.tW = 0
        self.tH = 0


template_names = []
template_dir = "templates/"

# Detect image
img = cv2.imread('D:/Bachelor_Degree_Research_Work/Image_data/01_hajuu.jpg')

r = 800.0 / img.shape[1]
dim = (800, int(img.shape[0] * r))
img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (11, 11), 0)
edge = cv2.Canny(gray, 60, 200)
_, contours, _ = cv2.findContours(edge.copy(), 1, 1)
# cv2.drawContours(img, contours, -1, [0, 255, 0], 2)
# cv2.imshow('Contours', img)
n = len(contours)
max_area = 0
pos = 0

for i in contours:
    area = cv2.contourArea(i)
    if area > max_area:
        max_area = area
        pos = i
peri = cv2.arcLength(pos, True)
approx = cv2.approxPolyDP(pos, 0.02 * peri, True)

size = img.shape
w, h, arr = functions.transform(approx)
image_w = 660
image_h = 400
pts2 = np.float32([[0, 0], [image_w, 0], [0, image_h], [image_w, image_h]])
pts1 = np.float32(arr)
M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (image_w, image_h))
# image = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
# image=cv2.adaptiveThreshold(image,255,1,0,11,2)
image = cv2.resize(dst, (image_w, image_h), interpolation=cv2.INTER_AREA)
cv2.imwrite("edged.jpg", image)


def percentage(part, whole):
    return 100 * float(part) / float(whole)


# [0] - dob     [1] - faname        [2] - fname     [3] - lname     [4] - rno       [5] - sex
template_names = functions.get_template_names(template_dir)

#FAMILY NAME
faname = Template()
faname.img_rbg = cv2.imread(template_dir + template_names[1])
faname.img_gray = cv2.cvtColor(faname.img_rbg, cv2.COLOR_BGR2GRAY)
faname.img_canny = cv2.Canny(faname.img_gray, 50, 200)

functions.create_de_noised_png(image, template_names[1], faname.startY, faname.endY, faname.startX, faname.endX, image_w, image_h)

faname.txt_value = functions.getText("info/" + template_names[1], "mon")
print("Овог: " + faname.txt_value.replace(" ",""))

# FIRST NAME
fname = Template()
fname.img_rbg = cv2.imread(template_dir + template_names[2])
fname.img_gray = cv2.cvtColor(fname.img_rbg, cv2.COLOR_BGR2GRAY)
fname.img_canny = cv2.Canny(fname.img_gray, 50, 200)

functions.create_de_noised_png(image, template_names[2], fname.startY, fname.endY, fname.startX, fname.endX, image_w, image_h)

fname.txt_value = functions.getText("info/" + template_names[2], "mon")
print("Эцэг/эх/-ийн нэр: " + fname.txt_value.replace(" ",""))


# LAST NAME
lname = Template()
lname.img_rbg = cv2.imread(template_dir + template_names[3])
lname.img_gray = cv2.cvtColor(lname.img_rbg, cv2.COLOR_BGR2GRAY)
lname.img_canny = cv2.Canny(lname.img_gray, 50, 200)

functions.create_de_noised_png(image, template_names[3], lname.startY, lname.endY, lname.startX, lname.endX, image_w, image_h)

lname.txt_value = functions.getText("info/" + template_names[3], "mon")
print("Нэр: " + lname.txt_value.replace(" ",""))


#DATE OF BIRTH
dob = Template()
dob.img_rbg = cv2.imread(template_dir + template_names[0])
dob.img_gray = cv2.cvtColor(dob.img_rbg, cv2.COLOR_BGR2GRAY)
dob.img_canny = cv2.Canny(dob.img_gray, 50, 200)

functions.create_de_noised_png(image, template_names[0], dob.startY, dob.endY, dob.startX, dob.endX, image_w, image_h)

dob.txt_value = functions.getText("info/" + template_names[0], "eng")
print("Төрсөн он сар өдөр: " + dob.txt_value.replace(" ",""))


# SSNO
ssno = Template()
ssno.img_rbg = cv2.imread(template_dir + template_names[4])
ssno.img_gray = cv2.cvtColor(ssno.img_rbg, cv2.COLOR_BGR2GRAY)
ssno.img_canny = cv2.Canny(ssno.img_gray, 50, 200)

functions.create_de_noised_png(image, template_names[4], ssno.startY, ssno.endY, ssno.startX, ssno.endX, image_w, image_h)

ssno.txt_value = functions.getText("info/" + template_names[4], "mon")
ssno.txt_value = ssno.txt_value[:11]
pattern = re.compile("^([A-Z][A-Z][0-9]+)")
pattern.match(ssno.txt_value)
print("Регистрийн дугаар: " + ssno.txt_value.replace("",""))


text_file = open("Output.txt", "w",encoding='utf-8')
text_file.write("Овог: " + faname.txt_value + "\nЭцэг/эх/-ийн нэр: " + fname.txt_value +
                "\nНэр: " + lname.txt_value.replace(" ","") + "\nТөрсөн он сар өдөр: " + dob.txt_value + "\nРегистрийн дугаар: " + ssno.txt_value)
text_file.close()

cv2.imshow('INPUT', img)
cv2.imshow('OUTPUT', image)
cv2.waitKey(0)
