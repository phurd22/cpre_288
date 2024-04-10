import numpy as np
from numpy import random

MAX_WIDTH = 10

def generateNumObjects():
    return random.randint(0,4)

def generateObjects(numObjects):
    pos = []
    for p in range(0, numObjects):
        l = []
        l.append(2*random.randint(0, 90))
        l.append(random.randint(2,MAX_WIDTH))
        pos.append(l)

    return pos

def generateAngles(objs):
    s = sorted(objs)
    
    angles = []
    for i in s:
        center = i[0]
        width = i[1]
        for j in range(0, width):
            angles.append(center + 2*j)

    return angles

def createMeasurements(angles):
    a = np.linspace(0,180, 91)
    d = (random.rand(1, len(a)) + 0.5)*100
    
    for i in angles:
        index = int((i/2)+1)
        d[0][index] = (random.rand()*10)+10
    
    return a, d

def writeToFile(a, d):
    with open("data/sim_data.txt", "w", encoding='utf-8') as f:
        f.write('Angle(Degrees)\tDistance(m)\t\n')

        for i in range(0,len(a)):
            f.write(str(int(a[i])) + '\t\t\t\t' + str(d[0][i]) + '\n')
        
        f.write("END\n")
        f.close()


if __name__ == '__main__':
    numObjects = generateNumObjects()
    print(numObjects)

    pos = generateObjects(numObjects)
    print(pos)

    angles = generateAngles(pos)
    print(angles)

    a, d = createMeasurements(angles)
    print(d)

    writeToFile(a, d)