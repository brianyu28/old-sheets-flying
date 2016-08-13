# Old Sheets Flying - Graphics Library
from PIL import Image, ImageFont, ImageDraw
import textwrap
import osf_fonts as fonts
import osf_colors as colors

# takes a string and a list of widths (in characters), returns a list of strings by line
def separate_into_lines(text, widths):
    lines = []
    lines.append(text)
    breakline_counter = 1
    for line_width in widths:
        lines = lines[:breakline_counter - 1] + textwrap.wrap(lines[breakline_counter - 1], width=line_width)
        lines = lines[:breakline_counter] + [(' '.join(lines[breakline_counter:]))]
        breakline_counter += 1
    return lines

# formats a number as a string, to 'precision' number of decimal places
def num_to_string(number, precision):
    '{:.{prec}f}'.format(number, prec=precision)

# takes an image and prepares it for presentation
# parameter values:
#   headline (string) : adds a headline to top of image (defaults to none)
#   grayscale (boolean) : determines whether to grayscale image (defaults to False)
def present_image(img, parameters={}):
    if ('headline' in parameters) and (parameters['headline'] != ''):
        img = image_with_headline(img, parameters['headline'], {})
    
    grayscale = parameters.get('grayscale', False)
    if grayscale:
        img = img.convert(mode="LA")
    return img

# takes an existing graphic and adds a headline to it
# takes no parameters
def image_with_headline(image, headline_text, parameters={}):
    headline_font = ImageFont.truetype(fonts.SLAB_SEMI, 100)
    broken_text = textwrap.wrap(headline_text, width=(image.width / 46))
    rows = len(broken_text)
    headline_row_height = ImageDraw.Draw(image).textsize(broken_text[0], headline_font)[1]
    
    padding = 50
    width = image.width
    height = image.height + (rows * headline_row_height) + padding
    
    img = Image.new('RGB', (width, height), colors.WHITE)
    img.paste(image, (0, (rows * headline_row_height) + padding))
    draw = ImageDraw.Draw(img)
    line_counter = 0
    for line in broken_text:
        line_size = draw.textsize(line, headline_font)[0]
        draw.text(((width / 2) - (line_size / 2), (line_counter * 100)), line, fill=colors.BLACK, font=headline_font)
        line_counter += 1
    return img

# generates a donut graphic representing a single data point (percentage)
# Parameters:
#   percent (int) : number to represent between 0 and 100, inclusive
# Optional Parameters:
#    description (string) : label which appears under parentheses (defaults to none)
#    color (rgb tuple) : color for the pie slice (defaults to Crimson Red)
#    label (string) : large label in middle of donut (defaults to percentage)
#    clockwise (boolean) : determines the direction of the pie slice (defaults clockwise)
def donut(percent, parameters={}):
    # set the width and height of the image
    width = 1000
    height = 1000
    
    # create the image
    img = Image.new('RGB', (width, height), colors.WHITE)
    draw = ImageDraw.Draw(img)
    
    # draw the grayed-out portion of the donut graph
    draw.ellipse([(0, 0), (width, height)], fill=colors.GRAY)
    
    # calculate the angles for the filled in portion of the donut graph, then draw
    clockwise = parameters.get('clockwise', True)
    
    start_angle = 0
    end_angle = 0
    if clockwise:
        start_angle = -90
        end_angle = start_angle + (3.6 * percent)
    else:
        end_angle = -90
        start_angle = end_angle - (3.6 * percent)
    pie_color = parameters['color'] if 'color' in parameters else colors.CRIMSON
    draw.pieslice([(0, 0), (width, height)], start_angle, end_angle, fill=pie_color)
    
    # fill in the center of the donut graph
    thickness = 100
    draw.ellipse([(thickness, thickness), (width - thickness, height - thickness)], fill=colors.WHITE)
    
    # draw the percentage number in SuecaSlab Light
    default_percent_text = str(int(percent)) + '%' if float(percent).is_integer() else str(percent) + '%'
    percent_text = parameters.get('label', default_percent_text)
    if percent_text == '':
        percent_text = default_percent_text
        
    percent_text_length = len(percent_text.replace('.', '').replace(',', ''))
    # font size should depend on the length of the percentage string
    percent_font_size = {
        1: 400,
        2: 350,
        3: 300,
        4: 225
    }.get(percent_text_length, 225)
    percent_font = ImageFont.truetype(fonts.SLAB_LIGHT, percent_font_size)
    # location of percentage text also depends on length of percentage string
    percent_text_size = draw.textsize(percent_text, percent_font)[0]
    draw.text(((width / 2) - (percent_text_size / 2), .19 * height), percent_text, fill=colors.BLACK, font=percent_font)
    
    # adds description text, one line for now
    if 'description' in parameters:
        description = parameters['description']
        description_lines = []
        if type(description) == list:
            description_lines = description
        elif description != '':
            description_lines = separate_into_lines(description, [17, 15])
        
        description_font = ImageFont.truetype(fonts.SLAB_HEAVY, 90)
        line_counter = 0
        for line in description_lines:
            line_size = draw.textsize(line, description_font)[0]
            draw.text(((width / 2) - (line_size / 2), height / 2 + (line_counter * 100)), line, fill=colors.BLACK, font=description_font)
            line_counter += 1
    
    return present_image(img, parameters)

# generates a rating graph
# Parameters:
#   values (list) : list of three percentages, as numbers from 0 to 100
# Optional Parameters:
#   padding (int) : amount of padding on the outside of the image (defaults to 50)
#   labels (boolean) : determines whether to show labels or not (defaults to True)
def rating(values, parameters={}):
    num_values = 3
    if len(values) != num_values:
        return
    total = sum(values)
    
    labels = parameters.get('labels', False)
    label_height = 75 if labels else 0
    
    padding = parameters.get('padding', 50)
    base_width = 1000
    base_height = 150
    width = base_width + (2 * padding)
    height = base_height + (2 * padding) + label_height
    
    img = Image.new('RGB', (width, height), colors.WHITE)
    draw = ImageDraw.Draw(img)
    
    # draw the three rectangles
    color_palette = [colors.CRIMSON, colors.GRAY, colors.GREEN]
    offset = 0
    dividers = []
    for index in range(0, num_values):
        length = base_width * (float(values[index]) / total)
        bounds = [(padding + offset, label_height + padding),
                  (padding + offset + length, label_height + padding + base_height)]
        draw.rectangle(bounds, fill=color_palette[index])
        offset += length
        dividers.append(offset)
        
    # draw the two dividers
    divider_width = 15
    for index in range(0, num_values - 1):
        bounds = [(padding + dividers[index] - (float(divider_width) / 2), label_height + padding),
                  (padding + dividers[index] + (divider_width / 2), label_height + padding + base_height)]
        draw.rectangle(bounds, fill=colors.LIGHT_GRAY)
        
    # draw the labels if labels are on:
    if labels:
        label_font = ImageFont.truetype(fonts.SANS, 50)
        old_offset = 0
        for index in range(0, num_values):
            offset = dividers[index]
            line = str(values[index]) + '%'
            line_size = draw.textsize(line, label_font)[0]
            origin = (padding + old_offset + ((offset - old_offset) / 2.0) - (line_size / 2.0), padding + (0.2 * label_height))
            if values[index] != 0:
                draw.text(origin, line, fill=color_palette[index], font=label_font)
            old_offset = offset
        
    return present_image(img, parameters)
    
    
