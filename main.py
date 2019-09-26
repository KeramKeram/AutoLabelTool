from PIL import Image
import configparser
import glob
from xml.etree import ElementTree as et
from pathlib import Path

file_path = "configuration.ini"


def paste_image(template_image, image, left, upper, right, lower):
    template_image.paste(image, (left, upper, right, lower))
    return template_image


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

    # tree.find('annotation/folder').text = folder
    # tree.find('annotation/filename').text = filename
    # tree.find('annotation/path').text = path + "/" + out_folder + "/" + filename
    # tree.find('annotation/size/width').text = width
    # tree.find('annotation/size/height').text = height
    # tree.find('annotation/object/bndbox/xmin').text = xmin
    # tree.find('annotation/object/bndbox/ymin').text = ymin
    # tree.find('annotation/object/bndbox/xmax').text = xmax
    # tree.find('annotation/object/bndbox/ymax').text = ymax
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
    x1_start = int(x_min_start)
    y1_start = int(y_min_start)
    x2_start = int(x_min_start) + width
    y2_start = int(y_min_start) + height
    output_image = paste_image(template_image, im, x1_start, y1_start, x2_start, y2_start)
    output_img_name = outDir + '/output_' + str(counter) + '.jpg'
    output_image.save(output_img_name)
    create_xml(xml_template, class_name, 'output_' + str(counter) + '.jpg', template_width, template_height, str(x1_start),
               str(y1_start),
               str(x2_start), str(y2_start), outDir, class_name, counter)
    counter += 1
