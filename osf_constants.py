NO_OPTIONS = ["n", "N", "no", "No", "NO", "0"]
YES_OPTIONS = ["y", "Y", "yes", "Yes", "YES", "1"]
BOTH_OPTIONS = ["both", "Both", "BOTH", "b", "B"]

PAGE_HEIGHT = 1470 # in pixels
COLUMN_WIDTH = 156 # in pixels
COLUMN_SPACING = 12 # in pixels

# function to define pixel with of columns, given number of columns
def width(cols):
    return (COLUMN_WIDTH * cols) + (COLUMN_SPACING * (cols - 1))
