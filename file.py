import os
import shutil


def copy_files():
    if os.path.exists("C:/1"):
        shutil.rmtree("C:/1")
    os.mkdir("C:/1")

    files = os.listdir("photos")

    for file in files:
        shutil.copy("photos/" + file, "C:/1")

    f = open("number_photo.txt", 'w')
    f.write("1")
    f.close()
