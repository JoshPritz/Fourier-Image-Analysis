import os
import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt

from itertools import product


path = '/Users/joshp/OneDrive/Documents/Senior Year, 2019-2020/Physics 357/FourierOptics/'
detector_size = (23.9, 35.8)        # Size of camera sensor in millimeters


def get_radius(image, diameter, detector=detector_size):

    size = image.shape
    pixels_per_mm = np.mean([size[i]/detector[i] for i in range(len(size))])

    return pixels_per_mm * float(diameter / 2)


def get_coordinates(radius, center: tuple):

    center = np.array(center, dtype=np.int)

    iterable = product(range(-int(radius), int(radius)+1), repeat=2)
    coordinates = np.array([coord for coord in iterable if np.linalg.norm(coord) <= radius])

    for coordinate in coordinates:
        coordinate += center

    return coordinates


def get_mask(image, diameter):

    mask = np.zeros_like(image, dtype=np.int)
    rows, cols = mask.shape
    x_center, y_center = rows // 2, cols // 2

    radius = get_radius(image, diameter)
    coordinates = get_coordinates(radius, center=(x_center, y_center))

    for coord in coordinates:
        mask[coord[0], coord[1]] = 1

    return mask


def pinhole(image, diameter, show: bool, save: bool, filepath=path):

    image_path = os.path.join(filepath, 'images', image)
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)

    mask = get_mask(img, diameter)
    masked_image = np.multiply(img, mask)

    transform = np.fft.fftshift(np.fft.fft2(masked_image))
    transform_image = 20 * np.log(np.abs(transform))

    plt.imshow(transform_image)
    plt.title('Pinhole Image (Diameter %s mm)' % diameter)

    if save:
        save_path = os.path.join(path, 'pinhole', image[:-4] + ('Pinhole%.1f' % diameter) + image[-4:])
        plt.imsave(fname=save_path, arr=transform_image, cmap='gray')
        print('\nImage Saved!')
    if show:
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Creates Theoretical Low Pass Filtered Image via Pinhole")
    parser.add_argument('image', type=str, help='Name of Image Whose Transform to Compute with File Type')
    parser.add_argument('diameter', type=float, help='Diameter of Pinhole')
    parser.add_argument('--show', action='store_true', help='Displays Image after Transform')
    parser.add_argument('--save', action='store_true', help='Saves Image If Flag is Given')
    arguments = parser.parse_args()

    pinhole(arguments.image, arguments.diameter, arguments.show, arguments.save)
