import zlib
from pathlib import Path

from bot_core.player_info import (PlayerInfo, RawInfo)

class MessageManager:
    #Used to double check correct server messages and throwaway and report broken ones
    cmdBank = (b'ACCEPTED\n', b'AD\n', b'AP\n', b'BB\n', b'BW\n', b'CR\n', b'CS\n', b'CU\n', b'CX\n', b'DY\n', b'EX\n', b'FD\n', b'FL\n', b'FW\n', b'FX\n', b'GH\n', b'GM\n', b'GO\n', b'GV\n', b'HE\n', b'HL\n', b'HX\n', b'LN\n', b'LR\n', b'LS\n', b'MN\n', b'MS\n', b'MX\n', b'NM\n', b'OW\n', b'PE\n', b'PH\n', b'PJ\n', b'PM\n', b'PO\n', b'PS\n', b'PU\n', b'RA\n', b'RR\n', b'SD\n', b'SN\n', b'TS\n', b'VS\n', b'VU\n', b'WR\n')
    
    def __init__(self, player_info:PlayerInfo, messageBuffer=[], message_feed=[]):
        self.player_info = player_info

        #For updating player info
        self.call_PlayerUpdate = False
        
        self.messageBuffer = messageBuffer
        self.message_feed = message_feed

        #All data that can be collected from the message manager is stored in these variables
        self.map = {}
        self.players:dict[int, RawInfo] = {}

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

                self.message_feed.append('hooooooraaaay')
                cursemessage = messages.pop(0).decode()
                self.message_feed.append(cursemessage)

                try:
                    with open('../curselog.txt', 'w') as file:
                         file.write(cursemessage)
                except FileNotFoundError:
                    print('missing curselog')
            
            #Food change: gives capacity and food
            elif messages[0].startswith(b'FX'):
                food = messages.pop(0).decode().split()
                self.player_info.food, self.player_info.food_capacity = food[1], food[2]

            #Heat change: gives capacity and food
            elif messages[0].startswith(b'HX'):
                heat = messages.pop(0).decode().split()
                self.player_info.heat, self.player_info.food_time, self.player_info.indoor_bonus = heat[1], heat[2], heat[3]

            #Monument Call
            elif messages[0].startswith(b'MN'):
                monument = messages.pop(0).decode().split()
                self.message_feed.append(monument)
            
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
                
                if not self.player_info.name:
                    self.player_update()

            #Player Says (Also Useful in finding player ID)
            elif messages[0].startswith(b'PS'):

                #TO DO
                # Handling Other players Messages      

                message = messages.pop(0).decode().split()

                #ID checking condition (comes in the following ways: ID/0)
                for i in range(len(message)):
                    if message[i] == '+NO':
                        self.player_info.LifeID = int(message[i-1].split('/')[0])
                        self.player_update()
                    elif message[i] == '*mother':
                        self.player_info.LifeID = int(message[i-3].split('/')[0])
                        self.player_update()


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
                
                self.player_update()

            #catch all of all messages I dont have implemented just yet
            #Bad Biomes, Baby Wiggle, Craving, Curse Token Change, Flip, Following, Ghost, Grave, Heat Change, Lineage, Learned Tool Report, Player Emote, PLAYER_OUT_OF_RANGE, Tools Slots, Valley Spacing, War Report
            #elif messages[0].startswith((b'BB', b'BW',b'CR', b'CX',  b'EX', b'FL', b'FW', b'GH', b'GV', b'HX', b'LN', b'LR',  b'PE', b'PO', b'TS', b'VS', b'WR',)):
             #   #TO DO
              #  messages.pop(0)
            elif messages[0].startswith(MessageManager.cmdBank):
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
        
    def player_update(self) -> None:
        if self.player_info.LifeID in self.players and not self.player_info.LifeID == 0:
                #death condition
                if self.players[self.player_info.LifeID].PU[-1] in ('reason_disconnected', 'reason_killed_id', 'reason_hunger', 'reason_nursing_hunger', 'reason_age'):
                    self.player_info.status = f'DEAD: {self.players[self.player_info.LifeID].PU[-1]}'
                    self.player_info.is_alive = False
                    return

                self.player_info._update_player_info(self.players[self.player_info.LifeID])