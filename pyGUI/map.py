import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon

import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    from os import path
    IMAGE_PATH = path.abspath(path.join(path.dirname(__file__), 'images'))
else:
    IMAGE_PATH = 'images'

class FieldObject():
    def __init__(self, number, angle, distance, width):
        self.number = number
        self.width = width

        self.x, self.y = self.calculatePosition(angle, distance)

    def calculatePosition(self, angle, distance):
        rad = angle*(np.pi/180)
        return distance*np.cos(rad), distance*np.sin(rad)
    
class FieldBoundary():
    def __init__(self, position, angle, width=0.75):
        self.points = self.calculatePoints(position, angle, width)

    def calculatePoints(self, position, angle, width):
        radius = 16
        x,y = position
        triangle_side_length = radius * width  # Adjust the size of the triangle as needed
        angle_rad = np.radians(angle)  # Convert angle to radians
        triangle_x = x + radius * np.cos(angle_rad)
        triangle_y = y + radius * np.sin(angle_rad)
        triangle_points = [
            [triangle_x, triangle_y],
            [triangle_x + triangle_side_length * np.cos(angle_rad - np.pi/2), 
             triangle_y + triangle_side_length * np.sin(angle_rad - np.pi/2)],
            [triangle_x + triangle_side_length * np.cos(angle_rad + np.pi/2), 
             triangle_y + triangle_side_length * np.sin(angle_rad + np.pi/2)]
        ]

        return triangle_points


class Map():
    def __init__(self, botPosition, botHeading):
        self.botPosition = botPosition
        self.botHeading = botHeading
        self.oldObjects = []
        self.newObjects = []
        self.boundaries = []

        self.path = IMAGE_PATH + '/map.png'
    
    def createFieldObjects(self, entries):
        self.newObjects = []
        for entry in entries:
            if float(entry[2]) > 100.0:
                entry[2] = 30.0
            new = FieldObject(int(entry[0]), self.botHeading + int(entry[1]) - 90, float(entry[2]), float(entry[3]))

            for old in self.oldObjects:
                if (np.abs(new.x - old.x) < 10) or (np.abs(new.y - old.y) < 10):
                    self.oldObjects.remove(old) 

            self.newObjects.append(new)

    def createBoundaries(self, sens):
        angle = self.botHeading
        for sen in sens:
            if sens[sen] == 1:
                if sen == 'cliffLeft' or sen == 'cliffLeftSignal':
                    angle += 90
                elif sen == 'cliffRight' or sen == 'cliffRightSignal':
                    angle -= 90
                elif sen == 'cliffFrontLeft' or sen == 'cliffFrontLeftSignal':
                    angle += 45
                elif sen == 'cliffFrontRight' or sen == 'cliffFrontRightSignal':
                    angle -= 45
                elif sen == 'bumpLeft':
                    self.createFieldObjects([[0, 135, 21, 10]])
                elif sen == 'bumpRight':
                    self.createFieldObjects([[0, 45, 21, 10]])
        
        if angle != self.botHeading:
            b = FieldBoundary(self.botPosition, angle)
            self.boundaries.append(b)


    def updateBotPosition(self, botPosition, botHeading):
        self.botPosition = botPosition
        self.botHeading = botHeading

    def updateMap(self):
        fig = plt.figure()
        x,y = self.botPosition
        #plot bot
        bot = Circle(self.botPosition, 16, color='g', fill=True)
        fig.gca().add_patch(bot)
        
        marker = Circle((x+(10*np.cos(self.botHeading*(np.pi/180))), y+(10*np.sin(self.botHeading*(np.pi/180)))), 2, color='k', fill=True)
        fig.gca().add_patch(marker)

        for b in self.boundaries:

            triangle = Polygon(b.points, closed=True, color='r')
            fig.gca().add_patch(triangle)

        for obj in self.oldObjects:
            # Splitting each line into x, y, and diameter
            diameter = obj.width
            # Plotting the circle
            circle = Circle((obj.x, obj.y), diameter/2, color='r', fill=True)
            fig.gca().add_patch(circle)

        for obj in self.newObjects:
            # Splitting each line into x, y, and diameter
            obj.x += x
            obj.y += y
            diameter = obj.width
            
            # Plotting the circle
            circle = Circle((obj.x, obj.y), diameter/2, color='r', fill=True)
            fig.gca().add_patch(circle)

            self.oldObjects.append(obj)

        self.newObjects = []

        fig.gca().axis('scaled')
        plt.savefig(self.path)
        fig.clear()

if __name__ == "__main__":
    entries = [[1,60,34.22,11.95],
                [2,140,26.11,4.56]]
    
    m = Map((0,0), 90)
    m.createFieldObjects(entries)
    
    m.updateMap()

    m.updateBotPosition((0, 0), -45)

    m.updateBotPosition((25, -25), -45)

    entries = [[3,90,20,8]]
    
    m.createFieldObjects(entries)
    m.updateMap()

    m.updateBotPosition((100, 0), 0)
    m.updateMap()

    m.updateBotPosition((150, 200), 30)
    sens = {
            'bumpLeft':0,
            'bumpRight': 0,
            'cliffLeft': 0,
            'cliffRight': 1,
            'cliffFrontLeft': 0,
            'cliffFrontRight': 0,
            'cliffLeftSignal': 0,
            'cliffRightSignal': 0,
            'cliffFrontLeftSignal': 0,
            'cliffFrontRightSignal': 0
        }
    
    m.createBoundaries(sens)
    m.updateMap()

    m.updateBotPosition((200, 250), -30)

    sens = {
            'bumpLeft':0,
            'bumpRight': 1,
            'cliffLeft': 0,
            'cliffRight': 0,
            'cliffFrontLeft': 0,
            'cliffFrontRight': 0,
            'cliffLeftSignal': 0,
            'cliffRightSignal': 0,
            'cliffFrontLeftSignal': 0,
            'cliffFrontRightSignal': 0
        }
    m.createBoundaries(sens)
    m.updateMap()
