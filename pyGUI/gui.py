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

        topGroupBox = self.createTopGroupBox()
        moveGroupBox = self.createMoveGroupBox()
        turnGroupBox = self.createTurnGroupBox()
        dataTab = self.createDataTabWidget()

        self.log = QTextBrowser()
        self.log.setPlainText("Command Log\n>> ")

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
        mainLayout.addWidget(self.log)
       
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


        scanButton = QPushButton("Scan")
        scanButton.setDefault(True)

        scanButton.clicked.connect(self.sendScan)

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
        self.moveDistanceValue.setMaximum(999)
        self.moveDistanceValue.setValue(500)

        self.moveSpeedValue = QSpinBox()
        self.moveSpeedValue.setPrefix("Speed: ")
        self.moveSpeedValue.setSingleStep(10)
        self.moveSpeedValue.setMaximum(500)
        self.moveSpeedValue.setValue(250)

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
        self.turnDegreeValue.setValue(90)

        self.turnSpeedValue = QSpinBox()
        self.turnSpeedValue.setPrefix("Speed: ")
        self.turnSpeedValue.setSingleStep(10)
        self.turnSpeedValue.setMaximum(500)
        self.turnSpeedValue.setValue(250)

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
        self.ed = QImage("Edge Detection Result")
        self.contrast = QImage("Enhanced Contrast")
        self.filtered = QImage("Filtered")

        layout = QGridLayout()
        layout.addWidget(self.gs, 0, 0)
        layout.addWidget(self.ed, 0, 1)
        layout.addWidget(self.contrast, 1, 0)
        layout.addWidget(self.filtered, 1, 1)
        tab3.setLayout(layout)

        dataTab.addTab(tab1, "Raw")
        dataTab.addTab(self.graph, "Polar")
        dataTab.addTab(tab3, "Greyscale")

        return dataTab
    
    
    def sendCommand(self, cmd):
        ret = True

        self.firstWindow.setDisabled(True)

        error = self.backend.processCommand(cmd)
        if (error < 0):
            ret = False
        self.log.setPlainText(self.log.toPlainText() + cmd + '\n\n' + self.backend.log_message + '\n\n>> ')
        
        self.firstWindow.setEnabled(True)

        return ret

    def sendConnect(self):
        self.backend.updateConnection(self.hostValue.text(), self.portValue.text())
        result = self.sendCommand('connect')
        if(result):
            self.connectButton.setDisabled(True)
            self.connectionStatusText.setText("CONNECTED")
            self.connectionStatus.setStyleSheet("background-color:green;")

    def sendScan(self):
        self.sendCommand("scan")
        self.backend.readData('scan_results.txt')
        self.updateDataTable()
        paths = self.backend.createGraphics()
        self.updateImages(paths)

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
        self.ed.updateImage(paths['ED'])
        self.contrast.updateImage(paths['CONTRAST'])
        self.filtered.updateImage(paths['FILTERED'])


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('images/icon.png'))
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())
