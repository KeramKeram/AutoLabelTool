from PIL import Image
import configparser
import glob
from xml.etree import ElementTree as et
from pathlib import Path
import random

file_path = "configuration.ini"


def paste_image(template_image, image, left, upper):
    template_img_copy = template_image.copy()
    template_img_copy.paste(image, (left, upper))
    return template_img_copy


def load_configuration_file(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_configuration_data():
    configuration = load_configuration_file(file_path)
    return configuration


def get_root(file):
    with open(file, encoding="utf8") as f:
        tree = et.parse(f)
        root = tree.getroot()
        return root, tree
    return None, None

def get_paste_coordinates_shift(x_min_rect, y_min_rect, x_max_rect, y_max_rect, width, height):
    x_shift = random.randrange(int(x_min_rect), int(x_max_rect) - int(width))
    y_shift = random.randrange(int(y_min_rect), int(y_max_rect) - int(height))
    return  int(x_shift), int(y_shift)


def create_xml(template_xml, folder, filename, width, height, xmin, ymin, xmax, ymax, out_folder, class_name,
               number):
    path = Path(__file__).parent.absolute()
    root, tree = get_root(template_xml)
    for elem in root.getiterator():
        try:
            elem.text = elem.text.replace('folder', folder)
            elem.text = elem.text.replace('filename', filename)
            elem.text = elem.text.replace('path', str(path) + "/" + out_folder + "/" + filename)
            elem.text = elem.text.replace('width', str(width))
            elem.text = elem.text.replace('height', str(height))
            elem.text = elem.text.replace('x1', str(xmin))
            elem.text = elem.text.replace('y1', str(ymin))
            elem.text = elem.text.replace('x2', str(xmax))
            elem.text = elem.text.replace('y2', str(ymax))
        except AttributeError:
            pass

    tree.write(out_folder + "/" + class_name + "_" + str(number) + ".xml")


output_dict = get_configuration_data()
template = output_dict['InputFiles']['Template']
images_to_paste_dir = output_dict['InputFiles']['ImagesToPasteDir']
outDir = output_dict['OutputFiles']['OutputFolder']
xml_template = output_dict['InputFiles']['xmlTemplate']
template_image = Image.open(template)
counter = 0
template_width, template_height = template_image.size
x_min_start = output_dict['TemplateConfArea']['leftX']
y_min_start = output_dict['TemplateConfArea']['leftY']
x_max_start = output_dict['TemplateConfArea']['RightX']
y_max_start = output_dict['TemplateConfArea']['RightY']

class_name = output_dict['InputFiles']['className']

for filename in glob.glob(images_to_paste_dir + '/*.jpg'):
    im = Image.open(filename)
    width, height = im.size
    x_shift, y_shift = get_paste_coordinates_shift(x_min_start, y_min_start, x_max_start, y_max_start, width, height)

    x1_start = int(x_min_start) + x_shift
    y1_start = int(y_min_start) + y_shift

    output_image = paste_image(template_image, im, x1_start, y1_start)
    output_img_name = outDir + '/output_' + str(counter) + '.jpg'
    output_image.save(output_img_name)

    x2_end = width + x1_start
    y2_end = height + y1_start

    create_xml(xml_template, class_name, 'output_' + str(counter) + '.jpg', template_width, template_height, str(x1_start),
               str(y1_start),
               x2_end, y2_end, outDir, class_name, counter)
    counter += 1
