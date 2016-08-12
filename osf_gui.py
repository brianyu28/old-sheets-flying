# graphical front-end for OSF
import osf
import easygui as gui
from subprocess import Popen, PIPE
from Tkinter import Tk
from re import search

def main():
    msg = "Welcome to Old Sheets Flying. Please choose a service."
    title = "Old Sheets Flying : The Harvard Crimson"
    
    GRAPHIC_DONUT = "Graphic : Donut"
    ABOUT = "About This Program"
    choices = [
        GRAPHIC_DONUT,
        ABOUT
    ]
    gain_focus()
    choice = gui.choicebox(msg, title, choices)
    if (choice == None):
        return
    elif (choice == GRAPHIC_DONUT):
        graphic_donut()
    elif (choice == ABOUT):
        about()
    else:
        return
        
def about():
    gui.msgbox("Old Sheets Flying\nCreated by Brian Yu\nCopyright 2016")
    
def graphic_donut():
    msg = "Enter information for this donut graph."
    title = "Donut Graph"
    field_names = ["Percent (0-100)", "Description (Text)"]
    field_values = gui.multenterbox(msg, title, field_names)
    
    percent_value = float(field_values[0].replace('%', ''))
    percent_label = field_values[0].replace('%', '') + '%'
    description = field_values[1]
    
    img = osf.graphics.donut(percent_value, {"label":percent_label, "description":description})
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