import pip._vendor.requests as requests
from zipfile import ZipFile
import shutil
import os

def updater(newVersion):
    dl_link = "https://github.com/sinanates17/Huggeds-Keymode-Converter/archive/refs/tags/" + newVersion + ".zip"
    dl = requests.get(dl_link, allow_redirects=True)

    for oldFile in os.listdir():
        if os.path.isdir(oldFile)
            shutil.rmtree(oldFile)
        else:
            os.remove(oldFile)

    open("temp.zip","wb").write(dl.content)

    with ZipFile(oneFolderUp + "temp.zip",'r') as temp:
        temp.extractall()
        temp.close()

    os.remove("temp.zip")

    for newFile in os.listdir(os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion):
        shutil.move(newFile, os.getcwd() + "/" + newFile.split("/")[-1])

    print("Update Complete! Please press any key to exit then rerun the program.")
