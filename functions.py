import configparser
from xml.etree import ElementTree as et
from pathlib import Path
import random

file_path = "configuration.ini"


###### IO FUNCTIONS ######
def get_configuration_data():
    configuration = configparser.ConfigParser()
    configuration.read(file_path)
    return configuration


def get_root(file):
    with open(file, encoding="utf8") as f:
        tree = et.parse(f)
        root = tree.getroot()
        return root, tree
    return None, None


def create_xml(template_xml, folder, filename, width, height, xmin, ymin, xmax, ymax, out_folder, class_name,
               number, ml_path):
    root, tree = get_root(template_xml)
    for elem in root.getiterator():
        try:
            elem.text = elem.text.replace('folder', folder)
            elem.text = elem.text.replace('filename', filename)
            elem.text = elem.text.replace('path', str(ml_path) + "/" + filename)
            elem.text = elem.text.replace('width', str(width))
            elem.text = elem.text.replace('height', str(height))
            elem.text = elem.text.replace('name', class_name)
            elem.text = elem.text.replace('x1', str(xmin))
            elem.text = elem.text.replace('y1', str(ymin))
            elem.text = elem.text.replace('x2', str(xmax))
            elem.text = elem.text.replace('y2', str(ymax))
        except AttributeError:
            print("Error during xml parsing.")
            raise AttributeError

    tree.write(out_folder + "/" + class_name + "_" + str(number) + ".xml")


###### IMAGE FUNCTIONS ######

def paste_image(template_image, image, left, upper):
    template_img_copy = template_image.copy()
    template_img_copy.paste(image, (left, upper))
    return template_img_copy


###### CALCULATION FUNCTIONS ######

def get_paste_coordinates_shift(x_min_rect, y_min_rect, x_max_rect, y_max_rect, width, height):
    x_shift = random.randrange(int(x_min_rect), int(x_max_rect) - int(width))
    y_shift = random.randrange(int(y_min_rect), int(y_max_rect) - int(height))
    return int(x_shift), int(y_shift)


def get_new_coordinates(old_x1, old_y1, old_x2, old_y2, old_height, old_width, new_height, new_width):
    width_ratio = old_width / new_width
    height_ratio = old_height / new_height

    x1 = round(old_x1 / width_ratio)
    y1 = round(old_y1 / height_ratio)
    x2 = round(old_x2 / width_ratio)
    y2 = round(old_y2 / height_ratio)

    return x1, y1, x2, y2
