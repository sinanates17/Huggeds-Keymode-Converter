class Note:
    def __init__(self, lane, startTime, noteType, hitsound, endTime, sample):
        self.lane = lane
        self.startTime = startTime
        self.noteType = noteType
        self.hitsound = hitsound
        self.endTime = endTime
        self.sample = sample
    
    def __repr__(self):
    	return str(self.__dict__)

    def newNoteInLane(self, lane):
    	return Note(lane, self.startTime, self.noteType, self.hitsound, self.endTime, self.sample)
        
    def isRice(self):
        return self.noteType != '128'

    def isLN(self):
        return self.noteType == '128'
