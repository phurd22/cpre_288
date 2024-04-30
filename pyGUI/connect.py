import time # Time library   
# Socket library:  https://realpython.com/python-sockets/  
# See: Background, Socket API Overview, and TCP Sockets  
import socket

TIMEOUT = 100

class BotConnection():
    def __init__(self, host=None, port=None):
            self.host = host
            self.port = port

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(TIMEOUT)
            self.bot = None

    def connectToBot(self):
        log_message = ''
        try:
            self.socket.connect((self.host, self.port))   # Connect to the socket  (Note: Server must first be running)
            log_message += 'Connection successful'
        except:
            log_message += 'Host could not be found, please try again'
            return log_message, -1

        self.bot = self.socket.makefile("rbw", buffering=0)

        return log_message, 0
    
    def disconnectFromBot(self):
        if self.bot is not None:
            print("Client exiting, and closing file descriptor, and/or network socket\n")
            time.sleep(2) # Sleep for 2 seconds
            self.bot.close()         # Close file object associated with the socket or UART
    
    def writeToBot(self, b):
        log_message = ''
        self.bot.write(b)
        try:
            pass
            #self.bot.write(b)
        except:
            log_message += 'Error sending byte to bot'
            return log_message, -1
        return log_message, 0
    
    def readFromBot(self):
        message = ''
        try:
            raw = self.bot.readline()
            message = raw.decode()
        except:
            return 'Error occured while reading from bot, please try again', -1
        
        return message, 0
    
    def getScanData(self, filename):
        log_message = ''
        error = 0
        rx_message = bytearray(1) # Initialize a byte array

        # Create or overwrite existing sensor scan data file
        file_object = open(filename,'w') # Open the file: file_object is just a variable for the file "handler" returned by open()
        while (rx_message.decode() != "END\n"): # Collect sensor data until "END" recieved
            try:
                rx_message = self.bot.readline()   # Wait for sensor response, readline expects message to end with "\n"
                file_object.write(rx_message.decode())  # Write a line of sensor data to the file
            except TimeoutError:
                log_message = "Scan request timed out, please try again"
                error = -1
                break

        file_object.close() # Important to close file once you are done with it!!

        return log_message, error 
    
    def __del__(self):
        self.disconnectFromBot()
        self.socket.close()  # Close the socket (NOTE: comment out if using UART interface, only use for network socket option)

if __name__ == '__main__':

    # TCP Socket BEGIN (See Echo Client example): https://realpython.com/python-sockets/#echo-client-and-server
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432       # The port used by the server
    cxn = BotConnection(HOST, PORT)
    print(cxn.host)
    print(cxn.port)

    error = cxn.connectToBot()

    send_message = "Connected\n"

    msg, error = cxn.writeToBot(send_message)

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