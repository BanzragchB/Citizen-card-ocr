from PIL import Image
import os

path = "image_path_here"
dirs = os.listdir(path)
basewidth = 800
quality_val = 100

#Looping the all image in the dirs resize all the images
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


img = Image.open(path)
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save('path_here', quality = quality_val)
