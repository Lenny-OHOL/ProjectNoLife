class RawInfo:
    """
    Used for easily storing player information in the dictionary when given the LifeID
    """
    def __init__(self, PU = [], name = '') -> None:
        self.PU = PU
        self.name = name

class PlayerInfo:
    def __init__(self) -> None:
        self.botID = '' # this will be the display name used for the bot in the bot display

        self.status = 'ALIVE' #This can either be ALIVE, GHOST, OR DEAD
        self.is_alive = True
        self.is_ghost = False
        self.LifeID = 0 #Number used to tell which player you are on the server
        self.playerObjectID = 0 #This is the number used to determine which character model you get based on age and race

        #Food 
        self.food = 0
        self.food_capacity = 0
        self.last_ate_id = 0
        self.last_ate_fill_max = 0

        self.mothers_name = ''
        self.name = ''

        #Heat
        self.heat = ''
        self.food_time = ''
        self.indoor_bonus = ''

        #Player Position from birth
        self.x = 0
        self.y = 0
        self.moveStep = 1

    def _update_player_info(self, player:RawInfo):
        self.name = player.name
        self.playerObjectID = player.PU[1]
        self.heat = player.PU[11]

        #X Y position changes to X upon death
        if not player.PU[14] == 'X':
            self.x, self.y = int(player.PU[14]), int(player.PU[15])