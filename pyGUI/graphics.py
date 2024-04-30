import numpy as np
import matplotlib.pyplot as plt
import cv2

import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    from os import path
    IMAGE_PATH = path.abspath(path.join(path.dirname(__file__), 'images'))
else:
    IMAGE_PATH = 'images'

THRESHOLD = 230
HEIGHT = 2000
SCALE = 4

class Graphics():
    def __init__(self, angles, distances):

        self.PATHS = {
                'GRAPH': IMAGE_PATH + '/graph.png',
                'GS': IMAGE_PATH + '/gray_scale.png',
                'ED': IMAGE_PATH + '/edge_detect.png',
                'CONTRAST': IMAGE_PATH + '/contrast.png',
                'FILTERED': IMAGE_PATH + '/filtered.png'
        }

        self.createGraph(angles, distances)
        self.createGrayScale(distances)

    def createGraph(self, angle_degrees, distance):
        # angle_radians: a vector that contains converted elements of vector angle_degrees into radians 
        # Units radians
        angle_radians = (np.pi/180) * angle_degrees

        # Create a polar plot
        plt.figure(1)
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}) # One subplot of type polar
        ax.plot(angle_radians, distance, color='r', linewidth=4.0)  # Plot distance verse angle (in radians), using red, line width 4.0

        ax.xaxis.set_label_coords(0.5, 0.15) # Modify location of x axis label (Typically do not need or want this)
        ax.tick_params(axis='both', which='major', labelsize=14) # set font size of tick labels
        #ax.set_rmax(2.5)                    # Saturate distance at 2.5 meters
        #ax.set_rticks([0.5, 1, 1.5, 2, 2.5])   # Set plot "distance" tick marks at .5, 1, 1.5, 2, and 2.5 meters
        ax.set_rlabel_position(-22.5)     # Adjust location of the radial labels
        ax.set_thetamax(180)              # Saturate angle to 180 degrees
        ax.set_xticks(np.arange(0,np.pi+.1,np.pi/4)) # Set plot "angle" tick marks to pi/4 radians (i.e., displayed at 45 degree) increments
                                                    # Note: added .1 to pi to go just beyond pi (i.e., 180 degrees) so that 180 degrees is displayed
        ax.grid(True)                     # Show grid lines
        plt.savefig(self.PATHS['GRAPH'])  # Display plot
        fig.clear()

    def createGrayScale(self, distances):
        
        image = self.convert_to_grayscale_image(np.array(distances), HEIGHT, np.min(distances), np.max(distances))

        self.edge_detection(image)

        con = self.contrast_increase(image)

        # Filtering based on threshold
        self.filter_image(con, THRESHOLD)

        cv2.imwrite(self.PATHS['GS'], cv2.resize(image, (0,0), fx=SCALE, fy=SCALE))

    def normalize(self, data, min_value, max_value):
        """
        Normalize data to the range [0, 1].

        Parameters:
        - data: Data to be normalized.
        - min_value: Minimum value in the original range.
        - max_value: Maximum value in the original range.

        Returns:
        - Normalized data.
        """
        return 1 - (data - min_value) / (max_value - min_value)

    def convert_to_grayscale_image(self, sensor_readings, image_height, min_distance, max_distance):
        """
        Convert simulated IR sensor data to a grayscale image.

        Parameters:
        - sensor_readings: List of simulated sensor readings.
        - image_height: Height of the output image.
        - max_distance: Maximum distance the sensor can measure.

        Returns:
        - Grayscale image as a NumPy array.
        """
        normalized_distances = self.normalize(sensor_readings, min_distance, max_distance)

        # Create an image with a single column of pixels
        image = np.zeros((image_height, 1000))

        # Map normalized distances to pixel intensities
        pixel_intensities = (normalized_distances * 255).astype(np.uint8)

        # Set pixel intensities in the column
        image = pixel_intensities * np.ones((len(pixel_intensities),1))
        return np.flip(image)
    
    def edge_detection(self, input_image_data):
       
        image = input_image_data.astype(np.uint8)

        # Apply GaussianBlur to reduce noise and help edge detection
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # Use Canny edge detector
        edges = cv2.Canny(blurred, 50, 150)

        # Save the result
        cv2.imwrite(self.PATHS['ED'], cv2.resize(edges, (0,0), fx=SCALE, fy=SCALE))

    def contrast_increase(self, input_image_data):
       
        image = input_image_data.astype(np.uint8)

        # Apply histogram equalization for contrast enhancement
        equalized_image = cv2.equalizeHist(image)

        # Save the result
        cv2.imwrite(self.PATHS['CONTRAST'], cv2.resize(equalized_image, (0,0), fx=SCALE, fy=SCALE))

        return equalized_image
    
    def filter_image(self, input_image_data, threshold_value):
        
        image = input_image_data.astype(np.uint8)

        # Apply the filter: Pixels above the threshold are kept, the rest set to 0
        filtered_image = np.where(image > threshold_value, image, 0)

        # Save the result
        cv2.imwrite(self.PATHS['FILTERED'], cv2.resize(filtered_image, (0,0), fx=SCALE, fy=SCALE))
        

if __name__ == "__main__":

    angle_degrees = np.arange(0,184,4)

    # distance: a vector, where each element is the corresponding distance measured at each angle in vector angle_degrees
    # Units: meters
    distance = [2.5, 2.0, 2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.5 ,2.5 ,2.5 ,2.0 ,2.0 ,2.0 ,2.0 ,2.0 ,2.5 ,2.5, 2.5, 
            2.5, 0.5, 0.5, 0.5, 0.5 ,0.5 ,0.5 ,0.5 ,0.5 ,0.5 ,0.5 ,2.5 ,2.5 ,2.5 ,2.5 ,2.5 ,1.5 ,1.5 ,1.5 ,1.5 ,1.5 ,1.5 ,2.5]

    g = Graphics(angle_degrees, distance)
