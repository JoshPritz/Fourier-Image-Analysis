import os
import sys
import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt


path = '/Users/joshp/OneDrive/Documents/Senior Year, 2019-2020/Physics 357/FourierOptics/'


def get_image(image, filepath=path):
    image_path = os.path.join(filepath, 'images', image)
    result = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
    return image, result


def find_center(image: np.ndarray, check_center: bool = True):
    rows, cols = image.shape
    convolution_size = [int(np.mean([rows / 50, cols / 50]))] * 2
    blur = cv2.blur(image, ksize=tuple(convolution_size))
    center = np.unravel_index(np.argmax(blur, axis=None), blur.shape)

    if check_center:
        start = tuple([i-50 for i in center])[::-1]
        end = tuple([i+50 for i in center])[::-1]
        color = (0, 0, 0)

        result = cv2.rectangle(image, start, end, color, thickness=5)

        plt.imshow(result, cmap='gray')
        plt.title('Center of Image')
        plt.xticks([]), plt.yticks([])
        plt.show()

        answer = input('Would you like to continue?[yes/no] ')

        if answer.lower() != 'yes' and answer.lower() != 'y':
            print('\n Pre-processing Aborted!')
            sys.exit(0)

    return center


def crop_around_center(image_name: np.ndarray, size: int, save: bool, show: bool,
                       check_center: bool, return_array: bool, filepath=path,):

    name, image = get_image(image_name, filepath)
    c_row, c_col = find_center(image, check_center)

    if check_center:
        image = get_image(image_name, filepath)[1]

    size //= 2
    cropped_image = image[c_row-size:c_row+size, c_col-size:c_col+size]

    plt.imshow(cropped_image, cmap='gray')
    plt.title('Cropped Image')
    plt.xticks([]), plt.yticks([])

    if save:
        save_path = os.path.join(filepath, 'images', name[:-4] + 'Crop' + name[-4:])
        plt.imsave(fname=save_path, arr=cropped_image, cmap='gray')
        print('Cropped Image Saved!')
    if show:
        plt.show()
    if return_array:
        return cropped_image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crops an Image About the Center of its Brightest Feature\n"
                                                 "(May Fail on Images from the Image or Object Plane)")
    parser.add_argument('image', type=str, help='Name of Image Whose Transform to Compute with File Type')
    parser.add_argument('--size', type=int, default=2000, help='Side length (in pixels) of Cropped Image')
    parser.add_argument('--show', action='store_true', help='Displays Image after Transform')
    parser.add_argument('--save', action='store_true', help='Saves Image If Flag is Given')
    parser.add_argument('--check', action='store_true',
                        help='Allows User to View Approximate Center and Choose Whether to Continue')
    parser.add_argument('--return_arr', action='store_true', help='Returns Image Array If Flag is Given')
    arguments = parser.parse_args()

    crop_around_center(arguments.image, arguments.size, arguments.save,
                       arguments.show, arguments.check, arguments.return_arr)
