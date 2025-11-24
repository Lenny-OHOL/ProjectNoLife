import time
import zlib
from threading import Thread
from pathlib import Path

#My libraries
from bot_core.server_connect import Server
from bot_core.player_info import PlayerInfo 
from bot_core.bot_display import BotDisplay
from bot_core.basic_action import BasicAction

# botMethods.objectId as objectId

class botActions(BasicAction, PlayerInfo, BotDisplay):
    """
    The core bot utilities class a bot will need to handle server messages from an OHOL server. It coontains the following options:
    Server Message Decompression and Storage, Talking, BasicMovement, and player updates
    """
    def __init__(self, *args, show_display=True, **kwargs):
        PlayerInfo.__init__(self)

        #Used to turn on and off the recvBytes
        self.working = True

        #Used for individualized bot display
        self.show_display = show_display

        #Starting Bot
        self.Server = Server(*args, **kwargs, PlayerInfo=self)
        #Basic Actions
        BasicAction.__init__(self, self.Server, self, self.Server.message_feed)
        BotDisplay.__init__(self, message_feed=self.Server.message_feed)
        self.addBot(self)
        self.start()

        if show_display:
            t2 = Thread(target=self._update_display)
            t2.start()

    def start(self):
        t = Thread(target=self.manage_bytes)
        t.start()


        #Gathering LifeId
        self.Server.message_feed.append('forcing PU')
        self('mother')

    def stop(self):
        self.working = False
        self.show_display = False
        self.Server.disconnect()
        print('finished stopping sequence')

    def stop_display(self):
        self.showDisplay = False
    
    def _update_display(self):
        while self.show_display:
            time.sleep(1)
            self.update_display()       

    def manage_bytes(self):
        while self.status == 'ALIVE' and self.working:

            self.Server._recieve_bytes()

            #if theres a message needing to be processed
            if self.Server.server_message_buffer:
                self.Server.messageDecompression(self.Server.server_message_buffer)
        
        #Death Sequence:
        self.stop()