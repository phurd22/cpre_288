import sys

from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QIcon

from botConnect import botConnection

class Backend(QObject):

    def __init__(self, filename):
        super().__init__()

        self.filename = filename

        self.data = None
        self.dataString = pyqtSignal(str, arguments=['data'])
        self.cxn = botConnection(host='192.168.1.1', port=288)

    @pyqtSlot(str, str)
    def updateCommandWindow(self, current, message) -> str:
        return current + message + '\n>> '
    
    @pyqtSlot(bool)
    def connect(self, state):
        error = 0
        if state:
            error = self.cxn.connectToBot()
            error = self.sendRequest('Connected')
        else:
            self.cxn.disconnectFromBot()

        if (error != 0):
            return True

        return False
    
    @pyqtSlot(str)
    def sendRequest(self, request):
        error = 0

        error = self.cxn.writeToBot(request)

        if(request == 'scan'):
            self.cxn.requestScan(self.filename)
            self.processData()
        
        if (error != 0):
            return True
        
        return False
    
    @pyqtSlot(str)
    def processCommand(self, text):
        log = text.split('>> ')

        print(log)

    def readData(self):
        try:
            self.data = []
            line = ''
            with open(self.filename, 'r') as f:
                while (line != 'END\n'):
                    line = f.readline()
                    self.data.append(line)
                f.close()
        except:
            self.data = None
            print('FileNotFound')

    def processData(self):
        self.readData()
        if self.data is not None:
            print(self.data)

    def printData(self):
        ret_str = ''
        for line in self.data:
            ret_str += line
            ret_str += '\n'

        self.dataString.emit(ret_str)
    
    
    def __del__(self):
        self.cxn.disconnectFromBot()


def run_app():

    # Create an instance of the application
    # QApplication MUST be declared in global scope to avoid segmentation fault
    app = QApplication(sys.argv)

    #app.setStyleSheet(stylesheet) 

    backend = Backend('scan_results.txt')

    # Create QML engine
    engine = QQmlApplicationEngine()

    app.setWindowIcon(QIcon('images/icon.png'))

    # Load the qml file into the engine
    engine.load(QUrl('qml/main.qml'))

    # Qml file error handling
    if not engine.rootObjects():
        sys.exit(-1)

    engine.rootObjects()[0].setProperty('backend', backend)

    return app.exec_()

if __name__ == '__main__':
    sys.exit(run_app())