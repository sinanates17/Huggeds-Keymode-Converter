import random
from note import note

#Establish what the current beatLength is
def establishBeatLength(note, points):
    for point in points:
        if float(point[1]) <= note.startTime:
            beatLength = float(point[1])
        else:
            beatLength = 150.0

# todo
'''
#Figure out what lanes are allowed for this note based on allowedLanes and restrictions from other placed notes (e.g within the unjack interval of another note or overlapping with other notes)
def checkAllowedLanes(note, conversionKey):
    possibleLanes = conversionKey[note.lane]
    allowedLanes = []

    #For every lane this note can be placed on based on the coversion key, check if the lane is available by making sure there are no occupied invervals at this time point that have a different origin lane.
    for outputLane in possibleLanes:
        okay = True
        for interval in occupiedIntervals[outputLane]:
            if note.isRice():
                if note.startTime >= interval[0] and note.startTime <= interval[1] and interval[2] != note.lane: 
                    okay = False
            elif note.isLN():
                if (note.startTime >= interval[0] and note.startTime <= interval[1] and interval[2] != note.lane) or (note.endTime >= interval[0] and note.endTime <= interval[1] and interval[2] != note.lane): 
                    okay = False
        if okay:
            allowedLanes.append(outputLane)

    return allowedLanes
'''

