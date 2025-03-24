import pandas as pd
import os
import cv2
import numpy as np
from PIL import Image


path_to_image_data = "data"

data = {}


def convert_to_model_res(img_path, filetype, subdirectory, count):
    image = Image.open(img_path).convert("RGB")
    new_image = image.resize((224, 224))

    subdirectory = subdirectory.replace(" ", "_").lower()
    new_filename = f"resized_data\{subdirectory}_{count}.{filetype}"
    new_image.save(new_filename)
    return new_filename


def read_data_dir(path_to_data):
    print("Appending images to array...")
    for subdirectory in os.listdir(path_to_data):
        # Construct the path to the subdirectory
        subdirectory_path = os.path.join(path_to_data, subdirectory)

        print(f"In subdirectory: {subdirectory_path}")
        images = []
        count = 0
        # Iterate over all files in the subdirectory and add images to the list
        for filename in os.listdir(subdirectory_path):
            img_path = os.path.join(subdirectory_path, filename)
            filetype = filename.split(".")[-1]
            if not (filetype == "png" or filetype == "jpg" or filetype == "jpeg"):
                continue

            new_filename = convert_to_model_res(img_path, filetype, subdirectory, count)
            subdirectory = subdirectory.replace(" ", "_").lower()
            # new_filename = f"resized_data/{subdirectory}_{count}.{filetype}"
            img = cv2.imread(new_filename)

            if img is not None:
                images.append(img)
                count += 1

        data[subdirectory.lower()] = images


def read_resized_dir(dir_path):
    data = {}

    for filename in os.listdir(dir_path):
        # Extract food name from filename
        food = " ".join(filename.split("_")[:-1])  # Join all parts except the last one

        file_path = os.path.join(dir_path, filename)
        img = Image.open(file_path)

        # Ensure the image is in RGB mode
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Resize image to 224x224 if it's not already
        if img.size != (224, 224):
            img = img.resize((224, 224))

        # Convert image to numpy array
        pixel_values = np.array(img)

        # Ensure the shape is correct (224, 224, 3)
        if pixel_values.shape != (224, 224, 3):
            print(f"Unexpected shape for {filename}: {pixel_values.shape}")
            continue

        # Add pixel values to the corresponding food category
        if food not in data:
            data[food] = []
        data[food].append(pixel_values)

    # Convert lists to numpy arrays
    for food in data:
        data[food] = np.array(data[food])
        print(f"{food}: {data[food].shape}")

    return data


def dict_to_dataframe(image_dict):
    rows = []
    expected_pixels = 224 * 224 * 3  # For 224x224 images

    for label in image_dict:
        count = 0
        for pixel_values in image_dict[label]:
            print(f"Count: {count}")
            # Ensure pixel_values is a numpy array
            print(f"len(pixel_values): {len(pixel_values)}")
            pixel_array = np.array(pixel_values)

            # Check if the image has the correct number of pixels
            if pixel_array.size != expected_pixels:
                print(f"filename: {pixel_array.size}")
                # continue
                # raise ValueError(f"Image for label '{label}' has {pixel_array.size} pixels. Expected {expected_pixels} pixels.")

            # Flatten the pixel values
            flat_pixels = pixel_array.flatten()

            # Ensure we have the correct number of pixels after flattening
            if len(flat_pixels) != expected_pixels:
                raise ValueError(
                    f"Flattened image for label '{label}' has {len(flat_pixels)} pixels. Expected {expected_pixels} pixels."
                )

            # Create the row with label and pixel values
            row = [label] + flat_pixels.tolist()
            rows.append(row)
            count += 1

    # Create column names
    columns = ["label"] + [f"pixel_{i}" for i in range(expected_pixels)]

    # Create the dataframe
    df = pd.DataFrame(rows, columns=columns)
    return df


def check_image_res(data_path):
    for filename in os.listdir(data_path):
        img_path = os.path.join(data_path, filename)
        with Image.open(img_path) as image:
            width, height = image.size
            if not (width == 224 and height == 224):
                print("WTF")
    print("aight")


if __name__ == "__main__":
    # check_image_res("resized_data")
    # data = read_data_dir("data")
    data = read_resized_dir("resized_data")
    df = dict_to_dataframe(data)
    print(df)

    df.to_pickle("./images.pkl")
