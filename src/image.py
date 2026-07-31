from PIL import Image, ImageFilter, ImageEnhance

with Image.open('figma.png') as picture:
    picture = picture.convert('RGBA')

    contrast = ImageEnhance.Contrast(picture)
    contrast = contrast.enhance(2.5)
    contrast.save('Contrast.png')

    color = ImageEnhance.Color(picture)
    color = color.enhance(2)
    color.save('color.png')