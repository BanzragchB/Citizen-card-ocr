# Citizen-card-ocr
The project uses OpenCV, tesseract.
This project uses images to find information of citizen card images was included in image_data folder.

First, you need to install tesseract ocr 3.02.
Tesseract OCR Engine extracts characters from the citizen card.
matching.py is the main python code, the main code starts here.
matching.py does read image, then find the top-left, top-right, bottom-right, bottom-left points. These 4 points used to straighten the object(citizen card).
Next step is searching template from steady image using the template images.
Finally, pass the image found to tesseract, which gives characters and writes to file.
