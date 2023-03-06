import requests
from zipfile import ZipFile
import shutil
import os

def checkUpdate(currentVersion):
    #Check if the current verison is up to date, if so, ask the user if they want to auto update
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

    for oldFile in os.listdir():
        if os.path.isdir(oldFile):
            shutil.rmtree(oldFile)
        else:
            os.remove(oldFile)
        #print("Removed " + oldFile)

    open("temp.zip","wb").write(dl.content)
    #print("Created temp zip")

    with ZipFile("temp.zip",'r') as temp:
        temp.extractall()
        #print("Extracted temp zip")

    os.remove("temp.zip")
    #print("Removed temp zip")

    for newFile in os.listdir(os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion[1:]):
        path = os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion[1:] + "/" + newFile
        if os.path.isdir(path):
            #print("Trying to copy " + newFile + " as a directory")
            shutil.copytree(os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion[1:] + "/" + newFile, os.getcwd() + "/" + newFile)
        else:
            #print("Trying to copy " + newFile + " as a file")
            shutil.copy(os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion[1:] + "/" + newFile, os.getcwd() + "/" + newFile)
                    
        #print("Copied " + newFile + " to root dir")
                    
    shutil.rmtree(os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion[1:])
    #print("Removed extracted dir after copying")

    print("Update Complete! Please press any key to exit then rerun the program.")
