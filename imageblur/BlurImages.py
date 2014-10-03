__author__ = 'will'

import sys
import os
from os import walk
from PIL import Image
from PIL import ImageFilter
from PIL import ImageFileIO

if len(sys.argv) < 2:
    print("Usage: BlurImages <rootdir>")
    exit()

strRootFolder = sys.argv[1]
if False == os.path.exists(strRootFolder):
    print("Error: Could not find folder " + strRootFolder)
else:
    print("Argument: " + strRootFolder)
    filesToBlur = []

    for root, dirNames, fileNames in walk(strRootFolder):
        for leFile in fileNames:
            filepath = os.path.join(root, leFile)
            if filepath.lower().endswith(".jpg") | filepath.lower().endswith(".png"):
                if filepath.lower().find("_blurred") < 0:
                    filesToBlur.append(filepath)
                    print("Found file " + filepath)

    for imagePath in filesToBlur:
        im = Image.open(imagePath)
        blurredImage = im.filter(ImageFilter.GaussianBlur(12))
        newImagePath = imagePath + "_blurred.jpg"
        blurredImage.save(newImagePath)
        print("Wrote " + newImagePath)

    img_filename = "/home/will/Pictures/happy.jpg"
    im = Image.open(img_filename)
    print("Image width: " + str(im.size[0]))
    print("Image height: " + str(im.size[1]))