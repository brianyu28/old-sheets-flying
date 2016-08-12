# quote card graphics
from PIL import Image, ImageFont, ImageDraw
import textwrap
import osf_fonts as fonts
import osf_colors as colors
import osf_static as static

quotetext_font = ImageFont.truetype(fonts.SLAB_LIGHT, 60)
authortext_font = ImageFont.truetype(fonts.SLAB_HEAVY, 60)
titletext_font = ImageFont.truetype(fonts.SLAB_LIGHT, 45)
opinion_font = ImageFont.truetype(fonts.SLAB_SEMI, 60)
thc_op_font = ImageFont.truetype(fonts.BIG_MOORE, 18)
thc_font = ImageFont.truetype(fonts.BIG_MOORE, 36)

# generates a quote card
# Optional Parameters
#   opinion (boolean) : determiens if opinion quote or not (defaults to no)
def quote(quote, author, position, parameters={}):
    opinion = parameters.get('opinion', False)
    breakquote = textwrap.wrap(quote, width=35)

    img = None
    if opinion:
        img = Image.new('RGB', (1120, 600), colors.CRIMSON)
        draw = ImageDraw.Draw(img)
        counter = 0
        for line in breakquote:
            draw.text((28,50 + (counter * 60)), line, font=quotetext_font, fill=colors.WHITE)
            counter += 1
        draw.text((28, 420), author, font=authortext_font, fill=colors.WHITE)
        draw.text((28, 490), position, font=titletext_font, fill=colors.WHITE)

        draw.text((860, 510), "opinion", font=opinion_font, fill=colors.WHITE)
        draw.text((922, 570), "The Harvard Crimson", font=thc_op_font, fill=colors.WHITE)
    else:
        seal = Image.open(static.SEAL_TRANS_SM)
        img = Image.new('RGB', (1120,600), colors.WHITE)
        img.paste(seal, (800, 250), seal)
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0,0), (1120, 30)], colors.CRIMSON)
        counter = 0
        for line in breakquote:
            draw.text((28,50 + (counter * 60)), line, font=quotetext_font, fill=colors.CRIMSON)
            draw.text((28, 420), author, font=authortext_font, fill=colors.CRIMSON)
            draw.text((28, 490), position, font=titletext_font, fill=colors.CRIMSON)
            draw.text((775, 550), "The Harvard Crimson", font=thc_font, fill=colors.CRIMSON)
            counter += 1
    return img
