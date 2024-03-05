import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import math


f = open('ir_data.txt', 'r')

data = f.read().split('\n')


distance = []
raw = []

for d in data:
    point = d.split(',')

    distance.append(int(point[0]))

    sum = 0
    for i in range(1, len(point)):
        sum += int(point[i])

    raw.append(sum/5)

print(distance)
print(raw)

# Define the function to fit
def exponential_decay(x, a, b, c):
    return a * np.exp(-b * x) + c

# Perform curve fitting
popt, pcov = curve_fit(exponential_decay, raw, distance, p0=(0, 0, 0))

print(popt)

# Visualize the results
y = []

for x in raw:
    y.append(exponential_decay(x, popt[0], popt[1], popt[2]))

plt.scatter(raw, distance, label='Original Data')
plt.plot(raw, y, 'r', label='Fitted Curve')
plt.legend()
plt.show()
