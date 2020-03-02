import os
import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt


focal_length = 200
wavelength = 632.8e-09
detector_size = (23.9, 35.8)
full_image_size = (2832, 4240)
path = '/Users/joshp/OneDrive/Documents/Senior Year, 2019-2020/Physics 357/FourierOptics/'


def get_k_extent(image: np.ndarray, focus=focal_length, lam=wavelength,
                 dec_size=detector_size, full_size=full_image_size):

    pixels_per_mm = np.array([full_size[i]/dec_size[i] for i in range(len(dec_size))])

    max_position = np.array(image.shape) / pixels_per_mm

    max_angle = np.arctan(max_position / (2 * focus))

    kx, ky = np.round((2 * np.pi * np.sin(max_angle)) / lam).astype(dtype=np.int)

    extent = -ky, ky, -kx, kx

    return extent, (kx, ky)


def grid_overlay(image: np.ndarray, show: bool, k_step: int = 20000):

    kx, ky = get_k_extent(image)[1]
    rows, cols = [dim // 2 for dim in image.shape]
    dx, dy = int((rows / kx) * k_step), int((cols / ky) * k_step)

    rgb_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    grid_color = [255, 0, 0]

    rgb_image[::dx, :, :] = grid_color
    rgb_image[:, ::dy, :] = grid_color

    if show:
        plt.imshow(rgb_image)
        plt.show()

    return rgb_image


def relabel_image(image_name: str, grid: bool, show: bool, save: bool, filepath=path, dpi=500):

    image_path = os.path.join(filepath, 'images', image_name)
    image = cv2.imread(image_path)

    if image is not None:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        print('Image Does Not Exist! Check File Name.')
        exit(0)

    k_extent = get_k_extent(image)[0]
    image = grid_overlay(image, show=show) if grid else image

    plt.figure(figsize=(float(image.shape[0])/dpi, float(image.shape[1])/dpi), dpi=dpi)
    plt.subplot(111)
    plt.imshow(image, extent=k_extent)
    plt.title('Image Plotted with Respect to Wave Number')

    if save:
        save_path = os.path.join(filepath, '%sRelabed%s' % (image_name[:-4], image_name[-4:]))
        plt.savefig(save_path, bbox_inches='tight', dpi=dpi)
        print('Figure Saved!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Relabels Images with Respect to Wave Number')
    parser.add_argument('image', type=str, help='Name of Image to be Relabeled')
    parser.add_argument('--grid', action='store_true', help='Overlays Grid onto Image')
    parser.add_argument('--show', action='store_true', help='Shows Gridded Image if Given')
    parser.add_argument('--save', action='store_true', help='Saves Relabeled Image if Given')
    arguments = parser.parse_args()

    relabel_image(image_name=arguments.image, grid=arguments.grid,
                  show=arguments.show, save=arguments.save)
