from rembg import remove
import cv2
import path_details as pd
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def has_alpha_channel(path: str) -> bool:
    # Check file extension
    if pd.get_ext(path) != 'png':
        # Not PNG
        return False
    # Load an image
    img = cv2.imread(path)
    # Check component size (RGBA)
    return img.shape[2] == 4


def remove_background(input_path: str, output_path: str = None):
    # Optimize
    cleaned_path = pd.get_cleaned_path(input_path)
    # Get filename
    filename = pd.get_filename(input_path)
    # Get path of directory
    directory = pd.get_file_directory(input_path)
    # Generate output filename
    new_filename = filename + '_output'
    if output_path is not None:
        new_filename = output_path

    # Generate output path
    output = directory + new_filename + '.png'
    # Remove background with "rembg"
    result = remove(cv2.imread(cleaned_path))
    # Write to an image
    cv2.imwrite(output, result)


def get_color_pallet(input_path: str, output_path: str = None):
    # Optimize
    cleaned_path = pd.get_cleaned_path(input_path)
    # Get filename
    filename = pd.get_filename(input_path)
    # Get path of directory
    directory = pd.get_file_directory(input_path)

    # Load an image with alpha channel
    img = cv2.imread(cleaned_path, -1)
    # Reshape an image component
    img = img.reshape((img.shape[0] * img.shape[1], 4))

    # Pixel's indexes which alpha channel is under 253
    indexes = []
    # Index counter
    i = 0
    for rgba in img:
        if int(rgba[3]) < 253:
            indexes.append(i)
        i += 1

    # Delete indexes
    img = np.delete(img, indexes, axis=0)
    # Delete alpha channel
    img = np.delete(img, 3, axis=1)

    # k-means
    cluster = KMeans(n_clusters=5)
    cluster.fit(X=img)
    cluster_centers_arr = cluster.cluster_centers_.astype(int, copy=False)

    # Pallet image statement
    img_size = 64
    width = img_size * 5
    height = img_size

    # Generate a raw image
    tiled_color_img = Image.new(mode='RGB', size=(width, height))

    for i, rgb_arr in enumerate(cluster_centers_arr):
        # Generate hex of color
        color_hex_str = '#{:02x}{:02x}{:02x}'.format(rgb_arr[2], rgb_arr[1], rgb_arr[0])
        # Generate a color
        color_img = Image.new(mode='RGB', size=(img_size, img_size), color=color_hex_str)
        # Paste a color onto pallet
        tiled_color_img.paste(im=color_img, box=(img_size * i, 0))

    # Generate output filename
    new_filename = filename + '_color_pallet'
    if output_path is not None:
        new_filename = output_path

    # Generate output path
    output = directory + new_filename + '.png'
    # Write to an image
    tiled_color_img.save(output, quality=95)
