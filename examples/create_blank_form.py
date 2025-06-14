"""Create a simple blank form template for demonstration."""
from PIL import Image, ImageDraw

width, height = 400, 300
img = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(img)
for y in [60, 100, 140, 180, 220]:
    draw.line([(50, y+10), (350, y+10)], fill='black')
img.save('blank_form.png')
print('Created blank_form.png')
