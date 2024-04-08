import cv2
import numpy as np

import numpy as np
import matplotlib.pyplot as plt

def generate_ir_data(num_samples, max_distance, sensor_noise_std):
    """
    Generate simulated IR sensor data.

    Parameters:
    - num_samples: Number of data samples to generate.
    - max_distance: Maximum distance the sensor can measure.
    - sensor_noise_std: Standard deviation of sensor noise.

    Returns:
    - A list of simulated IR sensor readings.
    """
    true_distances = np.linspace(0, max_distance, num_samples)
    sensor_noise = np.random.normal(0, sensor_noise_std, num_samples)
    sensor_readings = np.sin(true_distances) + sensor_noise
    return sensor_readings

def plot_sensor_data(sensor_readings, title="Simulated IR Sensor Data"):
    """
    Plot the simulated IR sensor data.

    Parameters:
    - sensor_readings: List of simulated sensor readings.
    - title: Plot title.
    """
    plt.plot(sensor_readings, label='Sensor Readings')
    plt.xlabel('Sample')
    plt.ylabel('Distance')
    plt.title(title)
    plt.legend()
    plt.show()

def normalize(data, min_value, max_value):
    """
    Normalize data to the range [0, 1].

    Parameters:
    - data: Data to be normalized.
    - min_value: Minimum value in the original range.
    - max_value: Maximum value in the original range.

    Returns:
    - Normalized data.
    """
    return (data - min_value) / (max_value - min_value)

def convert_to_grayscale_image(sensor_readings, image_height, max_distance):
    """
    Convert simulated IR sensor data to a grayscale image.

    Parameters:
    - sensor_readings: List of simulated sensor readings.
    - image_height: Height of the output image.
    - max_distance: Maximum distance the sensor can measure.

    Returns:
    - Grayscale image as a NumPy array.
    """
    normalized_distances = normalize(sensor_readings, 0, max_distance)

    # Create an image with a single column of pixels
    image = np.zeros((image_height, 100))
    print('image has shape {}'.format(image.shape,))

    # Map normalized distances to pixel intensities
    pixel_intensities = (normalized_distances * 255).astype(np.uint8)

    # Set pixel intensities in the column
    image = pixel_intensities * np.ones((len(pixel_intensities),1))
    return image

def display_image(image, title="Grayscale Image"):
    """
    Display a grayscale image.

    Parameters:
    - image: Grayscale image as a NumPy array.
    - title: Image title.
    """
    plt.imshow(image, cmap='gray', aspect='auto')
    plt.title(title)
    plt.xlabel('Column')
    plt.ylabel('Pixel')
    plt.colorbar(label='Distance')
    plt.show()

def edge_detection(input_image_data, output_image_path,input_image_path=None):
    if input_image_path != None:
        # Read the input image
        image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    else:
        image = input_image_data.astype(np.uint8)

    # Apply GaussianBlur to reduce noise and help edge detection
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    # Use Canny edge detector
    edges = cv2.Canny(blurred, 50, 150)

    # Save the result
    cv2.imwrite(output_image_path, edges)

    # Display the original and edge-detected images
    cv2.imshow('Original Image', image)
    cv2.imshow('Edge Detection Result', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def contrast_increase(input_image_data, output_image_path,input_image_path=None):
    if input_image_path != None:
        # Read the input image
        image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    else:
        image = input_image_data.astype(np.uint8)

    # Apply histogram equalization for contrast enhancement
    equalized_image = cv2.equalizeHist(image)

    # Save the result
    cv2.imwrite(output_image_path, equalized_image)

    # Display the original and contrast-enhanced images
    cv2.imshow('Original Image', image)
    cv2.imshow('Contrast Enhanced Result', equalized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def filter_image(input_image_data, output_image_path, threshold_value, input_image_path=None):
    if input_image_path != None:
        # Read the input image
        image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    else:
        image = input_image_data.astype(np.uint8)

    # Apply the filter: Pixels above the threshold are kept, the rest set to 0
    filtered_image = np.where(image > threshold_value, image, 0)

    # Save the result
    cv2.imwrite(output_image_path, filtered_image)

    # Display the original and filtered images
    cv2.imshow('Original Image', image)
    cv2.imshow('Filtered Result', filtered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    num_samples = 1000
    max_distance = 25  # Maximum distance the sensor can measure
    sensor_noise_std = 0.5  # Standard deviation of sensor noise
    image_height = 2000  # Height of the output image

    # Generate simulated IR sensor data
    simulated_data = generate_ir_data(num_samples, max_distance, sensor_noise_std)

    # Plot the simulated data
    plot_sensor_data(simulated_data)

    # Convert data to a grayscale image
    grayscale_image = convert_to_grayscale_image(simulated_data, image_height, max_distance)

    # Display the grayscale image
    display_image(grayscale_image)

    input_image_path = "test.jpeg"
    output_image_path = "output_edge_image.jpeg"

    edge_detection(grayscale_image, output_image_path)

    contrast_increase(grayscale_image, output_image_path)

    threshold_value = 150  # Adjust the threshold value as needed

    # Filtering based on threshold
    filter_image(grayscale_image, output_image_path, threshold_value)
