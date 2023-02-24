import pip._vendor.requests as requests
from zipfile import ZipFile
import shutil
import os

def update(newVersion)
    dl_link = "https://github.com/sinanates17/Huggeds-Keymode-Converter/archive/refs/tags/" + newNersion + ".zip"
    dl = requests.get(dl_link, allow_redirects=True)

    os.makedirs("delete")

    for oldFile in os.listdir():
        shutil.move(oldFile, "delete/" + oldFile)

    open("temp.zip","wb").write(dl.content)

    with ZipFile("temp.zip",'r') as temp:
        temp.extractall()
        temp.close()

    shutil.move("temp.zip", "delete/temp.zip")

    for newFile in os.listdir("Huggeds-Keymode-Converter-" + newVersion):
        shutil.move(newFile, os.getcwd() + "/" + newFile.split("/")[-1])

    print("Update Complete! Please press any key to exit then rerun the program.")
