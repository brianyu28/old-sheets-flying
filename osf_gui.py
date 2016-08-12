# graphical front-end for OSF
import osf

import easygui as gui
from subprocess import Popen, PIPE
from Tkinter import Tk
from re import search

def main():
    msg = "Welcome to Old Sheets Flying. Please choose a service."
    title = "Old Sheets Flying : The Harvard Crimson"
    
    QUOTE_NEWS = "Quote Card : News"
    QUOTE_OPINION = "Quote Card : Opinion"
    GRAPHIC_DONUT = "Graphic : Donut - Simple"
    GRAPHIC_DONUT_CUSTOM = "Graphic : Donut - Custom"
    ABOUT = "About This Program"
    choices = [
        QUOTE_NEWS,
        QUOTE_OPINION,
        GRAPHIC_DONUT,
        GRAPHIC_DONUT_CUSTOM,
        ABOUT
    ]
    gain_focus()
    choice = gui.choicebox(msg, title, choices)
    if (choice == None):
        return
    elif (choice == QUOTE_NEWS):
        quote(False)
    elif (choice == QUOTE_OPINION):
        quote(True)
    elif (choice == GRAPHIC_DONUT):
        graphic_donut()
    elif (choice == GRAPHIC_DONUT_CUSTOM):
        graphic_donut_custom()
    elif (choice == ABOUT):
        about()
    else:
        return
        
def about():
    gui.msgbox("Old Sheets Flying\nCreated by Brian Yu\nCopyright 2016")

def quote(is_opinion):
    msg = "Quote Card Generator"
    title = "Quote Card"
    field_names = ["Quote", "Author", "Position"]
    field_values = gui.multenterbox(msg, title, field_names)
    if field_values == None:
        return
    quote = field_values[0]
    author = field_values[1]
    position = field_values[2]
    
    img = osf.quotes.quote(quote, author, position, {"opinion":is_opinion})
    img.show()
    
def graphic_donut():
    msg = "Donut Graph"
    title = "Donut Graph"
    field_names = ["Headline (optional)", "Percent (0-100)", "Description (Text)"]
    field_values = gui.multenterbox(msg, title, field_names)
    if field_values == None:
        return
    
    headline = field_values[0]
    percent_value = float(field_values[1].replace('%', ''))
    percent_label = field_values[1].replace('%', '') + '%'
    description = field_values[2]
    
    img = osf.graphics.donut(percent_value, {"label":percent_label, "description":description, "headline":headline})
    img.show()
    
def graphic_donut_custom():
    msg = "Custom Donut Graph: leave fields blank for default"
    title = "Donut Graph - Custom"
    field_names = ["Headline (optional)", "Percent (0-100)", "Description (Text)", "Label (Text)", "Color (Red, 0-255)", "Color (Green, 0-255)", "Color (Blue, 0-255)", "Clockwise (y/n)", "Grayscale (y/n/b)"]
    field_values = gui.multenterbox(msg, title, field_names)
    if field_values == None:
        return
    
    headline = field_values[0]
    percent_value = float(field_values[1].replace('%', ''))
    description = field_values[2]
    percent_label = field_values[3]
    color_red = int(field_values[4]) if field_values[4] != '' else osf.colors.CRIMSON[0]
    color_green = int(field_values[5]) if field_values[5] != '' else osf.colors.CRIMSON[1]
    color_blue = int(field_values[6]) if field_values[6] != '' else osf.colors.CRIMSON[2]
    clockwise = not (field_values[7] in osf.constants.NO_OPTIONS)
    grayscale = field_values[8] in osf.constants.YES_OPTIONS
    
    parameters = {
        "label": percent_label,
        "description": description,
        "color": (color_red, color_green, color_blue),
        "clockwise": clockwise,
        "headline": headline,
        "grayscale": grayscale
    }
    
    if (field_values[8] in osf.constants.BOTH_OPTIONS):
        parameters["grayscale"] = not parameters["grayscale"]
        img = osf.graphics.donut(percent_value, parameters)
        img.show()
        parameters["grayscale"] = not parameters["grayscale"]
    
    img = osf.graphics.donut(percent_value, parameters)
    img.show()
    
def gain_focus():
    t = Tk()
    t.destroy()
    find_cmd_str = 'ps -o command | grep "%s"'%__file__
    find_results = Popen(find_cmd_str, shell=True, stdout=PIPE).stdout.read()
    py_path = search('(.*Python\.app)', find_results).groups()[0]
    Popen(['open',py_path])
    
if __name__ == '__main__':
    main()