import pip._vendor.requests as requests
from zipfile import ZipFile
import shutil
import os

def checkUpdate(currentVersion):
    #Check if the current verison is up to date, if so, ask the user if they want to auto update
    currentVersion = "osu" #Change this line every time a new release is made
    url = "http://github.com/sinanates17/Huggeds-Keymode-Converter/releases/latest"
    r = requests.get(url, allow_redirects=True)
    latestVersion = r.url.split('/')[-1]

    if currentVersion != latestVersion:
        choice = input("A new release is available, would you like to update? (\"yes\" or \"no\") ").lower()
        while choice not in ["yes", "no"]:
            choice = input("\"yes\" or \"no\" ").lower()
        if choice == "yes":
            import sys
            update(latestVersion)
            input()
            sys.exit()
        elif choice == "no":
            pass

def update(newVersion):
    dl_link = "https://github.com/sinanates17/Huggeds-Keymode-Converter/archive/refs/tags/" + newVersion + ".zip"
    dl = requests.get(dl_link, allow_redirects=True)

    oneFolderUp = os.getcwd() + "/.."

    deletePath = oneFolderUp + "/delete"

    os.makedirs(deletePath, exist_ok = True)

    for oldFile in os.listdir():
        shutil.move(oldFile, deletePath + "/" + oldFile)

    open(oneFolderUp + "/temp.zip","wb").write(dl.content)

    with ZipFile(oneFolderUp + "temp.zip",'r') as temp:
        temp.extractall(oneFolderUp)
        temp.close()

    shutil.move("temp.zip", deletePath + "/temp.zip")

    for newFile in os.listdir("Huggeds-Keymode-Converter-" + newVersion):
        shutil.move(newFile, os.getcwd() + "/" + newFile.split("/")[-1])

    shutil.rmtree(deletePath)

    print("Update Complete! Please press any key to exit then rerun the program.")
