import socket

#Jason still uses sha1 -_-
import hmac
import hashlib

from bot_core.message_manager import MessageManager
from bot_core.player_info import PlayerInfo, RawInfo


class Server(MessageManager):
    """
    A simple class designed to connect to any OHOL servers. 
    By default, it will connect to servers that are hosted locally but you can initialize it to connect to Big Server 2
    """
    def __init__(self,  email, key, host='localhost', port=8005, tutorial_number=1, server_password = 'testPassword', PlayerInfo:PlayerInfo = PlayerInfo()):
        
        self.server_message_buffer = []
        #Message Feed that will be used by the BotDisplay
        #Note to future self: If works for right now, but is badly setup
        self.message_feed = []

        MessageManager.__init__(self, PlayerInfo, self.server_message_buffer, self.message_feed)
        
        #Server Connection
        self.host = host
        self.port = port
        self.sequence_number = ''
        self.tutorial_number = tutorial_number #0 for main spawn, 1 for tutorial 1, 2 for tutorial 2
        self.server_password = server_password #BS2 uses 'testPassword' for its password


        #recieve byte control
        self.working = True

        #account information
        self.email = email
        self.key = key.replace('-', '')

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect()

    def __call__(self, message):
        self._send_to_server_and_feed(message)

    def _sha1(self, message):
        hashed = hmac.new(message.encode(), self.sequence_number.encode(), hashlib.sha1)
        return hashed.hexdigest()


    def connect(self):

        try:

            self.socket.connect((self.host, self.port))

            #Receive initial message from server
            print('Waiting to receive initial message from server...')
            initial_response = self.socket.recv(4096).decode().rsplit()
            print(f'Received from server: ')

            #Stores the sequence number from the initiaSequenceNumberl response to be used for SHA1
            self.sequence_number = initial_response[2]

            #0:Non-tutorial, 1:tut-1
            #for the message you send, the email MUST be 80 characters long, fill the rest with whitespace
            message = f'LOGIN client_new {self.email:<80} {self._sha1(self.server_password)} {self._sha1(self.key)} {self.tutorial_number}#'
    

            # Send the message (encode string to bytes)
            self.socket.send(message.encode())
            print(f"Message sent: {message}")


            if self.socket.recv(4096).startswith(b'REJECTED'):
                raise ConnectionError('Invalid Email or Key')

        except socket.gaierror:
            #Invalid host/port error
            print('Error: Invalid host or port')
        except ConnectionError:
            #Invalid Email or Key
            print('Error: Invalid Email or Key')
        except Exception as e:
            #Catchall for any other errors that can occur
            print(f'New Error: {e}')

    def disconnect(self):
        self.socket.close()

    def sendToServer(self, message):
        self.socket.send(message.encode('utf-8'))
        return message
    
    def _send_to_server_and_feed(self, message):
        self.message_feed.append(self.sendToServer(message))

    def _recieve_bytes(self):
            self.server_message_buffer.append(self.socket.recv(4096))

            if self.server_message_buffer:
                #print(self.server_message_buffer)
                #print(self.players.values())
                self.messageDecompression(self.server_message_buffer)