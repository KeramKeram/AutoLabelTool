from PIL import Image
import glob
import functions

file_path = "configuration.ini"


def main():
    ####### READ CONFIGURATION #########
    output_dict = functions.get_configuration_data()
    template = output_dict['InputFiles']['Template']
    images_to_paste_dir = output_dict['InputFiles']['ImagesToPasteDir']
    outDir = output_dict['OutputFiles']['OutputFolder']
    xml_template = output_dict['InputFiles']['xmlTemplate']
    x_min_start = output_dict['TemplateConfArea']['leftX']
    y_min_start = output_dict['TemplateConfArea']['leftY']
    x_max_start = output_dict['TemplateConfArea']['RightX']
    y_max_start = output_dict['TemplateConfArea']['RightY']
    class_name = output_dict['InputFiles']['className']

    ####### PREPARE DATA #########
    template_image = Image.open(template)
    template_width, template_height = template_image.size
    counter = 0
    print("Working...")

    for filename in glob.glob(images_to_paste_dir + '/*.jpg'):
        im = Image.open(filename)
        width, height = im.size
        x_shift, y_shift = functions.get_paste_coordinates_shift(x_min_start, y_min_start, x_max_start, y_max_start,
                                                                 width, height)
        x1_start = int(x_min_start) + x_shift
        y1_start = int(y_min_start) + y_shift

        output_image = functions.paste_image(template_image, im, x1_start, y1_start)
        output_img_name = outDir + '/output_' + str(counter) + '.jpg'
        output_image.save(output_img_name)

        x2_end = width + x1_start
        y2_end = height + y1_start
        functions.create_xml(xml_template, class_name, 'output_' + str(counter) + '.jpg', template_width,
                             template_height, str(x1_start),
                             str(y1_start),
                             x2_end, y2_end, outDir, class_name, counter)
        counter += 1

    print("Done.")

if __name__ == "__main__":
    main()
