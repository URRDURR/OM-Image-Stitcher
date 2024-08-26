from stitching import Stitcher
from tkinter import filedialog as fd
import os
from PIL import Image
import pillow_jxl
import cv2 as cv

# ///////////////////////////////////////////
# NOTE: The mirroring is wierd I dont get it,
# the microscope should be fliping it but
# doesnt seem like it looking at S267
# ///////////////////////////////////////////

# give the locations of all files of a type in a folder
def extract_file_locations(folder_path, file_type):

    # variable holds list of locations of all files of one type in a folder
    file_paths = []
    
    # creates list of all .{} files in directory
    testing = os.listdir(folder_path)

    for i in os.listdir(folder_path):
        if (i.endswith(file_type)) and ("5x" in i) and ("S" in i):
            file_paths.append(i)

    example_file_name = file_paths[0]

    # give absolute path of each file in the directory
    for i in range(len(file_paths)):
        file_paths[i] = folder_path + "\\" + file_paths[i]
    
    return file_paths, example_file_name


PATH_VIA_TERMINAL = False

powers_list = [1, 2, 4, 8, 16, 32, 64, 26]

if PATH_VIA_TERMINAL == True:
    print("Enter folder location")
    folder_path = fd.askdirectory()
else:
    folder_path = r"C:\Users\gma78\Desktop\stich"

file_locations, ___ = extract_file_locations(folder_path, "tif")

print(file_locations)

stitcher = Stitcher()
# confidence_threshold = 0.8

print("Starting . . .")
image = stitcher.stitch(file_locations)

imagep = Image.fromarray(image)
r, g, b = imagep.split()
imagep = Image.merge("RGB", (b, g, r))
imagep = imagep.transpose(Image.FLIP_TOP_BOTTOM)
imagep = imagep.transpose(Image.FLIP_LEFT_RIGHT)

file_path = folder_path + "\\" + "test-6.1.jxl"
imagep.save(file_path, lossless=True)
# cv.imwrite((folder_path + "\\" + "test-6.2.png"), image)
print("Finished!")
