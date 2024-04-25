# fyi you will need to install the pillow module
# pip install pillow

from PIL import Image
import sys
import os
try:
    file = sys.argv[1]
except:
    print("Please specify the file to be used...")
    quit(1)
scriptpath = os.path.dirname(__file__)
if os.path.dirname(file) == "":
    file = scriptpath + "/" + file
def ConvertRGB(num):
    value = hex(num).split('x')[-1].upper()
    if len(value) == 1:
        value = "0" + value
    return value
valid = [False, False]
exts = ['.ras', '.ps', '.im', '.tif', '.hdf', '.eps', '.jpg', '.icb', '.dds', '.bmp', '.msp', '.rgb', '.wmf', '.mpeg', '.h5', '.emf', '.blp', '.pcd', '.dcx', '.ftu', '.fit', '.pcx', '.jpeg', '.j2c', '.jpx', '.pxr', '.vda', '.gbr', '.pbm', '.cur', '.sgi', '.webp', '.qoi', '.jpf', '.pnm', '.pfm', '.vst', '.rgba', '.tga', '.jpe', '.pgm', '.xpm', '.png', '.psd', '.dib', '.j2k', '.icns', '.ftc', '.tiff', '.bw', '.ico', '.jpc', '.jfif', '.bufr', '.mpg', '.ppm', '.xbm', '.fli', '.flc', '.iim', '.jp2', '.apng', '.gif', '.fits', '.grib']
for extension in exts:
    if os.path.basename(file).endswith(extension):
        valid[1] = True
        
valid[0] = os.path.isfile(file)
if not valid[0]:
    print("File does not exist!")
    quit(1)
if not valid[1]:
    print("Invalid filetype!")
    quit(1)
try:
    im2 = Image.open(file)
except:
    print("Something went wrong when opening the image. Perhaps it's corrupted?")
    quit(1)
im = im2.convert("RGBA")
width, height = im.size
if height > 512 or width > 512:
    print("Image too big! Input one up to 512*512px.")
    quit(1)
colors = im.getcolors()
print("Found " + str(len(colors)) + " color(s).")
print("Writing header...")
palfile = """/*
 ************************
 *     PALETTE INFO     *
 ************************
*/

typedef Uint32 Palette;"""
palfile += "\n//Palette generated from " + os.path.basename(file)
for index, color in enumerate(colors):
    print("Writing color " + str(index + 1))
    redvalue = ConvertRGB(color[1][0])
    bluevalue = ConvertRGB(color[1][1])
    greenvalue = ConvertRGB(color[1][2])
    alphavalue = ConvertRGB(color[1][3])
    val = "0x" + redvalue + bluevalue + greenvalue + alphavalue
    final = "const Palette PAL" + ConvertRGB(index) + " = {" + val + "};"
    palfile += "\n" + final
f = open(os.path.dirname(file) + "/" "palette.c","w+")
f.write(palfile)
f.close()
print("Wrote palette to file palette.c")
