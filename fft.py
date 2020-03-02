import os
import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt

path = '/Users/joshp/OneDrive/Documents/Senior Year, 2019-2020/Physics 357/FourierOptics/'


def fourier_transform(image, filepath=path):

    image_path = os.path.join(filepath, 'images', image)

    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
    transform = np.fft.fft2(img)

    return np.fft.fftshift(transform)


def obtain_image(image, show: bool, save: bool, filepath=path):

    transform = fourier_transform(image, filepath)
    transform_image = 20 * np.log(np.abs(transform))

    plt.imshow(transform_image, cmap='binary')
    plt.title('Fourier Transform')
    plt.xticks(np.linspace(0, transform_image.shape[1], 5))
    plt.yticks(np.linspace(0, transform_image.shape[0], 5))

    if save:
        save_path = os.path.join(filepath, 'transforms', image[:-4] + 'Transform' + image[-4:])
        plt.imsave(fname=save_path, arr=transform_image, cmap='binary')
        print('Fourier Transform Saved!')
    if show:
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Computes an Image's Fourier Transform or Inverse Fourier Transform")
    parser.add_argument('image', type=str, help='Name of Image Whose Transform to Compute with File Type')
    parser.add_argument('--show', action='store_true', help='Displays Image after Transform')
    parser.add_argument('--save', action='store_true', help='Saves Image If Flag is Given')
    arguments = parser.parse_args()

    obtain_image(arguments.image, arguments.show, arguments.save)
