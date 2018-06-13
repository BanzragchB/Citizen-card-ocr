from PIL import Image
import os

path = "C:/Users/Banzragch/Desktop/Bachelor_Degree_Research_Work/Image_data/"
dirs = os.listdir(path)
basewidth = 800
quality_val = 100
#
# def resize():
#     for item in dirs:
#
#         if os.path.isfile(path + item):
#             img = Image.open(path+item)
#             f, e = os.path.splitext(path + item)
#             wpercent = (basewidth/float(img.size[0]))
#             hsize = int((float(img.size[1])*float(wpercent)))
#             img = img.resize((basewidth,hsize), Image.ANTIALIAS)
#             img.save(f + '_X.jpg', quality = quality_val)
#
# resize()


img = Image.open("C:/Users/Banzragch/Desktop/Bachelor_Degree_Research_Work/Image_data/p4_02.jpg")
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save('C:/Users/Banzragch/Desktop/Bachelor_Degree_Research_Work/Image_data/04_hajuu_2.jpg', quality = quality_val)