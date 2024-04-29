# fyi you will need to install the pillow module
# pip install pillow

from PIL import Image
import argparse
import os

def convert_rgb(num):
    value = hex(num)[2:].upper()
    if len(value) == 1:
        value = "0" + value
    return value

def main():
    parser = argparse.ArgumentParser(description='Convert an image to palette format.')
    parser.add_argument('image', type=str, help='Path to the image file')
    args = parser.parse_args()

    file = os.path.abspath(args.image)

    if not os.path.isfile(file):
        print("File does not exist!")
        return

    valid_extension = False
    valid_filetype = False
    for extension in exts:
        if file.lower().endswith(extension):
            valid_extension = True
            break

    if not valid_extension:
        print("Invalid filetype!")
        return

    try:
        im = Image.open(file)
        im = im.convert("RGBA")
    except Exception as e:
        print("Something went wrong when opening the image:", e)
        return

    width, height = im.size
    if height > 512 or width > 512:
        print("Image too big! Input one up to 512*512px.")
        return

    colors = im.getcolors()
    print("Found", len(colors), "color(s).")
    print("Writing header...")
    palfile = """/*
     ************************
     *     PALETTE INFO     *
     ************************
    */

    typedef Uint32 Palette;"""
    palfile += "\n//Palette generated from " + os.path.basename(file)

    for index, color in enumerate(colors):
        print("Writing color", index + 1)
        redvalue = convert_rgb(color[1][0])
        bluevalue = convert_rgb(color[1][1])
        greenvalue = convert_rgb(color[1][2])
        alphavalue = convert_rgb(color[1][3])
        val = "0x" + redvalue + bluevalue + greenvalue + alphavalue
        final = "const Palette PAL" + convert_rgb(index) + " = {" + val + "};"
        palfile += "\n" + final

    output_filename = os.path.splitext(os.path.basename(file))[0] + ".c"
    with open(output_filename, "w+") as f:
        f.write(palfile)

    print("Wrote palette to file", output_filename)

if __name__ == "__main__":
    exts = ['.ras', '.ps', '.im', '.tif', '.hdf', '.eps', '.jpg', '.icb', '.dds', '.bmp', '.msp', '.rgb', '.wmf', '.mpeg', '.h5', '.emf', '.blp', '.pcd', '.dcx', '.ftu', '.fit', '.pcx', '.jpeg', '.j2c', '.jpx', '.pxr', '.vda', '.gbr', '.pbm', '.cur', '.sgi', '.webp', '.qoi', '.jpf', '.pnm', '.pfm', '.vst', '.rgba', '.tga', '.jpe', '.pgm', '.xpm', '.png', '.psd', '.dib', '.j2k', '.icns', '.ftc', '.tiff', '.bw', '.ico', '.jpc', '.jfif', '.bufr', '.mpg', '.ppm', '.xbm', '.fli', '.flc', '.iim', '.jp2', '.apng', '.gif', '.fits', '.grib']
    main()
