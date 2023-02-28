import pip._vendor.requests as requests
from zipfile import ZipFile
import shutil
import os

def updater(newVersion):
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

    for newFile in os.listdir(os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion):
        path = os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion + "/" + newFile
        if os.path.isdir(path):
            #print("Trying to copy " + newFile + " as a directory")
            shutil.copytree(os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion + "/" + newFile, os.getcwd() + "/" + newFile)
        else:
            #print("Trying to copy " + newFile + " as a file")
            shutil.copy(os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion + "/" + newFile, os.getcwd() + "/" + newFile)
                    
        #print("Copied " + newFile + " to root dir")
                    
    shutil.rmtree(os.getcwd() + "/Huggeds-Keymode-Converter-" + newVersion)
    #print("Removed extracted dir after copying")

    print("Update Complete! Please press any key to exit then rerun the program.")
