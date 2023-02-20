# Defines a single note
class Note:
    def __init__(self, lane, startTime, noteType, hitsound, endTime, sample):
        self.lane = lane
        self.startTime = startTime
        self.noteType = noteType
        self.hitsound = hitsound
        self.endTime = endTime
        self.sample = sample
    
    # Define representation so you can do print(note)
    def __repr__(self):
    	return str(self.__dict__)

    # Lets you do str(note) to get the output of how it should be in the .osu file
    def __str__(self):
        return f'{note.lane},192,{note.startTime},{note.noteType},{note.hitsound},{note.endTime}{note.sample}'

    # Function that returns a clone of the note in a different lane
    def newNoteInLane(self, lane):
    	return Note(lane, self.startTime, self.noteType, self.hitsound, self.endTime, self.sample)
  
    # Functions to check if it is rice or ln
    def isRice(self):
        return self.noteType != '128'

    def isLN(self):
        return self.noteType == '128'

# Defines a timing point
class TimingPoint:
    def __init__(self, time, beatLength, meter, sampleSet, sampleIndex, volume, uninherited, effects):
        self.time = time 
        self.beatLength = beatLength 
        self.meter = meter 
        self.sampleSet = sampleSet 
        self.sampleIndex = sampleIndex 
        self.volume = volume
        # Convert inheritedness to bool
        self.uninherited = False if uninherited == '0' else True
        self.effects = effects

    # Define representation so you can do print(point)
    def __repr__(self):
        return str(self.__dict__)

# Defines an interval, YET TO BE IMPLEMENTED
class Interval:
    def __init__(self, startTime, endTime, originLane):
        self.startTime = startTime
        self.endTime = endTime
        self.originLane = originLane

    # Define representation so you can do print(interval)
    def __repr__(self):
        return str(self.__dict__)
