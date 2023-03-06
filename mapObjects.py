# Defines a single note
class Note:
    def __init__(self, lane, startTime, noteType, hitSound, endTime, sample):
        self.lane = lane
        self.startTime = startTime
        self.noteType = noteType
        self.hitSound = hitSound
        self.endTime = endTime
        self.sample = sample
        if self.isLN():
            self.length = endTime - startTime
        else:
            self.length = 0
    
    # Define representation so you can do print(note)
    def __repr__(self):
        return str(self.__dict__)
            
    # Lets you do str(note) to get the output of how it should be in the .osu file
    # !! Currently doesnt work correctly !!
    '''
    def __str__(self):
        return f'{self.lane},192,{self.startTime},{self.noteType},{self.hitSound},{self.endTime}{self.sample}'
    '''

    # Returns a clone of the note in a different lane
    def copyToLane(self, lane):
        return Note(lane, self.startTime, self.noteType, self.hitSound, self.endTime, self.sample)
    
    # Functions to check if it is rice or ln
    def isRice(self):
        return self.noteType != '128'

    def isLN(self):
        return self.noteType == '128'
    
    # Functions to check whether this note forms a jack or a shield with another note
    def isJacked(self, other, threshold):
        return (self.startTime >= other.startTime and self.startTime <= other.startTime + threshold) and (self.lane == other.lane)

    def isShielded(self, other, capThreshold, bodyThreshold):
        return (other.isLN()) and (other.length >= bodyThreshold) and (self.startTime <= other.endTime + capThreshold and self.startTime >= other.endTime) and (self.lane == other.lane)
        #      ^Preceding note must be LN  ^Preceding LN needs to be long enough   ^This note is within the "shield window" of the previous note

    # Lets you create a note from a string
    @classmethod
    def fromString(cls, noteString, keymode):
        # Get properties of note
        properties = noteString.split(",")

        lane = int(int(properties[0])/(512/keymode))
        startTime = int(properties[2])
        noteType = properties[3]
        hitSound = properties[4]
        endTime = int(properties[5].split(':')[0])
        sample = properties[5]
        sample = sample[sample.find(':'):-1]

        # Create note with properties
        return cls(lane, startTime, noteType, hitSound, endTime, sample)

# Defines a timing point
class TimingPoint:
    def __init__(self, time, beatLength, meter, sampleSet, sampleIndex, volume, uninherited, effects):
        self.time = time 
        self.beatLength = beatLength 
        self.meter = meter 
        self.sampleSet = sampleSet 
        self.sampleIndex = sampleIndex 
        self.volume = volume
        self.uninherited = uninherited
        self.effects = effects

    # Define representation so you can do print(point)
    def __repr__(self):
        return str(self.__dict__)

    # Lets you create a timing point from a string
    @classmethod
    def fromString(cls, noteString):
        properties = noteString.split(',')
        # Convert uninheritedness to bool
        properties[6] = False if properties[6] == '0' else True
        # Wow timing point~!
        return cls(*properties)

# Defines an interval between notes
class Interval:
    def __init__(self, startTime, endTime, originLane):
        self.startTime = startTime
        self.endTime = endTime
        self.originLane = originLane

    # Define representation so you can do print(interval)
    def __repr__(self):
        return str(self.__dict__)

# Defines a chord of multiple notes
class Chord:
    def __init__(self):
        self.threshold = 30
        self.startTime = None
        self.endTime = None
        self.notes = []
        self.size = 0
        
    # Define representation so you can do print(chord)
    def __repr__(self):
        return str(self.__dict__)

    # Add a Note object into the chord's notes list
    def addNote(self, note):
        # Check if note is earliest
        if self.startTime is None or note.startTime < self.startTime:
            self.startTime = note.startTime
            self.endTime = note.startTime + self.threshold

        # Add note to chord
        self.notes.append(note)
        self.size += 1
