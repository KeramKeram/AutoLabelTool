from PIL import Image
import glob
import functions

file_path = "configuration.ini"


def main():
    ####### READ CONFIGURATION #########
    output_dict = functions.get_configuration_data()
    template = output_dict['InputFiles']['Template']
    images_to_paste_dir = output_dict['InputFiles']['ImagesToPasteDir']
    xml_template = output_dict['InputFiles']['xmlTemplate']
    class_name = output_dict['InputFiles']['className']
    outDir = output_dict['OutputFiles']['OutputFolder']
    ml_path = output_dict['OutputFiles']['pathToFileInMLProgram']
    ml_img_dir_path = output_dict['OutputFiles']['pathToImgDirectoryMLProgram']
    x_min_start = output_dict['TemplateConfArea']['leftX']
    y_min_start = output_dict['TemplateConfArea']['leftY']
    x_max_start = output_dict['TemplateConfArea']['RightX']
    y_max_start = output_dict['TemplateConfArea']['RightY']

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
        x1_start = x_shift
        y1_start = y_shift

        output_image = functions.paste_image(template_image, im, x1_start, y1_start)
        new_image_file_name = class_name + '_output_' + str(counter) + '.jpg'
        output_img_name = outDir + "/" + new_image_file_name
        output_image.save(output_img_name)

        x2_end = width + x1_start
        y2_end = height + y1_start
        functions.create_xml(xml_template, ml_img_dir_path, new_image_file_name, template_width,
                             template_height, str(x1_start),
                             str(y1_start),
                             x2_end, y2_end, outDir, class_name, counter, ml_path)
        counter += 1

    print("Done.")


if __name__ == "__main__":
    main()
