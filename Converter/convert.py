import random

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

            #Establish what the current beatLength is
            for point in points:
                if float(point[1]) <= note[1]:
                    beatLength = float(point[1])
                    #print(beatLength)
                else:
                    beatLength = 150.0

            #Set the unjack time interval (ms) based on the BPM if unjack is true
            if unjack == '1':
                unjackTime = (unjackInterval * beatLength) + 2
            else:
                unjackTime = 0

            #Figure out what lanes are allowed for this note based on allowedLanes and restrictions from other placed notes (e.g within the unjack interval of another note or overlapping with other notes)
            possibleLanes = newConversionKey[note[0]]
            allowedLanes = []

            #For every lane this note can be placed on based on the coversion key, check if the lane is available by making sure there are no occupied invervals at this time point that have a different origin lane.
            for outputLane in possibleLanes:
                okay = True
                for interval in occupiedIntervals[outputLane]:
                    if note[2] == '1':
                        if note[1] >= interval[0] and note[1] <= interval[1] and interval[2] != note[0]: 
                            okay = False
                    if note[2] == '128':
                        if (note[1] >= interval[0] and note[1] <= interval[1] and interval[2] != note[0]) or (note[4] >= interval[0] and note[4] <= interval[1] and interval[2] != note[0]): 
                            okay = False
                if okay:
                    allowedLanes.append(outputLane)

            #Choose a lane to place this note on. If there are no available lanes, don't place a note.
            if allowedLanes: #Empty lists are false. Only map this note if there are available lanes
                laneChoice = random.choice(allowedLanes)
                #print(allowedLanes)
                outObjects.append([laneChoice, note[1], note[2], note[3], note[4], note[5]]) #[lane startTime noteType hitSound endTime sample]

                #Set restrictions for future notes based on where this note was placed
                if note[2] == '1':
                    occupiedIntervals[laneChoice].append([note[1], note[1] + unjackTime, note[0]])
                elif note[2] == '128':
                    if note[1] + unjackTime >= note[4] + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note[1], note[1] + unjackTime, note[0]])
                    elif note[1] + unjackTime < note[4] + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note[1], note[4] + (beatLength * minShieldInterval) - 2, note[0]])

    if conversionMode == 'random_nojack':
        noJackLanes = [-1 for i in range(inMode)]
        occupiedIntervals = [[] for i in range(outMode)] #Contains a list of intervals in [startTime endTime originLane] format for EVERY output column where future notes CANNOT be placed
        for note in inObjects:
            #print(note)

            #Establish what the current beatLength is
            for point in points:
                if float(point[1]) <= note[1]:
                    beatLength = float(point[1])
                    #print(beatLength)
                else:
                    beatLength = 150.0

            #Set the unjack time interval (ms) based on the BPM if unjack is true
            if unjack == '1':
                unjackTime = (unjackInterval * beatLength) + 2
            else:
                unjackTime = 0

            #Figure out what lanes are allowed for this note based on allowedLanes and restrictions from other placed notes (e.g within the unjack interval of another note or overlapping with other notes)
            possibleLanes = newConversionKey[note[0]]
            allowedLanes = []

            #For every lane this note can be placed on based on the coversion key, check if the lane is available by making sure there are no occupied invervals at this time point that have a different origin lane.
            for outputLane in possibleLanes:
                okay = True
                for interval in occupiedIntervals[outputLane]:
                    if note[2] == '1':
                        if note[1] >= interval[0] and note[1] <= interval[1] and interval[2] != note[0]: 
                            okay = False
                    if note[2] == '128':
                        if (note[1] >= interval[0] and note[1] <= interval[1] and interval[2] != note[0]) or (note[4] >= interval[0] and note[4] <= interval[1] and interval[2] != note[0]): 
                            okay = False
                if len(possibleLanes) > 1:
                    if outputLane == noJackLanes[note[0]]:
                        okay = False
                if okay:
                    allowedLanes.append(outputLane)

            #Choose a lane to place this note on. If there are no available lanes, don't place a note.
            if allowedLanes: #Empty lists are false. Only map this note if there are available lanes
                laneChoice = random.choice(allowedLanes)
                #print(allowedLanes)
                outObjects.append([laneChoice, note[1], note[2], note[3], note[4], note[5]]) #[lane startTime noteType hitSound endTime sample]

                #Set restrictions for future notes based on where this note was placed
                if note[2] == '1':
                    occupiedIntervals[laneChoice].append([note[1], note[1] + unjackTime, note[0]])
                elif note[2] == '128':
                    if note[1] + unjackTime >= note[4] + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note[1], note[1] + unjackTime, note[0]])
                    elif note[1] + unjackTime < note[4] + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note[1], note[4] + (beatLength * minShieldInterval), note[0]])
                
                noJackLanes[note[0]] = laneChoice

    if conversionMode == 'jack_alternate':
        occupiedIntervals = [[] for i in range(outMode)] #Contains a list of intervals in [startTime endTime originLane] format for EVERY output column where future notes CANNOT be placed
        jackConditionals = [[-10000, maxJack,-1] for i in range(inMode)] #Format: [time, currentJackCount, currentOutLane]. Every input lane has a conditional that determines if the next note from that lane will be jacked.
        shieldConditionals = [[-10000, -10000, maxShield,-1] for i in range(inMode)] #Format: [headTime, tailTime currentShieldCount, currentOutLane]. Every input lane has a conditional that determines if the next note from that lane will be shielded
        for note in inObjects:
            #print(note)

            #Establish what the current beatLength is
            for point in points:
                if float(point[1]) <= note[1]:
                    beatLength = float(point[1])
                    #print(beatLength)
                else:
                    beatLength = 150.0

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
            possibleLanes = newConversionKey[note[0]]
            allowedLanes = []

            #For every lane this note can be placed on based on the coversion key, check if the lane is available by making sure there are no occupied invervals at this time point that have a different origin lane.
            for outputLane in possibleLanes:
                okay = True
                for interval in occupiedIntervals[outputLane]:
                    if note[2] == '1':
                        if note[1] >= interval[0] and note[1] <= interval[1] and interval[2] != note[0]: 
                               okay = False
                    if note[2] == '128':
                        if (note[1] >= interval[0] and note[1] <= interval[1] and interval[2] != note[0]) or (note[4] >= interval[0] and note[4] <= interval[1] and interval[2] != note[0]): 
                            okay = False
                if okay:
                    allowedLanes.append(outputLane)

            #Choose an output lane based on the jack conditionals
            if allowedLanes: #Empty lists are falsy
                #Maximum jacks for an output column has been reached and its time to switch to the next column
                if (jackConditionals[note[0]][1] == maxJack) and jackConditionals[note[0]][2] in allowedLanes:
                    laneChoice = allowedLanes[(allowedLanes.index(jackConditionals[note[0]][2])+1)%len(allowedLanes)]
                    jackConditionals[note[0]][0] = note[1]
                    jackConditionals[note[0]][1] = 1 
                    jackConditionals[note[0]][2] = laneChoice
                    outObjects.append([laneChoice, note[1], note[2], note[3], note[4], note[5]]) #[lane startTime noteType hitSound endTime sample]

                #Within the jack interval and placing another jack is available
                elif (jackConditionals[note[0]][0] + (alternateInterval * beatLength) > note[1]) and jackConditionals[note[0]][2] in allowedLanes:
                    laneChoice = jackConditionals[note[0]][2]
                    jackConditionals[note[0]][0] = note[1]
                    jackConditionals[note[0]][1] += 1
                    jackConditionals[note[0]][2] = laneChoice
                    outObjects.append([laneChoice, note[1], note[2], note[3], note[4], note[5]]) #[lane startTime noteType hitSound endTime sample]

                #Either we're out of the jack interval or placing another jack isn't available
                else:
                    if jackConditionals[note[0]][2] in allowedLanes:
                        #Check if theres a shield that needs to be preserved
                        if shieldConditionals[note[0]][3] in allowedLanes and shieldConditionals[note[0]][2] < maxShield and shieldConditionals[note[0]][1] + shieldIntervalTime >= note[1]: #Theres a shield and we're not at maxShield yet
                            laneChoice = shieldConditionals[note[0]][3]
                            shieldConditionals[note[0]][2] += 1
                        else: 
                            laneChoice = allowedLanes[(allowedLanes.index(jackConditionals[note[0]][2])+1)%len(allowedLanes)]
                            shieldConditionals[note[0]][2] = 0
                    else:
                        #Check if theres a shield that needs to be preserved
                        if shieldConditionals[note[0]][3] in allowedLanes and shieldConditionals[note[0]][2] < maxShield and shieldConditionals[note[0]][1] + shieldIntervalTime >= note[1]: #Theres a shield and we're not at maxShield yet
                            laneChoice = shieldConditionals[note[0]][3]
                            shieldConditionals[note[0]][2] += 1
                        else:
                            for choice in allowedLanes:
                                if choice > jackConditionals[note[0]][2]:
                                    laneChoice = choice
                                    break
                                if choice == allowedLanes[-1]:
                                    laneChoice = allowedLanes[0]
                            shieldConditionals[note[0]][2] = 0
                    jackConditionals[note[0]][0] = note[1]
                    jackConditionals[note[0]][1] = 1
                    jackConditionals[note[0]][2] = laneChoice
                    outObjects.append([laneChoice, note[1], note[2], note[3], note[4], note[5]]) #[lane startTime noteType hitSound endTime sample]

                #If we just mapped a long note that meets the shield threshold, update the shield conditionals for the corresponding input lane
                if note[2] == '128' and note[4] - note[1] >= shieldThresholdTime:
                    shieldConditionals[note[0]][3] = laneChoice
                    shieldConditionals[note[0]][0] = note[1]
                    shieldConditionals[note[0]][1] = note[4]
                else:
                    shieldConditionals[note[0]][2] = 0

                #Set restrictions for future notes based on where this note was placed
                if note[2] == '1':
                    occupiedIntervals[laneChoice].append([note[1], note[1] + unjackTime, note[0]])
                elif note[2] == '128':
                    if note[1] + unjackTime >= note[4] + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note[1], note[1] + unjackTime, note[0]])
                    elif note[1] + unjackTime < note[4] + (beatLength * minShieldInterval):
                        occupiedIntervals[laneChoice].append([note[1], note[4] + (beatLength * minShieldInterval), note[0]])
    #if conversionMode == 'jack_alternate_random':
    #if conversionMode == 'block_alternate':
    #if conversionMode == 'block_alternate_random':

    if buffAmount > 0:
        extraOutObjects = []
        buffThreshold = 1.0
        for note in outObjects:
            for point in points:
                if float(point[1]) <= note[1]:
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
                if note[0] in row:
                    possibleBuffLanes = possibleBuffLanes + row
            possibleBuffLanes = [*set(possibleBuffLanes)]
            #print(possibleBuffLanes)
            random.Random(1).shuffle(possibleBuffLanes)
            
            for possibility in possibleBuffLanes:
                print(buffThreshold)
                okay = True
                for interval in occupiedIntervals[possibility]:
                    if note[2] == '1':
                        if note[1] >= interval[0] - unjackTime and note[1] <= interval[1]:
                            okay = False
                            break
                    if note[2] == '128':
                        if (note[1] >= interval[0] - unjackTime and note[1] <= interval[1]) or (note[4] >= interval[0] and note[4] <= interval[1]):
                            okay = False
                            break

                if okay:
                    if note[2] == '1':
                        if buffThreshold >= 1:
                            extraOutObjects.append([possibility, note[1], note[2], note[3], note[4], note[5]])
                            print([possibility, note[1], note[2], note[3], note[4], note[5]])
                            buffThreshold -= 1.0
                        else:
                            buffThreshold += buffAmount
                    occupiedIntervals[possibility].append([note[1], note[1] + unjackTime, -1]) #add an occupied interval regardless if a note is added or not because there might be future attempts to buff this spot.

                    #Repeat but with long notes
                    if note[2] == '128':
                        if buffThreshold >= 1:
                            extraOutObjects.append([possibility, note[1], note[2], note[3], note[4], note[5]])
                            #print([possibility, note[1], note[2], note[3], note[4], note[5]])
                            buffThreshold -= 1.0
                        else:
                            buffThreshold += buffAmount
                    occupiedIntervals[possibility].append([note[1], note[4] + beatLength * minShieldInterval, -1])
        outObjects = outObjects + extraOutObjects

        #outObjects.sort(key=lambda x: x[0])
        #outObjects.sort(key=lambda x: x[1])

    return outObjects