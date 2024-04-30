import sys
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QTextBrowser, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QPixmap
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

from backend import Backend

class QImage(QWidget):
    def __init__(self, label):
        super(QWidget, self).__init__()
        self.label = QLabel(label)
        self.image = QLabel(self, pixmap=QPixmap("image.png"))
        gsLayout = QVBoxLayout()
        gsLayout.addWidget(self.label)
        gsLayout.addWidget(self.image)
        self.setLayout(gsLayout)
    
    def updateImage(self, path):
        self.image.setPixmap(QPixmap(path))

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.backend = Backend()

        self.setWindowTitle("Plankton Bot 3000")

        topGroupBox = self.createTopGroupBox()
        moveGroupBox = self.createMoveGroupBox()
        turnGroupBox = self.createTurnGroupBox()
        bottomGroupBox = self.createBottomGroupBox()
        dataTab = self.createDataTabWidget()

        self.sens = {
            'bumpLeft': self.bumpLeft,
            'bumpRight': self.bumpRight,
            'cliffLeft': self.cliffLeft,
            'cliffRight': self.cliffRight,
            'cliffFrontLeft': self.cliffFrontLeft,
            'cliffFrontRight': self.cliffFrontRight,
            'cliffLeftSignal': self.cliffLeftSignal,
            'cliffRightSignal': self.cliffRightSignal,
            'cliffFrontLeftSignal': self.cliffFrontLeftSignal,
            'cliffFrontRightSignal': self.cliffFrontRightSignal
        }

        self.buttonWindow = QWidget()
        secondLayout = QVBoxLayout()
        secondLayout.addWidget(topGroupBox)
        secondLayout.addWidget(moveGroupBox)
        secondLayout.addWidget(turnGroupBox)
        self.buttonWindow.setLayout(secondLayout)

        self.firstWindow = QWidget()
        firstLayout = QHBoxLayout()
        firstLayout.addWidget(self.buttonWindow)
        firstLayout.addWidget(dataTab)
        self.firstWindow.setLayout(firstLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.firstWindow)
        mainLayout.addWidget(bottomGroupBox)
       
        self.setLayout(mainLayout)

    def createTopGroupBox(self):
        topGroupBox = QGroupBox()

        connectInfo = QWidget()

        host = QWidget()
        hostLabel = QLabel("HOST")
        self.hostValue = QLineEdit("192.168.1.1")
        hostLayout = QVBoxLayout()
        hostLayout.addWidget(hostLabel)
        hostLayout.addWidget(self.hostValue)
        host.setLayout(hostLayout)

        port = QWidget()
        portLabel = QLabel("PORT")
        self.portValue = QLineEdit("288")
        portLayout = QVBoxLayout()
        portLayout.addWidget(portLabel)
        portLayout.addWidget(self.portValue)
        port.setLayout(portLayout)

        connectInfoLayout = QHBoxLayout()
        connectInfoLayout.addWidget(host)
        connectInfoLayout.addWidget(port)
        connectInfo.setLayout(connectInfoLayout)


        self.connectButton = QPushButton("Connect to Bot")
        self.connectButton.setDefault(True)

        self.connectButton.clicked.connect(self.sendConnect)

        self.connectionStatusText = QLabel("DISCONNECTED")

        self.connectionStatus = QWidget()
        self.connectionStatus.setStyleSheet("background-color:red;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(self.connectionStatusText)
        self.connectionStatus.setLayout(textLayout)

        scanButton = QWidget()
        scanButtonsLayout = QHBoxLayout()

        scanButtonIR = QPushButton("Scan")
        scanButtonIR.setDefault(True)
        scanButtonIR.clicked.connect(self.sendScanIR)
        song = QPushButton("Play Song")
        song.setDefault(True)
        song.clicked.connect(self.sendSong)

        scanButtonsLayout.addWidget(scanButtonIR)
        scanButtonsLayout.addWidget(song)
        scanButton.setLayout(scanButtonsLayout)

        inner = QWidget()

        layout1 = QHBoxLayout()
        layout1.addWidget(self.connectionStatus)
        layout1.addWidget(self.connectButton)

        inner.setLayout(layout1)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(connectInfo)
        mainLayout.addWidget(inner)
        mainLayout.addWidget(scanButton)

        topGroupBox.setLayout(mainLayout)

        return topGroupBox

    def createMoveGroupBox(self):
        moveGroupBox = QGroupBox()

        self.moveForward = QRadioButton("Forward")
        self.moveBackward = QRadioButton("Backward")
        self.moveForward.setChecked(True)

        self.moveDistanceValue = QSpinBox()
        self.moveDistanceValue.setPrefix("Distance: ")
        self.moveDistanceValue.setSingleStep(10)
        self.moveDistanceValue.setMaximum(2000)
        self.moveDistanceValue.setValue(250)

        self.moveSpeedValue = QSpinBox()
        self.moveSpeedValue.setPrefix("Speed: ")
        self.moveSpeedValue.setSingleStep(50)
        self.moveSpeedValue.setMinimum(50)
        self.moveSpeedValue.setMaximum(350)
        self.moveSpeedValue.setValue(150)

        moveButton = QPushButton("Move")
        moveButton.setDefault(True)

        moveButton.clicked.connect(self.sendMove)

        layout = QGridLayout()
        layout.addWidget(self.moveForward, 0, 0)
        layout.addWidget(self.moveBackward, 0, 1)
        layout.addWidget(self.moveDistanceValue, 1, 0)
        layout.addWidget(self.moveSpeedValue, 1, 1)
        layout.addWidget(moveButton, 2, 0)
        moveGroupBox.setLayout(layout)

        return moveGroupBox

    def createTurnGroupBox(self):
        turnGroupBox = QGroupBox()

        self.turnRightSelect = QRadioButton("Right")
        self.turnLeftSelect = QRadioButton("Left")
        self.turnLeftSelect.setChecked(True)

        self.turnDegreeValue = QSpinBox()
        self.turnDegreeValue.setPrefix("Degrees: ")
        self.turnDegreeValue.setMaximum(180)
        self.turnDegreeValue.setValue(45)

        self.turnSpeedValue = QSpinBox()
        self.turnSpeedValue.setPrefix("Speed: ")
        self.turnSpeedValue.setSingleStep(50)
        self.turnSpeedValue.setMinimum(50)
        self.turnSpeedValue.setMaximum(350)
        self.turnSpeedValue.setValue(50)

        turnButton = QPushButton("Turn")
        turnButton.setDefault(True)

        turnButton.clicked.connect(self.sendTurn)

        layout = QGridLayout()
        layout.addWidget(self.turnLeftSelect, 0, 0)
        layout.addWidget(self.turnRightSelect, 0, 1)
        layout.addWidget(self.turnDegreeValue, 1, 0)
        layout.addWidget(self.turnSpeedValue, 1, 1)
        layout.addWidget(turnButton, 2, 0)
        turnGroupBox.setLayout(layout)

        return turnGroupBox
    
    def createBottomGroupBox(self):
        bottomGroupBox = QWidget()
        sensorStatus = QWidget()

        bump = QWidget()
        bumpLayout = QVBoxLayout()

        self.bumpLeft = QWidget()
        bumpLeftLabel = QLabel("Bump Left")
        bumpLeftLabel.setAlignment(Qt.AlignCenter)
        self.bumpLeft.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(bumpLeftLabel)
        self.bumpLeft.setLayout(textLayout)

        self.bumpRight = QWidget()
        bumpRightLabel = QLabel("Bump Right")
        bumpRightLabel.setAlignment(Qt.AlignCenter)
        self.bumpRight.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(bumpRightLabel)
        self.bumpRight.setLayout(textLayout)

        bumpLayout.addWidget(self.bumpLeft)
        bumpLayout.addWidget(self.bumpRight)
        bump.setLayout(bumpLayout)

        cliff = QWidget()
        cliffLayout = QVBoxLayout()

        self.cliffLeft = QWidget()
        cliffLeftLabel = QLabel("Cliff Left")
        cliffLeftLabel.setAlignment(Qt.AlignCenter)
        self.cliffLeft.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(cliffLeftLabel)
        self.cliffLeft.setLayout(textLayout)

        self.cliffRight = QWidget()
        cliffRightLabel = QLabel("Cliff Right")
        cliffRightLabel.setAlignment(Qt.AlignCenter)
        self.cliffRight.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(cliffRightLabel)
        self.cliffRight.setLayout(textLayout)

        cliffLayout.addWidget(self.cliffLeft)
        cliffLayout.addWidget(self.cliffRight)
        cliff.setLayout(cliffLayout)

        cliffFront = QWidget()
        cliffFrontLayout = QVBoxLayout()

        self.cliffFrontLeft = QWidget()
        cliffFrontLeftLabel = QLabel("Cliff Front Left")
        cliffFrontLeftLabel.setAlignment(Qt.AlignCenter)
        self.cliffFrontLeft.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(cliffFrontLeftLabel)
        self.cliffFrontLeft.setLayout(textLayout)

        self.cliffFrontRight = QWidget()
        cliffFrontRightLabel = QLabel("Cliff Front Right")
        cliffFrontRightLabel.setAlignment(Qt.AlignCenter)
        self.cliffFrontRight.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(cliffFrontRightLabel)
        self.cliffFrontRight.setLayout(textLayout)

        cliffFrontLayout.addWidget(self.cliffFrontLeft)
        cliffFrontLayout.addWidget(self.cliffFrontRight)
        cliffFront.setLayout(cliffFrontLayout)

        cliffSig = QWidget()
        cliffSigLayout = QVBoxLayout()

        self.cliffLeftSignal = QWidget()
        cliffLeftSignalLabel = QLabel("Cliff Left Signal")
        cliffLeftSignalLabel.setAlignment(Qt.AlignCenter)
        self.cliffLeftSignal.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(cliffLeftSignalLabel)
        self.cliffLeftSignal.setLayout(textLayout)

        self.cliffRightSignal = QWidget()
        cliffRightSignalLabel = QLabel("Cliff Right Signal")
        cliffRightSignalLabel.setAlignment(Qt.AlignCenter)
        self.cliffRightSignal.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(cliffRightSignalLabel)
        self.cliffRightSignal.setLayout(textLayout)

        cliffSigLayout.addWidget(self.cliffLeftSignal)
        cliffSigLayout.addWidget(self.cliffRightSignal)
        cliffSig.setLayout(cliffSigLayout)

        cliffFrontSig = QWidget()
        cliffFrontSigLayout = QVBoxLayout()

        self.cliffFrontLeftSignal = QWidget()
        cliffFrontLeftSignalLabel = QLabel("Cliff Front Left Signal")
        cliffFrontLeftSignalLabel.setAlignment(Qt.AlignCenter)
        self.cliffFrontLeftSignal.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(cliffFrontLeftSignalLabel)
        self.cliffFrontLeftSignal.setLayout(textLayout)

        self.cliffFrontRightSignal = QWidget()
        cliffFrontRightSignalLabel = QLabel("Cliff Front Right Signal")
        cliffFrontRightSignalLabel.setAlignment(Qt.AlignCenter)
        self.cliffFrontRightSignal.setStyleSheet("background-color:green;")
        textLayout = QHBoxLayout()
        textLayout.addWidget(cliffFrontRightSignalLabel)
        self.cliffFrontRightSignal.setLayout(textLayout)

        cliffFrontSigLayout.addWidget(self.cliffFrontLeftSignal)
        cliffFrontSigLayout.addWidget(self.cliffFrontRightSignal)
        cliffFrontSig.setLayout(cliffFrontSigLayout)

        secondLayout = QHBoxLayout()
        secondLayout.addWidget(bump)
        secondLayout.addWidget(cliff)
        secondLayout.addWidget(cliffFront)
        secondLayout.addWidget(cliffSig)
        secondLayout.addWidget(cliffFrontSig)
        sensorStatus.setLayout(secondLayout)

        self.log = QTextBrowser()
        self.log.setPlainText("Command Log\n>> ")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(sensorStatus)
        mainLayout.addWidget(self.log)
        bottomGroupBox.setLayout(mainLayout)

        return bottomGroupBox

    def createDataTabWidget(self):
        dataTab = QTabWidget()
        dataTab.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        self.dataTableWidget = QTableWidget(100, 2)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.dataTableWidget)
        tab1.setLayout(tab1hbox)

        self.graph = QImage("Polar Plot")

        tab3 = QWidget()
        self.gs = QImage("Raw Grayscale")
        self.filtered = QImage("Object Highlight")
        layout = QHBoxLayout()
        layout.addWidget(self.gs)
        layout.addWidget(self.filtered)
        tab3.setLayout(layout)

        tab4 = QWidget()
        self.map = QImage("Map")
        resetMap = QPushButton("Reset Map")
        resetMap.setDefault(True)
        resetMap.clicked.connect(self.resetMap)

        layout = QVBoxLayout()
        layout.addWidget(self.map)
        layout.addWidget(resetMap)
        tab4.setLayout(layout)

        dataTab.addTab(tab1, "Raw")
        dataTab.addTab(self.graph, "Polar")
        dataTab.addTab(tab3, "Greyscale")
        dataTab.addTab(tab4, "Map")

        return dataTab
    
    
    def sendCommand(self, cmd):
        ret = True

        self.setDisabled(True)

        error = self.backend.processCommand(cmd)
        if (error < 0):
            ret = False
        self.log.setPlainText(self.log.toPlainText() + cmd + '\n\n' + self.backend.log_message + '\n\n>> ')
        
        self.updateSensorStatus()

        self.setEnabled(True)
        self.map.updateImage('images/map.png')

        return ret

    def sendConnect(self):
        self.backend.updateConnection(self.hostValue.text(), self.portValue.text())
        result = self.sendCommand('connect')
        if(result):
            self.connectButton.setDisabled(True)
            self.connectionStatusText.setText("CONNECTED")
            self.connectionStatus.setStyleSheet("background-color:green;")

    def sendSong(self):
        self.sendCommand("song")

    def sendScanIR(self):
        self.sendCommand("scan")
        self.backend.readData('scan_results.txt')
        self.updateDataTable()
        paths = self.backend.createGraphics()
        self.updateImages(paths)
        self.map.updateImage('images/map.png')

    def sendMove(self):
        cmd = ''
        if(self.moveForward.isChecked()):
            cmd += 'forward '
        else:
            cmd += 'backward '
        
        cmd += str(self.moveDistanceValue.value()) + ' '
        cmd += str(self.moveSpeedValue.value())

        self.sendCommand(cmd)

    def sendTurn(self):
        cmd = ''
        if(self.turnLeftSelect.isChecked()):
            cmd += 'left '
        else:
            cmd += 'right '
        
        cmd += str(self.turnDegreeValue.value()) + ' '
        cmd += str(self.turnSpeedValue.value())

        self.sendCommand(cmd)
    
    def updateDataTable(self):
        self.dataTableWidget.setItem(0, 0, QTableWidgetItem('Angle(Degrees)'))
        self.dataTableWidget.setItem(0, 1, QTableWidgetItem('Distance(m)'))
        for i, row in enumerate(self.backend.data):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                self.dataTableWidget.setItem(i+1, j, item)
        

    def updateImages(self, paths):
        self.graph.updateImage(paths['GRAPH'])
        self.gs.updateImage(paths['GS'])
        self.filtered.updateImage(paths['FILTERED'])

    def updateSensorStatus(self):
        sens = self.backend.sens
        for i, sen in enumerate(sens):
            if sens[sen] == 1:
                self.sens[sen].setStyleSheet("background-color:red;")
            else:
                self.sens[sen].setStyleSheet("background-color:green;")

    def resetMap(self):
        self.backend.resetMap()
        self.map.updateImage('images/map.png')



if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('images/icon.png'))
    app.setStyleSheet("QDialog { background-image: url(images/background.jpg) }"
                      "QLineEdit { background: transparent }"
                      "QSpinBox { background: transparent }"
                      "QTextBrowser { background: transparent }")
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())
