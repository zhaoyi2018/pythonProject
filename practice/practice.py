import base64
import binascii
import os.path
import re

import pandas as pd
from PIL import Image
from io import BytesIO
import csv

csv.field_size_limit(max(csv.field_size_limit(), 2**30))

dir_path = "/data/home/zhaoyi/Documents/PycharmProjects/pythonProject/db_operate/hive_operate/data"
file_name = "face_template.csv"
save_path = "/data/home/zhaoyi/Documents/PycharmProjects/pythonProject/practice/data"


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")


# 编码转图片
def base64_to_img(base64_image_string, file_name, file_dir):
    create_folder_if_not_exists(file_dir)
    image_data = base64.b64decode(base64_image_string)
    image = Image.open(BytesIO(image_data))
    image.save(os.path.join(file_dir, file_name) + '.png', 'PNG')


def get_img_name(update_time, index):
    if index < 10:
        return update_time + "_00" + str(index)
    elif index < 100:
        return update_time + "_0" + str(index)
    else:
        return update_time + "_" + str(index)


def is_base64(s):
    try:
        base64.b64decode(s)
        return True
    except binascii.Error:
        return False


# 读取csv文件
file_path = os.path.join(dir_path, file_name)
with open(file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    header = next(csv_reader)
    print("Header:", header)

    for row_index, row in enumerate(csv_reader):
        print(f"当前行数:{row_index}")

        imgs_list = row[1].split(";") if ";" in row[1] else row[1].split("；")
        if len(imgs_list) >= 2:
            uid = row[0]
            update_time = row[4]
            for index, img in enumerate(imgs_list):
                base64_to_img(row[1], get_img_name(update_time, index+1), os.path.join(save_path, uid))

        if not is_base64(row[1]) and len(imgs_list) == 1:
            break

# 图片存储
