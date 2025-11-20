from pathlib import Path


class OHOLObject:
    def __init__(self, id, description, containable = 0, blocksWalking = 0, numUses = 0, foodValue = 0):
        self.id = id
        self.description = description
        self.containable = containable
        self.blocksWalking = blocksWalking
        self.numUses = numUses
        self.foodValue = foodValue



class objectBank:
    """
    A map to quickly identify objects given an Id the server will send to an account
    """
    def __init__(self) -> None:
        #Maps Ids to OHOL objects
        self.IdMap: dict[int,OHOLObject] = {}

        #The words that we only care about
        self.keyWords = ('containable', 'blocksWalking', 'numUses', 'foodValue')

        self.nextObjectNumber = 0

        #Counters:
        self.uniqueObjectsCount = 0
        self.totalObjectsCount = 0
        self.loadObjects()
        self.generateObjectStages()

    def loadObjects(self):
        for file in Path('resources/objects').iterdir():
            if file.name == 'nextObjectNumber.txt':
                self.nextObjectNumber = int(file.open('r').read())
            elif file.name.split('.')[0].isdigit():
                g = file.open('r').read().splitlines()
                object = OHOLObject(g[0].split('=')[1], g[1])
                
                properties = [i for i in g if i.startswith(self.keyWords)]
                object.containable = int(properties[0].split('=')[1])
                object.blocksWalking = int(properties[1].split('=')[1].split(',')[0])
                object.foodValue = int(properties[2].split('=')[1])
                object.numUses = int(properties[3].split('=')[1].split(',')[0])

                self.IdMap[int(object.id)] = object
                self.uniqueObjectsCount += 1

    def generateObjectStages(self):
        #Damn, this shits advanced. I have to pull out sorted maps to solve this
        self.totalObjectsCount = self.uniqueObjectsCount
        newObjects = {}
        for id in sorted(self.IdMap):
            if self.IdMap[id].numUses > 1:
                for i in range(1, self.IdMap[id].numUses):
                    newObject = OHOLObject(str(self.nextObjectNumber), self.IdMap[id].description, self.IdMap[id].containable, self.IdMap[id].blocksWalking, i, self.IdMap[id].foodValue)
                    newObjects[self.nextObjectNumber] = newObject
                    self.nextObjectNumber += 1
                    self.totalObjectsCount += 1



        self.IdMap.update(newObjects)
        del newObjects
