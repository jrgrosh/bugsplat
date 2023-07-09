import os
import shutil
import json
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import random
import sys

random.seed(0)

def prepare_dataset(source_directory="./data/data_aggregated", target_directory="../bugsplat-dataset-2023/", size_threshold=.0175):
    os.makedirs(target_directory, exist_ok=True)
    filenames = os.listdir(source_directory)
    for filename in filenames:
        file_path = os.path.join(source_directory, filename)

        r = random.random()
        if(r <.85):
            subfolder = "train"
        elif(r<.95):
            subfolder = "val"
        else:
            subfolder = "test"


        if filename.lower().endswith(".jpeg") or filename.lower().endswith(".jpg"):
            file_basename = os.path.splitext(filename)[0]
            file_json = file_basename + ".json"
            file_json_path = os.path.join(source_directory, file_json)

            with Image.open(file_path) as image:
                width, height = image.size

            try:
                with open(file_json_path, "r") as fj:
                    json_data = json.load(fj)
                    
                    data = ""
                    for bb in json_data["shapes"]:

                        x0, y0 = bb["points"][0]
                        x1, y1 = bb["points"][1]

                        xcenter = ((x0 + x1)/2.0) / width
                        ycenter = ((y0 + y1)/2.0) / height

                        bb_width = np.abs((x1 - x0) / (width))
                        bb_height = np.abs((y1 - y0) / (height))

                        if(bb_width < size_threshold or bb_height < size_threshold):
                            continue

                        data += "0 " + str(xcenter) +  " " + str(ycenter) + " " + str(bb_width) + " " + str(bb_height) + "\n"

                        with open(target_directory + "labels/" + subfolder + "/" + file_basename + ".txt", "w") as ft:
                            ft.write(data)
            except FileNotFoundError:
                with open(target_directory + "labels/" + subfolder + "/" + file_basename + ".txt", "w") as ft:
                    ft.write("")            
            shutil.copy(file_path, target_directory + "images/" + subfolder)

threshold = .0175
if(len(sys.argv) > 1):
    threshold = sys.argv[1]
prepare_dataset(threshold = threshold)