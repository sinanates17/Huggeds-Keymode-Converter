import os
import configparser
import convert
import parsing
import updater
import pip._vendor.requests as requests
import zipfile
import shutil

currentVersion = "osu" #Change this line every time a new release is made

updater.checkUpdate(currentVersion)
                        
# Parse the config
cfg = configparser.ConfigParser(allow_no_value=True)
cfg.read('config.ini')

changeAuthor = cfg['Metadata'].get('change_author')
if changeAuthor == '': changeAuthor = None
changeHP = cfg['Metadata'].get('change_hp')
if changeHP == '': changeHP = None
changeOD = cfg['Metadata'].get('change_od')
if changeOD == '': changeOD = None
autoSort = cfg['Metadata']['autosort']
songDir = cfg['Metadata']['songs_folder']

outputKeymode = cfg.getint('Mapping','target_keymode')
conversionMode = cfg['Mapping']['conversion_mode']
alternateInterval = cfg.getfloat('Mapping','alternate_interval')
unjack = cfg['Mapping']['unjack']
unjackInterval = cfg.getfloat('Mapping','unjack_interval')
maxJack = cfg.getint('Mapping','max_jack')
minShieldInterval = cfg.getfloat('Mapping','min_shield_interval')
shieldPreserver =  cfg['Mapping']['shield_preserver']
shieldThreshold = cfg.getfloat('Mapping','shield_threshold')
shieldPreserverInterval = cfg.getfloat('Mapping','shield_preserver_interval')
maxShield = cfg.getint('Mapping','max_shield')
buffAmount = cfg.getfloat('Mapping','buff')

# Initialize stuffs
inputDirectory = os.getcwd() + '/Input/'
outputDirectory = os.getcwd() + '/Output/'

#Parse the Input folder for maps to process
beatmaps = [] #Formated as [beatmap, origin]
for f in os.listdir(inputDirectory):
    # Skip if not file
    #if not os.path.isfile(inputDirectory + f):
        #continue

    # Add all .osu files
    if f.endswith(".osu"):
        beatmaps.append([f, None])

    # If an osz is inputted, scan it and add any .osu files to the beatmaps
    elif f.endswith(".osz"):
        #Extract the .osz into a temporary folder
        with zipfile.ZipFile(inputDirectory + f, 'r') as osz:
            os.mkdir(inputDirectory + f[0:-4])
            osz.extractall(path=inputDirectory + f[0:-4])
        for ff in os.listdir(inputDirectory + f[0:-4]):
            if ff.endswith(".osu"):
                beatmaps.append([ff, inputDirectory + f])
        
    # If a beatmap folder is inputted, scan it and add any .osu files to the beatmaps
    elif os.path.isdir(inputDirectory + f):
        for ff in os.listdir(os.getcwd() +  f):
            if ff.endswith(".osu"):
                beatmaps.append([ff, inputDirectory + f])

# Loop through every difficulty in the Input folder and create converts
for i,beatmap in enumerate(beatmaps):
    #Print progress
    print(f'Converting map {i+1}/{len(beatmaps)} | {beatmap[0].strip(".osu")}')

    # Parse the map for its stuff
    if beatmap[1] == None:
        with open(inputDirectory + beatmap[0], "r", encoding="utf8") as f:
            inputKeymode, redPoints, hitObjects, outputHead, setID, creator, title, artist = parsing.parseMap(f, changeAuthor, changeHP, changeOD)
    
    elif '.osz' in beatmap[1]:
        with open(beatmap[1][0:-4] + "/" + beatmap[0], "r", encoding="utf8") as f:
            inputKeymode, redPoints, hitObjects, outputHead, setID, creator, title, artist = parsing.parseMap(f, changeAuthor, changeHP, changeOD)

    elif os.path.isdir(beatmap[1]):
        with open(inputDirectory + beatmap[1] + "/" + beatmap[0], "r", encoding="utf8") as f:
            inputKeymode, redPoints, hitObjects, outputHead, setID, creator, title, artist = parsing.parseMap(f, changeAuthor, changeHP, changeOD)

    # Parse the conversion key
    conversionKey = parsing.parseConversionKey(cfg['Conversion Keys'], inputKeymode, outputKeymode)

    # Pass all of the timing points, hit objects, and configurable paramaters into the 'convert' method, which returns a list containing all of the hit objects for the output file
    newHitObjects = convert.convertMap(hitObjects, redPoints, inputKeymode, outputKeymode, conversionMode, alternateInterval, maxJack, unjack, unjackInterval, minShieldInterval, conversionKey, shieldPreserver, shieldThreshold, shieldPreserverInterval, maxShield, buffAmount)

    filename = beatmap[0][0:-4] + " To " + str(outputKeymode) + "K.osu" #Set the filename for the converted difficulty

    #Try to find the right beatmap folder if autosort is on
    destination = None
    if autoSort == '1':
        for folder in os.listdir(songDir):
            done = False
            if os.path.isdir(songDir + '/' + folder):
                if title in folder and artist in folder:
                    for file in os.listdir(songDir + '/' + folder):
                        if file.endswith('.osu'):
                            with open(songDir + '/' + folder + '/' + file) as chart:
                                while True:
                                    line = chart.readline()
                                    if 'Title:' in line:
                                        theTitle = line.split(':')[-1]
                                    elif 'Artist:' in line:
                                        theArtist = line.split(':')[-1]
                                    elif 'Creator:' in line:
                                        theCreator = line.split(':')[-1]
                                    elif 'BeatmapSetID:' in line:
                                        theSetID = line.split(':')[-1]
                                        break
                            if theSetID == setID and setID != '-1':
                                done = True
                                destination = songDir + '/' + folder + '/'
                                break
                            elif title == theTitle and artist == theArtist and creator == theCreator and setID == '-1':
                                done = True
                                destination = songDir + '/' + folder + '/'
                                break
                    if done:
                        break

    #Move the converted .osus into the proper beatmap folders 
    if destination != None:
        with open(destination + filename,"w", encoding="utf8") as f:
            #todo changeAuthor
            #todo changeHP
            #todo changeOD
            edits = {'keymode': outputKeymode}
            f.write(outputHead.format(**edits))

            # Code to write the new hit objects into the output file
            for newNote in newHitObjects:
                laneNumber = (newNote.lane)*(512/outputKeymode)+2
                f.write(f'{laneNumber},192,{newNote.startTime},{newNote.noteType},{newNote.hitSound},{newNote.endTime}{newNote.sample}\n')
    else:
        with open(outputDirectory + filename,"w", encoding="utf8") as f:
            #todo changeAuthor
            #todo changeHP
            #todo changeOD
            edits = {'keymode': outputKeymode}
            f.write(outputHead.format(**edits))

            # Code to write the new hit objects into the output file
            for newNote in newHitObjects:
                laneNumber = (newNote.lane)*(512/outputKeymode)+2
                f.write(f'{laneNumber},192,{newNote.startTime},{newNote.noteType},{newNote.hitSound},{newNote.endTime}{newNote.sample}\n')

    if beatmap[1] != None:
        if os.path.isdir(beatmap[1]):
            shutil.move(outputDirectory + filename, destination)

        elif '.osz' in beatmap[1]:
            with zipfile.ZipFile(beatmap[1],"a") as dest:
                dest.write(outputDirectory + filename, filename)
                os.remove(outputDirectory + filename)

#After everything, move .oszs and beatmap folders in the Input folder to the Output folder
for dir in os.listdir(inputDirectory):
    if '.osz' in dir or os.path.isdir(inputDirectory + dir):
        shutil.move(inputDirectory + dir, outputDirectory)

input("Done! Press enter to exit.")
