class PlayerInfo:
    def __init__(self) -> None:
        self.botID = '' # this will be the display name used for the bot in the bot display

        self.status = 'ALIVE' #This can either be ALIVE, GHOST, OR DEAD
        self.LifeID = 0 #Number used to tell which player you are on the server
        self.playerObjectID = 0 #This is the number used to determine which character model you get based on age and race

        #Food 
        self.food = 0
        self.foodCapacity = 0
        self.last_ate_id = 0
        self.last_ate_fill_max = 0

        self.mothersName = ''
        self.name = ''

        #Heat
        self.heat = ''
        self.food_time = ''
        self.indoor_bonus = ''

        #Player Position from birth
        self.x = 0
        self.y = 0
        self.moveStep = 1

class RawInfo:
    """
    Used for easily storing player information in the dictionary when given the LifeID
    """
    def __init__(self, PU = [], name = '') -> None:
        self.PU = PU
        self.name = name