import random, math
from settings import *

def randomPositions(epuckPosition, robotIDs):
    translations = {}
    search = 1
    while search:
        for ID in robotIDs:
            translations[ID] = [random.uniform(-arenaSize, arenaSize), 0.01, random.uniform(-arenaSize, arenaSize)]
        search = 0
    
        for ID1 in robotIDs:
            epuck_distance = math.sqrt(((translations[ID1][0] - epuckPosition[0])**2 + (translations[ID1][2] - epuckPosition[2])**2))
            for ID2 in robotIDs:
                distance = math.sqrt((translations[ID1][0] - translations[ID2][0])**2 + (translations[ID1][2] - translations[ID2][2])**2)    
                if distance != 0 and (distance < objectMinimumDistance or epuck_distance < objectMinimumDistance):
                    search = 1

    keys = list(translations.keys())
    values = list(translations.values())
    random.shuffle(values)
    
    shuffled_translations = dict()
    i=0
    while i < len(keys):
        shuffled_translations.update({keys[i]: values[i]})
        i+=1

    return shuffled_translations
    
def deleteObjects(self):
    IDs = []
    for ID in self.activeRobots:
        IDs += [ID]
    for ID in IDs:
        if ID != "e-puck":
            self.deleteRobot(ID)