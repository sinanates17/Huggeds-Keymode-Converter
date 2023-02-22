import os
import configparser
from math import floor
import convert
from mapObjects import Note, TimingPoint

#Parse the config
cfg = configparser.ConfigParser(allow_no_value=True)
cfg.read('config.ini')

changeAuthor = cfg['Metadata']['change_author']
changeHP = cfg['Metadata']['change_hp']
changeOD = cfg['Metadata']['change_od']

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

#Initialize stuffs
inputDirectory = os.getcwd() + '/Input/'
outputDirectory = os.getcwd() + '/Output/'

beatmaps = []
for f in os.listdir(inputDirectory):
    # Skip if not file
    if not os.path.isfile(inputDirectory + f):
        continue

    # Add all .osu files
    if f.endswith(".osu"):
        beatmaps.append(f)

    # Skip .osz for now, maybe add support later
    elif f.endswith(".osz"):
        pass

#Loop through every difficulty in the Input folder and create converts in the Output folder
for i,beatmap in enumerate(beatmaps):
    #Print progress
    print(f'Converting map {i+1}/{len(beatmaps)} | {beatmap.strip(".osu")}')

    reference = open(inputDirectory + beatmap,"r", encoding="utf8")

    #Find the keymode to be converted
    for line in reference.readlines(): 
        if "CircleSize:" in line:
            inputKeymode = int(line[11:-1])
            #print(inputKeymode)
            reference.close()
            break

    #Create the active conversion key from the keys in the config
    reference = open(inputDirectory + beatmap,"r",encoding="utf8")
    preConversionKey = cfg['Conversion Keys'][str(inputKeymode) + '-' + str(outputKeymode)]
    preConversionKey = preConversionKey.split(',')
    conversionKey = [[] for i in range(inputKeymode)]
    counter = 0
    idk = 0
    for value in preConversionKey:
        if '\n' in value:
            conversionKey[idk].append(value[-1])
        else:
            conversionKey[idk].append(value)
        counter += 1
        if counter == outputKeymode:
            counter = 0
            idk += 1

    #Start writing metadata into the output difficulty
    filename = beatmap[0:-4] + " To " + str(outputKeymode) + "K.osu" #Set the filename for the converted difficulty
    output = open(outputDirectory + filename,"w", encoding="utf8")
    mappingMode = 0
    timingMode = False
    timingPoints = []
    redPoints = []
    greenPoints = []
    hitObjects = []

    #By the end of this for loop, everything until the [HitObjects] section in the output file is written, and all the timing points and hit objects are stored in lists
    for line in reference.readlines():
        if 'Creator:' in line and changeAuthor != 'none': #Change the beatmap author if indicated in the config
            output.write('Creator:' + changeAuthor + '\n')
        elif 'HPDrainRate:' in line and changeHP != 'none': #Change the beatmap HP if indicated in the config
            output.write('HPDrainRate:' + changeHP + '\n')
        elif 'OverallDifficulty:' in line and changeOD != 'none': #Change the beatmap OD if indicated in the config
            output.write("OverallDifficulty:" + changeOD + '\n')
        elif 'CircleSize:' in line:
            output.write("CircleSize:" + str(outputKeymode) + '\n')
        elif 'Version:' in line:
            output.write(line[0:-1] + " To " + str(outputKeymode) + 'K\n')
        else:
            if mappingMode == 0:
                output.write(line)
                #print(line)
            elif mappingMode == 1:
                note = Note.fromString(line, inputKeymode)
                hitObjects.append(note) #Add each hitobject to list containing all hitobject
        if timingMode:
            if ',' in line:
                point = TimingPoint.fromString(line)
                if point.uninherited:
                    redPoints.append(point) #Create arrays to store information about timing points. Each row is a point.
                    #print(redPoints[-1])
                #elif '0' in point.effects:
                    #greenPoints.append(point)
        if '[TimingPoints]' in line: #Know to start recording timing point info when the [TimingPoints] section of the .osu is reached.
            timingMode = True
            mappingMode = 0
        if '[HitObjects]' in line:
            mappingMode = 1
            timingMode = False
    reference.close()

    #Pass all of the timing points, hit objects, and configurable paramaters into the 'convert' method, which returns a list containing all of the hit objects for the output file
    newHitObjects = convert.map(hitObjects, redPoints, inputKeymode, outputKeymode, conversionMode, alternateInterval, maxJack, unjack, unjackInterval, minShieldInterval, conversionKey,shieldPreserver,shieldThreshold,shieldPreserverInterval,maxShield, buffAmount)

    #Code to write the new hit objects into the output file
    for newNote in newHitObjects:
        laneNumber = (newNote.lane)*(512/outputKeymode)+2
        output.write(f'{laneNumber},192,{newNote.startTime},{newNote.noteType},{newNote.hitSound},{newNote.endTime}{newNote.sample}\n')
    output.close()

input("Done! Press enter to exit.")
