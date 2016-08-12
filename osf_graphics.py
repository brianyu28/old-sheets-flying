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

# generates a donut graphic representing a single data point (percentage)
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
    percent_text = parameters.get('label', str(percent) + '%')
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
        else:
            description_lines = separate_into_lines(description, [17, 15])
        
        description_font = ImageFont.truetype(fonts.SLAB_HEAVY, 90)
        line_counter = 0
        for line in description_lines:
            line_size = draw.textsize(line, description_font)[0]
            draw.text(((width / 2) - (line_size / 2), height / 2 + (line_counter * 100)), line, fill=colors.BLACK, font=description_font)
            line_counter += 1
        
    
    return img