def map(inObjects, points, inMode, outMode, conversionMode, alternateInterval, maxJack, unjack, unjackInterval, minShieldInterval, conversionKey, keepShield, shieldThreshold, shieldInterval, maxShield, buffAmount):

    outObjects = [] #Initialize a list to contain all the converted hitobjects

    #HitObject format: [lane startTime noteType hitSound endTime sample]
    #Timing Point format: [time beatLength meter sampleSet sampleIndex volume uninherited effects]

    #Convert the conversion key to a list of lists containing output lane numbers

    #print(points)
    newConversionKey = []
    for inLane in conversionKey:
        theLanes = []
        for outLane in range(len(inLane)):
            if inLane[outLane] == '1':
                theLanes.append(outLane)
        newConversionKey.append(theLanes)
    #print(newConversionKey)

    if conversionMode == 'random':
        occupiedIntervals = [[] for i in range(outMode)] #Contains a list of intervals in [startTime endTime originLane] format for EVERY output column where future notes CANNOT be placed
        for note in inObjects:
            #print(note)

            beatLength = establishBeatLength(note, points)

            #Set the unjack time interval (ms) based on the BPM if unjack is true
            if unjack == '1':
                unjackTime = (unjackInterval * beatLength) + 2
            else:
                unjackTime = 0

            #Figure out what lanes are allowed for this note based on allowedLanes and restrictions from other placed notes (e.g within the unjack interval of another note or overlapping with other notes)
            possibleLanes = newConversionKey[note.lane]
            allowedLanes = []

            #For every lane this note can be placed on based on the coversion key, check if the lane is available by making sure there are no occupied invervals at this time point that have a different origin lane.
            for outputLane in possibleLanes:
                okay = True
                for interval in occupiedIntervals[outputLane]:
                    if note.isRice():
                        if note.startTime >= interval[0] and note.startTime <= interval[1] and interval[2] != note.lane: 
                            okay = False
                    elif note.isLN():
                        if (note.startTime >= interval[0] and note.startTime <= interval[1] and interval[2] != note.lane) or (note.endTime >= interval[0] and note.endTime <= interval[1] and interval[2] != note.lane): 
                            okay = False
                if okay:
                    allowedLanes.append(outputLane)

            #Choose a lane to place this note on. If there are no available lanes, don't place a note.
            if allowedLanes: #Empty lists are false. Only map this note if there are available lanes
                laneChoice = random.choice(allowedLanes)
                #print(allowedLanes)
                newNote = note.newNoteInLane(laneChoice)
                outObjects.append(newNote)


                #Set restrictions for future notes based on where this note was placed
                if note.isRice():
                    occupiedIntervals[laneChoice].append([note.startTime, note.startTime + unjackTime, note.lane])
                else:
                    if note.startTime + unjackTime >= note.endTime + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note.startTime, note.startTime + unjackTime, note.lane])
                    elif note.startTime + unjackTime < note.endTime + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note.startTime, note.endTime + (beatLength * minShieldInterval) - 2, note.lane])

    if conversionMode == 'random_nojack':
        noJackLanes = [-1 for i in range(inMode)]
        occupiedIntervals = [[] for i in range(outMode)] #Contains a list of intervals in [startTime endTime originLane] format for EVERY output column where future notes CANNOT be placed
        for note in inObjects:
            #print(note)

            beatLength = establishBeatLength(note, points)

            #Set the unjack time interval (ms) based on the BPM if unjack is true
            if unjack == '1':
                unjackTime = (unjackInterval * beatLength) + 2
            else:
                unjackTime = 0

            #Figure out what lanes are allowed for this note based on allowedLanes and restrictions from other placed notes (e.g within the unjack interval of another note or overlapping with other notes)
            possibleLanes = newConversionKey[note.lane]
            allowedLanes = []

            #For every lane this note can be placed on based on the coversion key, check if the lane is available by making sure there are no occupied invervals at this time point that have a different origin lane.
            for outputLane in possibleLanes:
                okay = True
                for interval in occupiedIntervals[outputLane]:
                    if note.isRice():
                        if note.startTime >= interval[0] and note.startTime <= interval[1] and interval[2] != note.lane: 
                            okay = False
                    elif note.isLN():
                        if (note.startTime >= interval[0] and note.startTime <= interval[1] and interval[2] != note.lane) or (note.endTime >= interval[0] and note.endTime <= interval[1] and interval[2] != note.lane): 
                            okay = False
                if len(possibleLanes) > 1:
                    if outputLane == noJackLanes[note.lane]:
                        okay = False
                if okay:
                    allowedLanes.append(outputLane)

            #Choose a lane to place this note on. If there are no available lanes, don't place a note.
            if allowedLanes: #Empty lists are false. Only map this note if there are available lanes
                laneChoice = random.choice(allowedLanes)
                #print(allowedLanes)
                newNote = note.newNoteInLane(laneChoice)
                outObjects.append(newNote)


                #Set restrictions for future notes based on where this note was placed
                if note.isRice():
                    occupiedIntervals[laneChoice].append([note.startTime, note.startTime + unjackTime, note.lane])
                elif note.isLN():
                    if note.startTime + unjackTime >= note.endTime + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note.startTime, note.startTime + unjackTime, note.lane])
                    elif note.startTime + unjackTime < note.endTime + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note.startTime, note.endTime + (beatLength * minShieldInterval), note.lane])
                
                noJackLanes[note.lane] = laneChoice

    if conversionMode == 'jack_alternate':
        occupiedIntervals = [[] for i in range(outMode)] #Contains a list of intervals in [startTime endTime originLane] format for EVERY output column where future notes CANNOT be placed
        jackConditionals = [[-10000, maxJack,-1] for i in range(inMode)] #Format: [time, currentJackCount, currentOutLane]. Every input lane has a conditional that determines if the next note from that lane will be jacked.
        shieldConditionals = [[-10000, -10000, maxShield,-1] for i in range(inMode)] #Format: [headTime, tailTime currentShieldCount, currentOutLane]. Every input lane has a conditional that determines if the next note from that lane will be shielded
        for note in inObjects:
            #print(note)

            beatLength = establishBeatLength(note, points)

            #Set the unjack time interval (ms) based on the BPM if unjack is true
            if unjack == '1':
                unjackTime = (unjackInterval * beatLength) + 2
            else:
                unjackTime = 0
            if keepShield == '1':
                shieldThresholdTime = shieldThreshold * beatLength - 2
                shieldIntervalTime = shieldInterval * beatLength + 2
            else:
                shieldThresholdTime = 1000000
                shieldIntervalTime = 0

            #Figure out what lanes are allowed for this note based on allowedLanes and restrictions from other placed notes (e.g within the unjack interval of another note or overlapping with other notes)
            possibleLanes = newConversionKey[note.lane]
            allowedLanes = []

            #For every lane this note can be placed on based on the coversion key, check if the lane is available by making sure there are no occupied invervals at this time point that have a different origin lane.
            for outputLane in possibleLanes:
                okay = True
                for interval in occupiedIntervals[outputLane]:
                    if note.isRice():
                        if note.startTime >= interval[0] and note.startTime <= interval[1] and interval[2] != note.lane: 
                            okay = False
                    elif note.isLN():
                        if (note.startTime >= interval[0] and note.startTime <= interval[1] and interval[2] != note.lane) or (note.endTime >= interval[0] and note.endTime <= interval[1] and interval[2] != note.lane) or (interval[0] >= note.startTime and interval[0] <= note.endTime and interval[2] != note.lane) or (interval[1] >= note.startTime and interval[0] <= note.endTime and interval[2] != note.lane): 
                            okay = False
                if okay:
                    allowedLanes.append(outputLane)

            #Choose an output lane based on the jack conditionals
            if allowedLanes: #Empty lists are falsy
                #Maximum jacks for an output column has been reached and its time to switch to the next column
                if (jackConditionals[note.lane][1] == maxJack) and jackConditionals[note.lane][2] in allowedLanes:
                    laneChoice = allowedLanes[(allowedLanes.index(jackConditionals[note.lane][2])+1)%len(allowedLanes)]
                    jackConditionals[note.lane][0] = note.startTime
                    jackConditionals[note.lane][1] = 1 
                    jackConditionals[note.lane][2] = laneChoice
                    newNote = note.newNoteInLane(laneChoice)
                    outObjects.append(newNote)


                #Within the jack interval and placing another jack is available
                elif (jackConditionals[note.lane][0] + (alternateInterval * beatLength) > note.startTime) and jackConditionals[note.lane][2] in allowedLanes:
                    laneChoice = jackConditionals[note.lane][2]
                    jackConditionals[note.lane][0] = note.startTime
                    jackConditionals[note.lane][1] += 1
                    jackConditionals[note.lane][2] = laneChoice
                    newNote = note.newNoteInLane(laneChoice)
                    outObjects.append(newNote)


                #Either we're out of the jack interval or placing another jack isn't available
                else:
                    if jackConditionals[note.lane][2] in allowedLanes:
                        #Check if theres a shield that needs to be preserved
                        if shieldConditionals[note.lane][3] in allowedLanes and shieldConditionals[note.lane][2] < maxShield and shieldConditionals[note.lane][1] + shieldIntervalTime >= note.startTime: #Theres a shield and we're not at maxShield yet
                            laneChoice = shieldConditionals[note.lane][3]
                            shieldConditionals[note.lane][2] += 1
                        else: 
                            laneChoice = allowedLanes[(allowedLanes.index(jackConditionals[note.lane][2])+1)%len(allowedLanes)]
                            shieldConditionals[note.lane][2] = 0
                    else:
                        #Check if theres a shield that needs to be preserved
                        if shieldConditionals[note.lane][3] in allowedLanes and shieldConditionals[note.lane][2] < maxShield and shieldConditionals[note.lane][1] + shieldIntervalTime >= note.startTime: #Theres a shield and we're not at maxShield yet
                            laneChoice = shieldConditionals[note.lane][3]
                            shieldConditionals[note.lane][2] += 1
                        else:
                            for choice in allowedLanes:
                                if choice > jackConditionals[note.lane][2]:
                                    laneChoice = choice
                                    break
                                if choice == allowedLanes[-1]:
                                    laneChoice = allowedLanes[0]
                            shieldConditionals[note.lane][2] = 0
                    jackConditionals[note.lane][0] = note.startTime
                    jackConditionals[note.lane][1] = 1
                    jackConditionals[note.lane][2] = laneChoice
                    newNote = note.newNoteInLane(laneChoice)
                    outObjects.append(newNote)

                #If we just mapped a long note that meets the shield threshold, update the shield conditionals for the corresponding input lane
                if note.isLN() and note.endTime - note.startTime >= shieldThresholdTime:
                    shieldConditionals[note.lane][3] = laneChoice
                    shieldConditionals[note.lane][0] = note.startTime
                    shieldConditionals[note.lane][1] = note.endTime
                else:
                    shieldConditionals[note.lane][2] = 0

                #Set restrictions for future notes based on where this note was placed
                if note.isRice():
                    occupiedIntervals[laneChoice].append([note.startTime-2, note.startTime + unjackTime, note.lane])
                elif note.isLN():
                    if note.startTime + unjackTime >= note.endTime + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note.startTime, note.startTime + unjackTime, note.lane])
                    elif note.startTime + unjackTime < note.endTime + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note.startTime, note.endTime + (beatLength * minShieldInterval), note.lane])
    #if conversionMode == 'jack_alternate_random':
    #if conversionMode == 'block_alternate':
    #if conversionMode == 'block_alternate_random':

    if buffAmount > 0:
        extraOutObjects = []
        buffThreshold = 1.0
        for note in outObjects:
            for point in points:
                if float(point[1]) <= note.startTime:
                    beatLength = float(point[1])
                    #print(beatLength)
                else:
                    beatLength = 150.0

            #Set the unjack time interval (ms) based on the BPM if unjack is true
            if unjack == '1':
                unjackTime = (unjackInterval * beatLength) + 2
            else:
                unjackTime = 0

            #HitObject format: [lane startTime noteType hitSound endTime sample]

            possibleBuffLanes = []
            for row in newConversionKey:
                #print(row)
                if note.lane in row:
                    possibleBuffLanes = possibleBuffLanes + row
            possibleBuffLanes = [*set(possibleBuffLanes)]
            #print(possibleBuffLanes)
            random.Random(1).shuffle(possibleBuffLanes)
            
            for possibility in possibleBuffLanes:
                print(buffThreshold)
                okay = True
                for interval in occupiedIntervals[possibility]:
                    if note.isRice():
                        if note.startTime >= interval[0] - unjackTime and note.startTime <= interval[1]:
                            okay = False
                            break
                    elif note.isLN():
                        if (note.startTime >= interval[0] - unjackTime and note.startTime <= interval[1]) or (note.endTime >= interval[0] and note.endTime <= interval[1]):
                            okay = False
                            break

                if okay:
                    if note.isRice():
                        if buffThreshold >= 1:
                            newNote = note.newNoteInLane(possibility)
                            extraOutObjects.append(newNote)
                            #print(newNote)
                            buffThreshold -= 1.0
                        else:
                            buffThreshold += buffAmount
                    occupiedIntervals[possibility].append([note.startTime, note.startTime + unjackTime, -1]) #add an occupied interval regardless if a note is added or not because there might be future attempts to buff this spot.

                    #Repeat but with long notes
                    elif note.isLN():
                        if buffThreshold >= 1:
                            newNote = note.newNoteInLane(possibility)
                            extraOutObjects.append(newNote)
                            #print(newNote)
                            buffThreshold -= 1.0
                        else:
                            buffThreshold += buffAmount
                    occupiedIntervals[possibility].append([note.startTime, note.endTime + beatLength * minShieldInterval, -1])
        outObjects = outObjects + extraOutObjects

        #outObjects.sort(key=lambda x: x[0])
        #outObjects.sort(key=lambda x: x[1])

    return outObjects