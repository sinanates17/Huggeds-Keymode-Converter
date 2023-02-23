import pip._vendor.requests as requests
from zipfile import ZipFile
import shutil
import os

url = "http://github.com/sinanates17/Huggeds-Keymode-Converter/releases/latest"
r = requests.get(url, allow_redirects=True)
version = r.url.split('/')[-1]
dl_link = "https://github.com/sinanates17/Huggeds-Keymode-Converter/archive/refs/tags/" + version + ".zip"
dl = requests.get(dl_link, allow_redirects=True)

os.makedirs("delete")

for oldFile in os.listdir():
    shutil.move(oldFile, "delete/" + oldFile)

open("temp.zip","wb").write(dl.content)

with ZipFile("temp.zip",'r') as temp:
    temp.extractall()
    temp.close()

shutil.move("temp.zip", "delete/temp.zip")

for newFile in os.listdir("Huggeds-Keymode-Converter-" + version):
    shutil.move(newFile, os.getcwd() + "/" + newFile.split("/")[-1])

print("Update Complete!")
