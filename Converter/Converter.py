import os
import configparser
from math import floor
import convert
from mapObjects import Note, TimingPoint

#Parse the config
config = configparser.ConfigParser(allow_no_value=True)
config.read('config.ini')

changeAuthor = config['Metadata']['change_author']
changeHP = config['Metadata']['change_hp']
changeOD = config['Metadata']['change_od']

outputKeymode = config.getint('Mapping','target_keymode')
conversionMode = config['Mapping']['conversion_mode']
alternateInterval = config.getfloat('Mapping','alternate_interval')
unjack = config['Mapping']['unjack']
unjackInterval = config.getfloat('Mapping','unjack_interval')
maxJack = config.getint('Mapping','max_jack')
minShieldInterval = config.getfloat('Mapping','min_shield_interval')
shieldPreserver =  config['Mapping']['shield_preserver']
shieldThreshold = config.getfloat('Mapping','shield_threshold')
shieldPreserverInterval = config.getfloat('Mapping','shield_preserver_interval')
maxShield = config.getint('Mapping','max_shield')
buffAmount = config.getfloat('Mapping','buff')

#Initialize stuffs
inputDirectory = os.getcwd() + '/Input/'
outputDirectory = os.getcwd() + '/Output/'
inputs = os.listdir(inputDirectory)

#Loop through every difficulty in the Input folder and create converts in the Output folder
for beatmap in inputs:
    #Ignore files that dont end in .osu
    if not beatmap.endswith(".osu"):
        continue

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
    preConversionKey = config['Conversion Keys'][str(inputKeymode) + '-' + str(outputKeymode)]
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
                lane = floor(int(line.split(',')[0])/(512/inputKeymode))
                startTime = int(line.split(',')[2])
                noteType = line.split(',')[3]
                hitSound = line.split(',')[4]
                endTime = int(line.split(',')[5].split(':')[0])
                sample = line.split(',')[5]
                sample = sample[sample.find(':'):-1]
                note = Note(lane, startTime, noteType, hitSound, endTime, sample)
                hitObjects.append(note)
                #print(hitObjects[-1])
        if timingMode:
            if ',' in line:
                point = TimingPoint(*line.split(','))
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
        output.write(str(laneNumber) + ',192,' + str(newNote.startTime) + ',' + str(newNote.noteType) + ',' + str(newNote.hitSound) + ',' + str(newNote.endTime) + str(newNote.sample) + '\n')
    output.close()
