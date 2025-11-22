import time
import zlib
from threading import Thread
from pathlib import Path

#My libraries
from bot_core.server_connect import Server
from bot_core.player_info import (PlayerInfo, RawInfo) 
from bot_core.bot_display import BotDisplay
from bot_core.basic_action import BasicAction

# botMethods.objectId as objectId

#non-compressed message types
cmdBank = (b'ACCEPTED\n', b'AD\n', b'AP\n', b'BB\n', b'BW\n', b'CR\n', b'CS\n', b'CU\n', b'CX\n', b'DY\n', b'EX\n', b'FD\n', b'FL\n', b'FW\n', b'FX\n', b'GH\n', b'GM\n', b'GO\n', b'GV\n', b'HE\n', b'HL\n', b'HX\n', b'LN\n', b'LR\n', b'LS\n', b'MN\n', b'MS\n', b'MX\n', b'NM\n', b'OW\n', b'PE\n', b'PH\n', b'PJ\n', b'PM\n', b'PO\n', b'PS\n', b'PU\n', b'RA\n', b'RR\n', b'SD\n', b'SN\n', b'TS\n', b'VS\n', b'VU\n', b'WR\n')

class botActions(PlayerInfo, BotDisplay):
    """
    The core bot utilities class a bot will need to handle server messages from an OHOL server. It coontains the following options:
    Server Message Decompression and Storage, Talking, BasicMovement, and player updates
    """
    def __init__(self, *args, show_display=True, **kwargs):
        PlayerInfo.__init__(self)

        self.messageBuffer = []

        BotDisplay.__init__(self)
        self.addBot(self)

        #stored map info
        self.map = {}

        #Stored Players
        self.players: dict[int, RawInfo] = {}

        #Message Feed that will be used by the BotDisplay
        #Note to future self: If works for right now, but is badly setup
        self.messageFeed = []

        #Used to turn on and off the recvBytes
        self.working = True

        #Used for individualized bot display
        self.show_display = show_display

        #Starting Bot
        self.Server = Server(*args, **kwargs, messageBuffer=self.messageBuffer, messageFeed=self.messageFeed)
        self.start()
        #Basic Actions
        self.BasicAction = BasicAction(self.Server, self, self.messageFeed)

        if show_display:
            t2 = Thread(target=self._update_display)
            t2.start()

    def start(self):
        t = Thread(target=self.manage_bytes)
        t.start()


        #Gathering LifeId
        self.messageFeed.append('forcing PU')
        self.Server('MOTH 0 0#')

        #naming itself
        self.Server('SAY 0 0 I AM TEST#')

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
        while self.working:

            self.Server._recieve_bytes()

            #if theres a message needing to be processed
            if self.messageBuffer:
                self.messageDecompression(self.messageBuffer)

    #Note to self: Make sure all commands end with an pound key!!!
    #Note: Message must all be in caps, or it will not send
    def Talk(self, message):
        return self.sendToServer(message)
    
    #Simple Left, Right, Up, Down Bot Movement
    def basicMovement(self, direction=''):
        if direction == 'Left':
            moveCMD = f'MOVE {self.x} {self.y} @{self.moveStep} -1 0#'
            self.messageFeed.append(self.sendToServer(moveCMD))
        elif direction == 'Right':
            moveCMD = f'MOVE {self.x} {self.y} @{self.moveStep} 1 0#'
            self.messageFeed.append(self.sendToServer(moveCMD))
        elif direction == 'Up':
            moveCMD = f'MOVE {self.x} {self.y} @{self.moveStep} 0 1#'
            self.messageFeed.append(self.sendToServer(moveCMD))
        elif direction == 'Down':
            moveCMD = f'MOVE {self.x} {self.y} @{self.moveStep} 0 -1#'
            self.messageFeed.append(self.sendToServer(moveCMD))

    #THIS NEEDS TO BE FIXED TO ADJUST FOR ALL OF THE i PARAMATERS. IF WORKS JUST ENOUGH FOR BASIC STUFF
    def basicAction(self, action, x=None, y=None):
        if action == 'SELF' or action == 'DROP':
            x, y = self.x, self.y

            actionCMD = f'{action} {x} {y} -1#'

            self.messageFeed.append(self.sendToServer(actionCMD))
        elif action == 'USE':
            x, y = self.x, self.y

            actionCMD = f'{action} 0 0#'

            self.messageFeed.append(self.sendToServer(actionCMD))
        else:
            self.messageFeed.append('Incorrect action type')


    def PlayerUpdate(self) -> None:
        if self.LifeID in self.players and not self.LifeID == 0:
                #death condition
                if self.players[self.LifeID].PU[-1] in ('reason_disconnected', 'reason_killed_id', 'reason_hunger', 'reason_nursing_hunger', 'reason_age'):
                    self.status = f'DEAD: {self.players[self.LifeID].PU[-1]}'
                    self.stop()
                    return

                if self.players[self.LifeID].PU:
                    self.playerObjectID = self.players[self.LifeID].PU[1]
                    self.heat = self.players[self.LifeID].PU[11]
                    if not self.players[self.LifeID].PU[14] == 'X':
                        self.x, self.y = int(self.players[self.LifeID].PU[14]), int(self.players[self.LifeID].PU[15])

                if self.players[self.LifeID].name:
                    self.name = self.players[self.LifeID].name



    def messageDecompression(self, messages):
        if not messages: 
            return
        elif messages[0] == b'': #During split, there is a chance where the pound key will be the last character, forcing there to be an empty byte
            messages.pop(0)
            return self.messageDecompression(messages)
        else:
            messages = messages.pop(0).split(b'#', 1) + messages
            
            #Curse Update
            if messages[0].startswith(b'CU'):

                self.messageFeed.append('hooooooraaaay')
                cursemessage = messages.pop(0).decode()
                self.messageFeed.append(cursemessage)

                try:
                    with open('../curselog.txt', 'w') as file:
                         file.write(cursemessage)
                except FileNotFoundError:
                    print('missing curselog')
            
            #Food change: gives capacity and food
            elif messages[0].startswith(b'FX'):
                food = messages.pop(0).decode().split()
                self.food, self.foodCapacity = food[1], food[2]

            #Monument Call
            elif messages[0].startswith(b'MN'):

                monument = messages.pop(0).decode().split()
                self.messageBuffer.append(monument)
            
            #Map Change
            elif messages[0].startswith(b'MX'):

                #TO DO
                #print('showing map changes:')
                #print(bufferedMessage[0].decode())

                messages.pop(0)
            
            elif messages[0].startswith(b'NM'):
                names = messages.pop(0).decode().splitlines()
                names.pop(0)
                while names:
                    name = names.pop(0).split(' ', 1)

                    if int(name[0]) in self.players:
                        self.players[int(name[0])].name = name[1]
                    else:
                        self.players[int(name[0])] = RawInfo(name=name[1])
                
                if not self.name:
                    self.PlayerUpdate()

            #Player Says (Also Useful in finding player ID)
            elif messages[0].startswith(b'PS'):

                #TO DO
                # Handling Other players Messages      

                message = messages.pop(0).decode().split()

                #ID checking condition (comes in the following ways: ID/0)
                for i in range(len(message)):
                    if message[i] == '+NO':
                        self.LifeID = int(message[i-1].split('/')[0])
                        self.PlayerUpdate()
                    elif message[i] == '*mother':
                        self.LifeID = int(message[i-3].split('/')[0])
                        self.PlayerUpdate()


            #Player Update
            elif messages[0].startswith(b'PU'):


                playerUpdate = messages.pop(0).decode().split()
                playerUpdate.pop(0)

                while playerUpdate:
                    lifeID = int(playerUpdate[0])

                    if lifeID in self.players:
                        self.players[lifeID].PU = playerUpdate[0:24]
                    else:
                        self.players[lifeID] = RawInfo(PU=playerUpdate[0:24])
                    playerUpdate = playerUpdate[25:]

                    if playerUpdate:
                        try:
                            int(playerUpdate[0])
                        except ValueError:
                            deathMessage = playerUpdate.pop(0)
                            self.players[lifeID].PU.append(deathMessage)
                
                self.PlayerUpdate()

            #catch all of all messages I dont have implemented just yet
            #Bad Biomes, Baby Wiggle, Craving, Curse Token Change, Flip, Following, Ghost, Grave, Heat Change, Lineage, Learned Tool Report, Player Emote, PLAYER_OUT_OF_RANGE, Tools Slots, Valley Spacing, War Report
            #elif messages[0].startswith((b'BB', b'BW',b'CR', b'CX',  b'EX', b'FL', b'FW', b'GH', b'GV', b'HX', b'LN', b'LR',  b'PE', b'PO', b'TS', b'VS', b'WR',)):
             #   #TO DO
              #  messages.pop(0)
            elif messages[0].startswith(cmdBank):
                messagetype = messages.pop(0).decode()

                with Path('serverlog.txt').open('a') as file:
                    file.write(messagetype + '\n')

            #Note: Some messages end with the Enf Of Frame Marker #FM, so we delete all chars including and after '#FM'
            elif messages[0].startswith(b'FM'): 
                messages.pop(0)

            #Compressed Message Condition
            elif messages[0].startswith(b'CM'):
                splitlines = messages.pop(0).split()

                #Compressed messages are sent with the following parameters: BinarySize, CompressedSize
                savedByte = messages.pop(0)

                #interesting...
                #When dealing with very large compressed files, we must use zlib object to deal with it if you prioritize low ram for your build
                #Thank you : https://stackoverflow.com/questions/32367005/zlib-error-error-5-while-decompressing-data-incomplete-or-truncated-stream-in
                zobj = zlib.decompressobj()

                messages.insert(0, savedByte[int(splitlines[2]):])
                messages.insert(0,zobj.decompress(savedByte[:int(splitlines[2])]))

            
            #Map Chunk Condition
            elif messages[0].startswith(b'MC'):
                splitlines = messages.pop(0).decode().split()
                
                splitlines = [int(s) for s in splitlines[1:]]
                #Compressed messages are sent with the following parameters: sizex, sizey, x, y, BinarySize, CompressedSize
                #each tile is divided as so: BiomeType:GroundOnlyType:Object/s Ids
                #BiomeType is between 0-6
                #Note: array[0][0][0] will show the bottom left corner, meaning that the bottom left corner is [0][0] and the top right corner is [32][30]
                savedByte = messages[0][0:int(splitlines[5])]
                messages[0] = messages[0][int(splitlines[5]):]             
            
                decompressedByte = zlib.decompress(savedByte).decode().split()
                for y in range(splitlines[3], splitlines[3] + splitlines[1]):
                    for x in range(splitlines[2], splitlines[2] + splitlines[0]):
                        self.map[(x,y)] = decompressedByte.pop(0).split(':', 2)

            #messageBuffer Error check
            else:
                print('error, no matching tag or not needed message deleting first element')
                print(messages[0])
                print('end of messed up message')
                messages.pop(0)
            
            return self.messageDecompression(messages)