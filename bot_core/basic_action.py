from typing import Any, Literal
from bot_core.player_info import PlayerInfo
from bot_core.server_connect import Server

class BasicAction:
    actions = [
        'move',
        'self',
        'drop',
        'use'
    ]
    directions = {
        'up':'0 1',
        'left':'-1 0',
        'center':'0 0',
        'right':'1 0',
        'down':'0 -1'
    }
    def __init__(self, Server:Server, player_info, messageFeed):
        self.Server = Server
        self.player_info:PlayerInfo = player_info
        self.messageFeed = messageFeed

    def __call__(self, command, direction='center'):
        if command in BasicAction.actions and direction in BasicAction.directions:
            getattr(self, command)(direction)
        else:
            self.action_not_found()


    def move(self, direction):
        self.Server(f'MOVE {self.player_info.x} {self.player_info.y} @{self.player_info.moveStep} {BasicAction.directions[direction]}#')
    
    def action_not_found(self):
        self.messageFeed.append('Action not found')