import time # Time library   
# Socket library:  https://realpython.com/python-sockets/  
# See: Background, Socket API Overview, and TCP Sockets  
import socket
import os

absolute_path = os.path.dirname(__file__) # Absoult path to this python script
relative_path = "./"   # Path to sensor data file relative to this python script (./ means data file is in the same directory as this python script)
full_path = os.path.join(absolute_path, relative_path) # Full path to sensor data file


class botConnection():
    def __init__(self, host=None, port=None):
            self.host = host
            self.port = port

            self.socket = None
            self.bot = None

    def connectToBot(self):
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((HOST, PORT))   # Connect to the socket  (Note: Server must first be running)

        except:
            print('Host could not be found, please try again')
            return -1

        self.bot = self.socket.makefile("rbw", buffering=0)

        return 0
    
    def writeToBot(self, message):
        
        try:
            self.bot.write(str(message).encode())
        except:
            print('Invalid message, please try again')
            return -1
       
        return 0
    
    def readFromBot(self):
        message = ''
        try:
            raw = self.bot.readline()
            message = raw.decode()
        except:
             print('Error occured while reading from bot, please try again')

             return 'error', -1
        
        return message, 0
    
    def requestScan(self, filename):
        print("Requested Sensor scan from Cybot:\n")

        rx_message = bytearray(1) # Initialize a byte array

        # Create or overwrite existing sensor scan data file
        file_object = open(full_path + filename,'w') # Open the file: file_object is just a variable for the file "handler" returned by open()

        while (rx_message.decode() != "END\n"): # Collect sensor data until "END" recieved
                rx_message = self.bot.readline()   # Wait for sensor response, readline expects message to end with "\n"
                file_object.write(rx_message.decode())  # Write a line of sensor data to the file
                print(rx_message.decode()) # Convert message from bytes to String (i.e., decode), then print

        file_object.close() # Important to close file once you are done with it!!     
    
    def __del__(self):
        print("Client exiting, and closing file descriptor, and/or network socket\n")
        time.sleep(2) # Sleep for 2 seconds
        self.bot.close()         # Close file object associated with the socket or UART
        self.socket.close()  # Close the socket (NOTE: comment out if using UART interface, only use for network socket option)

if __name__ == '__main__':
    # TCP Socket BEGIN (See Echo Client example): https://realpython.com/python-sockets/#echo-client-and-server
    HOST = "192.168.1.1"  # The server's hostname or IP address
    PORT = 288        # The port used by the server
    cxn = botConnection(HOST, PORT)
    print(cxn.host)
    print(cxn.port)

    error = cxn.connectToBot()

    send_message = "Connected\n"

    error = cxn.writeToBot(send_message)

    if error < 0:
        exit(error)

    while send_message != 'quit\n':
        print("wait for server reply\n")
        rx_message, error = cxn.readFromBot()      # Wait for a message, readline expects message to end with "\n"

        if error < 0:
             exit(error)

        print("Got a message from server: " + rx_message + "\n") # Convert message from bytes to String (i.e., decode)
        send_message = input("Enter a message (enter quit to exit):") + '\n' # Enter next message to send to server
        cxn.writeToBot(send_message) # Convert String to bytes (i.e., encode), and send data to the server

        if error < 0:
             exit(error)

    del cxn
