from stitching import Stitcher
from tkinter import filedialog as fd
import os
from PIL import Image
import pillow_jxl


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
    folder_path = r"C:\Users\gma78\Desktop\Stitch Test"

file_locations, ___ = extract_file_locations(folder_path, "tif")

stitcher = Stitcher()

print("Starting . . .")
image = stitcher.stitch(file_locations)

image = Image.fromarray(image)
r, g, b = image.split()
image = Image.merge("RGB", (b, g, r))
image = image.transpose(Image.ROTATE_180)

file_path = folder_path + "\\" + "test-4.jxl"
image.save(file_path, lossless=True)
print("Finished!")
