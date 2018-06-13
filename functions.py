import cv2
import pytesseract
from PIL import Image
import os
import numpy as np
import re

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

def transform(pos):

    pts = []
    n = len(pos)
    for i in range(n):
        pts.append(list(pos[i][0]))

    sums = {}
    diffs = {}
    tl = tr = bl = br = 0
    for i in pts:
        x = i[0]
        y = i[1]
        sum = x + y
        diff = y - x
        sums[sum] = i
        diffs[diff] = i
    sums = sorted(sums.items())
    diffs = sorted(diffs.items())
    n = len(sums)
    rect = [sums[0][1], diffs[0][1], diffs[n - 1][1], sums[n - 1][1]]
    #      top-left   top-right   bottom-left   bottom-right

    h1 = np.sqrt((rect[0][0] - rect[2][0]) ** 2 + (rect[0][1] - rect[2][1]) ** 2)  # height of left side
    h2 = np.sqrt((rect[1][0] - rect[3][0]) ** 2 + (rect[1][1] - rect[3][1]) ** 2)  # height of right side
    h = max(h1, h2)

    w1 = np.sqrt((rect[0][0] - rect[1][0]) ** 2 + (rect[0][1] - rect[1][1]) ** 2)  # width of upper side
    w2 = np.sqrt((rect[2][0] - rect[3][0]) ** 2 + (rect[2][1] - rect[3][1]) ** 2)  # width of lower side
    w = max(w1, w2)

    return int(w), int(h), rect


def get_template_names(temp_dir):
    temp = []
    for file in os.listdir(temp_dir):
        if os.path.isfile(os.path.join(temp_dir, file)):
            temp.append(file)
    return temp


def get_tH_tW(template):
    (tH, tW) = template.shape[:2]
    return tH, tW


def part(percent, whole):
    return (percent * whole) / 100.0


# def get_points_of_templates(canny, gray, tH, tW):
#     found = None
#     for scale in np.linspace(0.2, 1.0, 20)[::-1]:
#         resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
#         r = gray.shape[1] / float(resized.shape[1])
#
#         if resized.shape[0] < tH or resized.shape[1] < tW:
#             break
#         edged = cv2.Canny(resized, 50, 200)
#         result = cv2.matchTemplate(edged, canny, cv2.TM_CCOEFF)
#         (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
#
#         if found is None or maxVal > found[0]:
#             found = (maxVal, maxLoc, r)
#
#     (_, maxLoc, r) = found
#     (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
#     (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
#     (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     print(startY, endY, startX, endX)
#     return startY, startX, endY, endX, cnts


def create_de_noised_png(image, template_name, startY, endY, startX, endX, width, height):
    if template_name == "template_dob.PNG":
        startX = int(part(25, width))
        endX = int(part(45, width))
        startY = int(part(79, height))
        endY = int(part(84, height))

    elif template_name == "template_rno.PNG":

        startX = int(part(22, width))
        endX = int(part(70, width))
        startY = int(part(90, height))
        endY = int(part(96, height))

    elif template_name == "template_fname.PNG":

        startX = int(part(25, width))
        endX = int(part(50, width))
        startY = int(part(36, height))
        endY = int(part(40, height))

    elif template_name == "template_lname.PNG":
        startX = int(part(25, width))
        endX = int(part(55, width))
        startY = int(part(51, height))
        endY = int(part(55, height))


    elif template_name == "template_faname.PNG":
        startX = int(part(25, width))
        endX = int(part(50, width))
        startY = int(part(20, height))
        endY = int(part(25, height))

    img = image[startY:endY, startX:endX]
    # de_noised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    cv2.imwrite("info/" + template_name,img)


def getText(img_path, lang):
    image = Image.open(img_path)
    result = pytesseract.image_to_string(image, lang=lang)
    return result


def checkRegex(template):

    if template == "faname" or template == "fname" or template == "lname":
        return
    if template == "ssno":
        return
    if template == "dob":
        pattern = re.compile("^([0-9]+)+$")
        if pattern.match(template):
            return

# def changeLetters(template, str):
#
#      if template == "ssno"