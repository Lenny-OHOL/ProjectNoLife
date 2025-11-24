from bot_core.player_info import PlayerInfo
from bot_core.server_connect import Server

class BasicAction:
    """
        A class containing the basic actions a bot will send to the server.
        It currently includes die, mother, move, self, drop, use and say
    """
    actions = [
        'die',
        'mother',
        'move',
        'self',
        'drop',
        'use',
        'say'
    ]
    directions = {
        'up':'0 1',
        'left':'-1 0',
        'center':'0 0',
        'right':'1 0',
        'down':'0 -1'
    }
    def __init__(self, Server:Server, player_info:PlayerInfo, message_feed):
        self.Server = Server
        self.player_info = player_info
        self.message_feed = message_feed

    def __call__(self, command, *args, **kwargs):
        if command in BasicAction.actions:
            if args or kwargs:
                getattr(self, command)(*args, **kwargs)
            else:
                getattr(self, command)()
        else:
            self.action_not_found()


    #baby /die command. Must be less than 3 years old to work
    def die(self):
        self.Server(f'DIE {self.player_info.x} {self.player_info.y}#')

    #Passing a drop command with -1 will drop the item on the tile instead of a body part
    #If you dont have a backpack, and you set your body_slot = 5, it will do nothing
    #Dropping items on a tile will do the following beviors:
    #1) Check if tile is empty, if empty, place the item on the empty tile. If not empty, swap the item in hand with empty tile
    #
    def drop(self, direction='center', body_slot='-1'):
        add_x, add_y = [int(item) for item in BasicAction.directions[direction].split(' ')]
        
        self.Server(f'DROP {int(self.player_info.x) + add_x} {int(self.player_info.y + add_y)} {body_slot}#')

    def mother(self):
        self.Server(f'MOTH {self.player_info.x} {self.player_info.y}#')

    def move(self, direction='center'):
        self.Server(f'MOVE {self.player_info.x} {self.player_info.y} @{self.player_info.moveStep} {BasicAction.directions[direction]}#')

    #Self is used to feed player and place clothes on player
    # You can use the body_slot = -1 to place clothes as well
    # 2 is used for the front shoe, and 3 is used for the back shoe, however, when adding boots, the back shoe is always added first no matter what
    # when swapping shoes, the front shoe is prioritized first compared to the back shoe
    def self(self, body_slot='-1'):
        self.Server(f'SELF {self.player_info.x} {self.player_info.y} {body_slot}#')
    
    def use(self, direction='center'):
        add_x, add_y = [int(item) for item in BasicAction.directions[direction].split(' ')]
        
        self.Server(f'USE {int(self.player_info.x) + add_x} {int(self.player_info.y + add_y)}#')
        #if item_slot:
        #    self.Server(f'SELF {self.player_info.x} {self.player_info.y} {item_slot}#')
        #else:
        #    self.Server(f'SELF {self.player_info.x} {self.player_info.y}#')

    def say(self, message='F'):
        self.Server(f'SAY {self.player_info.x} {self.player_info.y} {message.upper()}#')

    def action_not_found(self):
        self.message_feed.append('Action not found')



'''
Weird Quirks of Jasons Code:

When adding items into clothing containers. Both the drop and self command will put items into clothing containers on the person. The 
ingame client uses key bindings while the default game uses self when you click on a particular clothing item



List of actions and their completions

KA x y#
USE x y id i#
BABY x y#
BABY x y id#
SELF x y i# 100%
UBABY x y i#
UBABY x y i id#
REMV x y i#
SREMV x y c i#
DROP x y c#
SWAP x y#
KILL x y#
KILL x y id#
JUMP x y#
EMOT x y e#
DIE x y#
GRAVE x y#
OWNER x y#
FORCE x y#
PING x y unique_id#
VOGS x y#
VOGN x y#
VOGP x y#
VOGM x y#
VOGI x y id#
VOGT x y text# 
VOGX x y#
PHOTO x y seq#
PHOID x y photo_id_string#
LEAD x y#
UNFOL x y#
PROP x y#
ORDR x y#
FLIP x y#
MOTH X Y# : 100%
APVT x y github_username#


'''