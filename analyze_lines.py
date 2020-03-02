import os
import cv2
import numpy as np
import pandas as pd


path = '/Users/joshp/OneDrive/Documents/Senior Year, 2019-2020/Physics 357/FourierOptics/'


def get_image_data(image_name: str, to_csv: bool, axis: int = 1, filepath=path):

    image = cv2.imread(os.path.join(filepath, 'images', image_name))

    if image is None:
        print('Check File Name!')
        exit(0)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    convolution_size = (25, 25)
    blur = cv2.blur(image, convolution_size)
    c_col = np.unravel_index(np.argmax(blur, axis=None), blur.shape)[axis]

    pixel_values = np.mean(blur[:, c_col-50:c_col+50], axis=axis)
    data = pd.DataFrame(data={'pixel': list(range(blur.shape[int(not axis)])),
                              'value': pixel_values})

    if to_csv:
        save_path = os.path.join(path, '%s_Data.CSV' % image_name[:-4])
        data.to_csv(path_or_buf=save_path, index=False)
        print('CSV Saved!')

    return data
