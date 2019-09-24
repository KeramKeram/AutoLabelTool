from PIL import Image
import configparser
file_path = "configuration.ini"

def paste_image(template_image, image, left, upper, right, lower):
    template_image.paste(image, (left, upper, right, lower))
    return template_image

def load_configuration_file(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def get_configuration_data(input_data):
    configuration = load_configuration_file(file_path)
    template = configuration['InputFiles']['Template']
    images_to_paste_dir = configuration['InputFiles']['ImagesToPasteDir']
    return [template, images_to_paste_dir]

