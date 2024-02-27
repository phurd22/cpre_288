import sys
import time

import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        # Ideally one would use self.addToolBar here, but it is slightly
        # incompatible between PyQt6 and other bindings, so we just add the
        # toolbar as a plain widget instead.
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)

        self.command = QtWidgets.QLineEdit()
        self.command.setEchoMode(QtWidgets.QLineEdit.Normal)

        layout.addWidget(self.command)

        self._static_ax = static_canvas.figure.subplots(subplot_kw={'projection': 'polar'})
        
        # angle_degrees: a vector (i.e., array of numbers) for which each element is an angle at which the sensor 
        # makes a distance measurement.
        # arange: used to to store into vector angle_degrees numbers from 0 degrees to 180 degrees, counting by 4's.
        # Units: degrees
        angle_degrees = np.arange(0,184,4)

        # distance: a vector, where each element is the corresponding distance measured at each angle in vector angle_degrees
        # Units: meters
        distance = [2.5, 2.0, 2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.5 ,2.5 ,2.5 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.5 ,2.5, 2.5, 
                    2.5, 0.5, 0.5, 0.5, 0.5 ,0.5 ,0.5 ,0.5 ,0.5 ,0.5 ,0.5 ,2.5 ,2.5 ,2.5 ,2.5 ,2.5 ,1.5 ,1.5 ,1.5 ,1.5 ,1.5 ,1.5 ,2.5]

        # angle_radians: a vector that contains converted elements of vector angle_degrees into radians 
        # Units radians
        angle_radians = (np.pi/180) * angle_degrees

        self._static_ax.plot(angle_radians, distance, color='r', linewidth=4.0)
        self._static_ax.set_xlabel('Distance (m)', fontsize = 14.0)  # Label x axis
        self._static_ax.set_ylabel('Angle (degrees)', fontsize = 14.0) # Label y axis
        self._static_ax.xaxis.set_label_coords(0.5, 0.15) # Modify location of x axis label (Typically do not need or want this)
        self._static_ax.tick_params(axis='both', which='major', labelsize=14) # set font size of tick labels
        self._static_ax.set_rmax(2.5)                    # Saturate distance at 2.5 meters
        self._static_ax.set_rticks([0.5, 1, 1.5, 2, 2.5])   # Set plot "distance" tick marks at .5, 1, 1.5, 2, and 2.5 meters
        self._static_ax.set_rlabel_position(-22.5)     # Adjust location of the radial labels
        self._static_ax.set_thetamax(180)              # Saturate angle to 180 degrees
        self._static_ax.set_xticks(np.arange(0,np.pi+.1,np.pi/4)) # Set plot "angle" tick marks to pi/4 radians (i.e., displayed at 45 degree) increments
                                                    # Note: added .1 to pi to go just beyond pi (i.e., 180 degrees) so that 180 degrees is displayed
        self._static_ax.grid(True)                     # Show grid lines

        # Create title for plot (font size = 14pt, y & pad controls title vertical location)
        self._static_ax.set_title("Mock-up Polar Plot of CyBot Sensor Scan from 0 to 180 Degrees", size=14, y=1.0, pad=-24) 

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()


if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()