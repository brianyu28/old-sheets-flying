# Old Sheets Flying - Graphics Library
from PIL import Image, ImageFont, ImageDraw
import textwrap
import osf_fonts as fonts
import osf_colors as colors
import osf_constants as constants

# takes an ad and prepares it for presentation
# parameter values:
#   grayscal (boolean) : determines whether to grayscale image (defaults to False)
def present_ad(img, parameters={}):
    grayscale = parameters.get('grayscale', False)
    if grayscale:
        img = img.convert(mode="LA")
    return img
    
    
# generates a facebook house ad
# width and height are in pixels
def facebook(height, width, parameters):
    width = width
    height = height
    
    # create the image
    img = Image.new('RGB', (width, height), colors.BLUE_3)
    draw = ImageDraw.Draw(img)
    
    lines = {
        "headline0" : {
            "text": "Like",
            "size": 0,
            "center": (0, 0),
            "font": fonts.SLAB
        },

        "headline1" : {
            "text": "The Crimson",
            "size": 0,
            "center": (0, 0),
            "font": fonts.SLAB_SEMI
        },

        "link" : {
            "text": "Facebook.com/TheHarvardCrimson",
            "size": 0,
            "center": (0, 0),
            "font": fonts.SLAB_SEMI
        },

        "dst" : {
            "text": "Don't stop there.",
            "size": 0,
            "center": (0, 0),
            "font": fonts.SLAB
        },

        "link_dst" : {
            "text": "Facebook.com/CrimsonFlyby",
            "size": 0,
            "center": (0, 0),
            "font": fonts.SLAB_SEMI
        }
    }
    
    # four different configuration settings:
    #   vertical large, horizontal large
    #   vertical small, horizontal small
    large = height >= (constants.PAGE_HEIGHT / 2) # height > 735
    vertical = height >= 1.5 * width
    
    
    if (large and vertical):
        lines["headline0"]["size"] = 50
        lines["headline0"]["center"] = ((width / 2), (height / 10))
        
        lines["headline1"]["size"] = 50 + ((width - 490) / 7)
        lines["headline1"]["center"] = ((width / 2), lines["headline0"]["center"][1] + lines["headline1"]["size"])
        
        
    for name, component in lines.iteritems():
        font = ImageFont.truetype(component["font"], component["size"])
        line_width = draw.textsize(component["text"], font)[0]
        draw.text((component["center"][0] - (line_width / 2.0), component["center"][1]), component["text"], fill=colors.BLACK, font=font)
        
    
    return present_ad(img, parameters)