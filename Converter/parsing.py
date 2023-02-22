from mapObjects import Note, TimingPoint

# Create the active conversion key from the keys in the config
def parseConversionKey(conversionKeys, inputKeymode, outputKeymode):
    preConversionKey = conversionKeys[f'{inputKeymode}-{outputKeymode}']
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

    return conversionKey

def parseMap(reference, changeAuthor, changeHP, changeOD):
    inputKeymode = None
    mappingMode = 0
    timingMode = False
    timingPoints = []
    redPoints = []
    greenPoints = []
    hitObjects = []
    outputHead = ''

    # By the end of this for loop, everything until the [HitObjects] section in the output file is written, and all the timing points and hit objects are stored in lists
    for line in reference.readlines():
        '''if 'Creator:' in line: #Change the beatmap author if indicated in the config
            outputHead += 'Creator:{changeAuthor}\n'
        elif 'HPDrainRate:' in line: #Change the beatmap HP if indicated in the config
            outputHead += 'HPDrainRate:{changeHP}\n'
        elif 'OverallDifficulty:' in line: #Change the beatmap OD if indicated in the config
            outputHead += 'OverallDifficulty:{changeOD}\n'''
        if 'Creator:' in line and changeAuthor is not None: #Change the beatmap author if indicated in the config
            outputHead += f'Creator:{changeAuthor}\n'
        elif 'HPDrainRate:' in line and changeHP is not None: #Change the beatmap HP if indicated in the config
            outputHead += f'HPDrainRate:{changeHP}\n'
        elif 'OverallDifficulty:' in line and changeOD is not None: #Change the beatmap OD if indicated in the config
            outputHead += f'OverallDifficulty:{changeOD}\n'
        elif 'CircleSize:' in line:
            inputKeymode = int(line.strip('CircleSize:'))
            outputHead += 'CircleSize:{outputKeymode}\n'
        elif 'Version:' in line:
            outputHead += f'{line[0:-1]} To {{outputKeymode}}K\n'
        else:
            if mappingMode == 0:
                outputHead += line
                #print(line)
            elif mappingMode == 1:
                note = Note.fromString(line, inputKeymode)
                hitObjects.append(note) # Add each hitobject to list containing all hitobject
        if timingMode:
            if ',' in line:
                point = TimingPoint.fromString(line)
                if point.uninherited:
                    redPoints.append(point) # Create arrays to store information about timing points. Each row is a point.
                    #print(redPoints[-1])
                #elif '0' in point.effects:
                    #greenPoints.append(point)
        if '[TimingPoints]' in line: # Know to start recording timing point info when the [TimingPoints] section of the .osu is reached.
            timingMode = True
            mappingMode = 0
        if '[HitObjects]' in line:
            mappingMode = 1
            timingMode = False

    return inputKeymode, redPoints, hitObjects, outputHead