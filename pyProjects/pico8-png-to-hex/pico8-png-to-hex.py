"""
Converts a .png file using the Pico-8's 16 color palette into 
a string of hex digits consumable by the Pico-8 to break 
the 256 tile sprite storage limit of that system.
"""
import sys              # used in calls to get CLI args
import subprocess       # used to derive filepath of CLI arg
from PIL import Image   # python imaging library

# imports from the pico8-png-to-hex project directory
from pngGraphicMethods import *
from p8Help import printHelp
from linneXtermColors import col

def getHexString(filePath):    
    """takes a filePath from command line and invokes other classes and 
    methods to produce the primary function of this python script--output 
    a single digit hexadecimal string consumable by the Pico-8"""
    # open image passed in
    img = Image.open(filePath)
    
    #create a list of the pixels
    pixels=list(img.convert('RGB').getdata())
    
    byteString=""

    #convert the RGB values in each pixel to a hex value, using a custom
    # dictionary with the long hex as key and the single-digit pico-8 palette as value 
    for r, g, b, in pixels:
        byteString+=longHex[rgb2hex(r,g,b)]
    #r, g, b = rgb_im.getpixel((0, 1))

    print(col.LT_GREEN + "\n  Pico-8 Image Hex String:\n" + col.LT_BLUE + "  " + byteString + "\n")

    img.close

def main():
    # check if a file argument was passed in from the  command line
    if ((len(sys.argv) < 2)  or (len(sys.argv) > 2) or 
        (sys.argv[-1] == '--help') or (sys.argv[-1] == '-help') or
        (sys.argv[-1] == '--h') or (sys.argv[-1] == '-h')):
        printHelp()
        sys.exit(0)    
    
    # get the filename passed in from command line    
    filename = sys.argv[-1]
    
    # invoke POSIX standard shell command as a subprocess to derive the directory  
    # of the filename passed in.  Works whether it's in same directory as python
    # script, or elsewhere
    path = subprocess.check_output("readlink -f {0}".format(filename), shell=True)
    path = path.rstrip('\n')
    print(col.LT_GREEN + "  Reading from...\n" + col.LT_BLUE + "  " + path)
    
    getHexString(path)
    
if __name__ == "__main__":
    main()
