import os
import configparser
import convert
import parsing
import pip._vendor.requests as requests

#Check if the current verison is up to date, if so, ask the user if they want to auto update
currentVersion = "osu" #Change this line every time a new release is made
url = "http://github.com/sinanates17/Huggeds-Keymode-Converter/releases/latest"
r = requests.get(url, allow_redirects=True)
latestVersion = r.url.split('/')[-1]

if currentVersion != latestVersion:
    choice = input("A new release is available, would you like to update? (\"yes\" or \"no\")")
    while choice != "yes" and choice != "no":
        choice = input("\"yes\" or \"no\"")
    if choice == "yes":
        from update import updater
        import sys
        updater(latestVersion)
        input()
        sys.exit()
    elif choice == "no":
        pass                              
                        
# Parse the config
cfg = configparser.ConfigParser(allow_no_value=True)
cfg.read('config.ini')

changeAuthor = cfg['Metadata'].get('change_author')
if changeAuthor == '': changeAuthor = None
changeHP = cfg['Metadata'].get('change_hp')
if changeHP == '': changeHP = None
changeOD = cfg['Metadata'].get('change_od')
if changeOD == '': changeOD = None

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

# Loop through every difficulty in the Input folder and create converts in the Output folder
for i,beatmap in enumerate(beatmaps):
    #Print progress
    print(f'Converting map {i+1}/{len(beatmaps)} | {beatmap.strip(".osu")}')

    # Parse the map for its stuff
    with open(inputDirectory + beatmap, "r", encoding="utf8") as f:
        inputKeymode, redPoints, hitObjects, outputHead = parsing.parseMap(f, changeAuthor, changeHP, changeOD)

    # Parse the conversion key
    conversionKey = parsing.parseConversionKey(cfg['Conversion Keys'], inputKeymode, outputKeymode)

    # Pass all of the timing points, hit objects, and configurable paramaters into the 'convert' method, which returns a list containing all of the hit objects for the output file
    newHitObjects = convert.convertMap(hitObjects, redPoints, inputKeymode, outputKeymode, conversionMode, alternateInterval, maxJack, unjack, unjackInterval, minShieldInterval, conversionKey, shieldPreserver, shieldThreshold, shieldPreserverInterval, maxShield, buffAmount)

    # Start writing metadata into the output difficulty
    filename = beatmap[0:-4] + " To " + str(outputKeymode) + "K.osu" #Set the filename for the converted difficulty
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

input("Done! Press enter to exit.")
