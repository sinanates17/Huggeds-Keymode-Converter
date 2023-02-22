from mapObjects import Note, TimingPoint

# Create the active conversion key from the keys in the config
def parseConversionKey(conversionKeys, inputKeymode, outputKeymode):
    rawConversionKey = conversionKeys[f'{inputKeymode}-{outputKeymode}'].split(',')

    conversionKey = [[] for i in range(inputKeymode)]
    counter = 0
    idk = 0
    for value in rawConversionKey:
        if '\n' in value:
            conversionKey[idk].append(value[-1])
        else:
            conversionKey[idk].append(value)
        counter += 1
        if counter == outputKeymode:
            counter = 0
            idk += 1

    return conversionKey

def parseMap(reference, author, HP, OD):
    inputKeymode = None
    mappingMode = False
    timingMode = False
    timingPoints = []
    redPoints = []
    greenPoints = []
    hitObjects = []
    outputHead = ''

    # By the end of this for loop, everything until the [HitObjects] section in the output file is written, and all the timing points and hit objects are stored in lists
    for line in reference.readlines():
        # Add each hitobject to list containing all hitobjects
        if mappingMode:
                note = Note.fromString(line, inputKeymode)
                hitObjects.append(note)

        # Change the beatmap author if indicated in the config
        elif 'Creator:' in line and author is not None: 
            outputHead += f'Creator:{author}\n'

        # Change the beatmap HP if indicated in the config
        elif 'HPDrainRate:' in line and HP is not None: 
            outputHead += f'HPDrainRate:{HP}\n'

        # Change the beatmap OD if indicated in the config
        elif 'OverallDifficulty:' in line and OD is not None: 
            outputHead += f'OverallDifficulty:{OD}\n'

        # Get input keymode from circlesize and leave field to be formatted.
        elif 'CircleSize:' in line:
            inputKeymode = int(line.strip('CircleSize:'))
            outputHead += 'CircleSize:{keymode}\n'

        elif 'Version:' in line:
            outputHead += f'{line[0:-1]} To {{keymode}}K\n'

        else:
            # Write everything outside of HitObjects to output
            outputHead += line

            # Add each timing point to a list. Only track red points for now
            if timingMode:
                if ',' in line:
                    point = TimingPoint.fromString(line)
                    if point.uninherited:
                        redPoints.append(point)
                    #elif '0' in point.effects:
                        #greenPoints.append(point)

        # Know to start recording timing point info when the [TimingPoints] section of the .osu is reached, same for hitobjects
        if '[TimingPoints]' in line: 
            timingMode = True
            mappingMode = False
        if '[HitObjects]' in line:
            mappingMode = True
            timingMode = False

    return inputKeymode, redPoints, hitObjects, outputHead
