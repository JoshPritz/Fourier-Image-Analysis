import os
import sys
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


def high_pass(image, mask, show: bool, save: bool, filepath=path):

    image_transform = fourier_transform(image, filepath)

    rows, columns = image_transform.shape
    x_center, y_center = rows // 2, columns // 2

    if mask <= max(rows, columns):
        image_transform[x_center-mask:x_center+mask, y_center-mask:y_center+mask] = 0
    else:
        print('Mask Size Larger Than Image!')
        sys.exit(0)

    inverse = np.fft.ifftshift(image_transform)
    inverse = np.fft.ifft2(inverse)
    inverse_image = np.abs(inverse)

    plt.imshow(inverse_image, cmap='gray')
    plt.title('Cleaned Image')
    plt.xticks(np.linspace(0, columns, 5))
    plt.yticks(np.linspace(0, rows, 5))

    if save:
        save_path = os.path.join(path, 'cleaned_images', image[:-4] + 'Cleaned' + image[-4:])
        plt.imsave(fname=save_path, arr=inverse_image, cmap='gray')
        print('Cleaned Image Saved!')

    if show:
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Cleans an Image Using a High-Pass FFT Filter")
    parser.add_argument('image', type=str, help='Name of Image Whose Transform to Compute with File Type')
    parser.add_argument('--mask', type=int, default=5, help='Side Length of Square Mask Placed over Central Feature')
    parser.add_argument('--show', action='store_true', help='Displays Image after Transform')
    parser.add_argument('--save', action='store_true', help='Saves Image If Flag is Given')
    arguments = parser.parse_args()

    high_pass(arguments.image, arguments.mask, arguments.show, arguments.save)
