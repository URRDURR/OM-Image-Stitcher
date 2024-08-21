from PIL import Image
import os
from tkinter import filedialog as fd
import pillow_jxl


# human style alphanumeric sort
def alphanumeric_sort(input_paths):
    nums = [(int(file.split("\\")[-1].split(".")[0].split(" ")[2][:-2]), file) for file in input_paths]
    nums.sort(key=lambda tup: tup[0])

    sorted_paths = []
    for i in nums:
        sorted_paths.append(i[1])

    return sorted_paths


# give the locations of all files of a type in a folder
def extract_file_locations(folder_path, file_type):

    # variable holds list of locations of all files of one type in a folder
    file_paths = []

    # creates list of all .{} files in directory
    testing = os.listdir(folder_path)

    for i in os.listdir(folder_path):
        if (i.endswith(file_type)) and ("50x" in i) and ("S" in i) and ("mm" in i):
            file_paths.append(i)

    # files sorted to be chronological
    file_paths = alphanumeric_sort(file_paths)

    example_file_name = file_paths[0]

    # give absolute path of each file in the directory
    for i in range(len(file_paths)):
        file_paths[i] = folder_path + "\\" + file_paths[i]

    return file_paths, example_file_name


# creates composite image
def merge(images, compression):
    temp_im = Image.open(images[0])
    w = temp_im.size[0] * len(images) // compression
    h = temp_im.size[1]
    long_im = Image.new("RGB", (w, h))

    for i in range(len(images)):
        im = Image.open(images[i])
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        long_im.paste(im, ((temp_im.size[0] * i) // compression, 0))

    return long_im


PATH_VIA_TERMINAL = True
COMPRESSION_VIA_TERMINAL = True

powers_list = [1, 2, 4, 8, 16, 32, 64, 26]

if PATH_VIA_TERMINAL == True:
    print("Enter folder location")
    folder_path = fd.askdirectory()
else:
    folder_path = r"C:\Users\gma78\OneDrive - Simon Fraser University (1sfu)\MOCVD-LAB\data\01-SMI-reactor\C03-Optical_microscope_images\S270"

if COMPRESSION_VIA_TERMINAL == True:
    while True:
        compression_factor = input("Enter shortening factor (power of 2 up to 64): ")
        compression_factor = int(compression_factor)
        if compression_factor in powers_list:
            break
        print("please try again")
else:
    compression_factor = 1

extention = ".jxl"

image_paths, file_example = extract_file_locations(folder_path, "tif")
image = merge(image_paths, compression_factor)

print("Starting . . .")

file_example_split = file_example.split(" ")
file_name = (
    file_example_split[0] + " " + file_example_split[1] + " " + "Shortened" + " " + str(compression_factor) + "x"
)
file_path = folder_path + "\\" + file_name + extention

image.save(file_path, lossless=True)
print(file_path)
print("Finished!")
