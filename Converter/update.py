import pip._vendor.requests as requests
from zipfile import ZipFile
import shutil
import os

def updater(newVersion):
    dl_link = "https://github.com/sinanates17/Huggeds-Keymode-Converter/archive/refs/tags/" + newVersion + ".zip"
    dl = requests.get(dl_link, allow_redirects=True)

    oneFolderUp = os.getcwd().strip("/" + os.getcwd().split("/")[-1])

    deletePath = oneFolderUp + "/delete"

    os.makedirs(deletePath)

    for oldFile in os.listdir():
        shutil.move(oldFile, deletePath + "/" + oldFile)

    open("temp.zip","wb").write(dl.content)

    with ZipFile("temp.zip",'r') as temp:
        temp.extractall()
        temp.close()

    shutil.move("temp.zip", deletePath + "/temp.zip")

    for newFile in os.listdir("Huggeds-Keymode-Converter-" + newVersion):
        shutil.move(newFile, os.getcwd() + "/" + newFile.split("/")[-1])

    shutil.rmtree(deletePath)

    print("Update Complete! Please press any key to exit then rerun the program.")
