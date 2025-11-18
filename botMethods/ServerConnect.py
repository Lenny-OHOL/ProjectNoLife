import socket

#Jason still uses sha1 -_-
import hmac
import hashlib


class accountLogin:
    """
    A simple class designed to connect to any OHOL servers. 
    By default, it will connect to servers that are hosted locally but you can initialize it to connect to Big Server 2
    """
    def __init__(self,  email, key, host='localhost', port=8005, tutorialNumber=1):
        #Server Connection
        self.host = host
        self.port = port
        self.SequenceNumber = ''
        self.serverPassword = 'testPassword'
        self.tutorialNumber = tutorialNumber #0 for main spawn, 1 for tutorial 1, 2 for tutorial 2

        #account information
        self.email = email
        self.key = key.replace('-', '')

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def hashingAlg(self, message):
        hashed = hmac.new(message.encode(), self.SequenceNumber.encode(), hashlib.sha1)
        return hashed.hexdigest()


    def connect(self):

        try:

            self.socket.connect((self.host, self.port))

            #Receive initial message from server
            print('Waiting to receive initial message from server...')
            initial_response = self.socket.recv(4096).decode().rsplit()
            print(f'Received from server: ')

            #Stores the sequenceNumber from the initial response to be used for SHA1
            self.SequenceNumber = initial_response[2]

            #0:Non-tutorial, 1:tut-1
            #for the message you send, the email MUST be 80 characters long, fill the rest with whitespace
            message = f'LOGIN client_new {self.email:<80} {self.hashingAlg(self.serverPassword)} {self.hashingAlg(self.key)} {self.tutorialNumber}#'
    

            # Send the message (encode string to bytes)
            self.socket.send(message.encode())
            print(f"Message sent: {message}")


            if self.socket.recv(4096).startswith(b'REJECTED'):
                raise ConnectionError('Invalid Email or Key')

        except socket.gaierror:
            #Invaldi host/port error
            print('Error: Invalid host or port')
        except ConnectionError:
            #Invlaid Email or Key
            print('Error: Invalid Email or Key')
        except Exception as e:
            #Catchall for any other errors that can occur
            print(f'New Error: {e}')


    def sendToServer(self, message):
        self.socket.send(message.encode('utf-8'))
        return message