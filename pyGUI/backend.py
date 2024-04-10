from connect import BotConnection
from graphics import Graphics

import numpy as np

import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    from os import path
    data_path = path.abspath(path.join(path.dirname(__file__), 'data'))
    image_path = path.abspath(path.join(path.dirname(__file__), 'images'))
else:
    data_path = 'data'
    image_path = 'images'

HOST = "127.0.0.1"
PORT = 65432  

class Backend():
    def __init__(self):
        self.cxn = BotConnection(HOST, PORT)
        self.graphics = None

        self.data = None
        self.angles = None
        self.distances = None

        self.log_message = None

    def processCommand(self, command):
        error = 0
        if (command.lower() == 'connect'):
            self.log_message, error = self.cxn.connectToBot()
        elif(command.lower() == 'scan'):
            self.log_message, error = self.cxn.requestScan(data_path + '/scan_results.txt')
        else:
            self.log_message, error = self.cxn.writeToBot(command)
        return error


    def readData(self, fileName):
        try:
            data = []
            line = ''
            self.data = []
            with open(data_path + '/' + fileName, 'r', encoding='utf-8') as f:
                while (line != 'END\n'):
                    d = []
                    line = f.readline()
                    entries = line.split('\t')

                    d.append(entries[0])

                    dist = entries[len(entries)-1].split('\n')
                    d.append(dist[0])

                    data.append(d)

                f.close()

            for i in range(1, len(data)-1):
                self.data.append([int(data[i][0]), float(data[i][1])])
            
            self.splitData()

        except:
            self.data = None
            print('FileNotFound')

    def splitData(self):
        if self.data is not None:
            self.angles = np.zeros(len(self.data))
            self.distances = np.zeros(len(self.data))
            for i, row in enumerate(self.data):
                self.angles[i] = row[0]
                self.distances[i] = row[1]

    def createGraphics(self):
        if self.angles is not None:
            self.graphics = Graphics(self.angles, self.distances)
            return self.graphics.PATHS


    def dataToString(self):
        ret_str = ''
        for line in self.data:
            l = ''
            for entry in line:
                l += str(entry)
                l += ' '
            ret_str += l
            ret_str += '\n'
        return ret_str

    def updateConnection(self, host, port):
        self.cxn = None
        self.cxn = BotConnection(host, int(port))

if __name__ == '__main__':
    b = Backend()

    b.readData('sim_data.txt')

    str1 = b.createGraphics()

