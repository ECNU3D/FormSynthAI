import json
from pathlib import Path
from typing import Dict, Any

from PIL import Image, ImageDraw, ImageFont
from faker import Faker

faker = Faker()


def load_config(path: str) -> Dict[str, Any]:
    """Load configuration file describing form template and fields."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_value(name: str) -> str:
    """Generate synthetic value based on field name heuristics."""
    lname = name.lower()
    if 'name' in lname:
        return faker.name()
    if 'address' in lname:
        return faker.address().replace('\n', ' ')
    if 'date' in lname:
        return faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
    if 'phone' in lname:
        return faker.phone_number()
    if 'email' in lname:
        return faker.email()
    return faker.word()


def render_field(draw: ImageDraw.Draw, text: str, x: int, y: int,
                 font_path: str = None, font_size: int = 20,
                 handwritten: bool = False) -> None:
    """Render a text field at a given position."""
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()
    if handwritten:
        # Apply slight rotation for handwriting effect
        tmp = Image.new('RGBA', draw.im.size, (255, 255, 255, 0))
        tdraw = ImageDraw.Draw(tmp)
        tdraw.text((x, y), text, fill='black', font=font)
        rotated = tmp.rotate(faker.pyfloat(min_value=-2, max_value=2), resample=Image.BICUBIC)
        draw.bitmap((0, 0), rotated, rotated)
    else:
        draw.text((x, y), text, fill='black', font=font)


def generate_form(config_path: str, output_path: str,
                  handwritten: bool = False, font_path: str = None) -> None:
    cfg = load_config(config_path)
    template_path = Path(cfg['template_path'])
    image = Image.open(template_path).convert('RGBA')
    draw = ImageDraw.Draw(image)

    for field_name, params in cfg['fields'].items():
        text = generate_value(field_name)
        x = params.get('x', 0)
        y = params.get('y', 0)
        size = params.get('font_size', 20)
        render_field(draw, text, x, y, font_path=font_path,
                     font_size=size, handwritten=handwritten)

    image.convert('RGB').save(output_path)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate synthetic filled form')
    parser.add_argument('config', help='Path to JSON config describing fields')
    parser.add_argument('output', help='Output image path')
    parser.add_argument('--handwritten', action='store_true',
                        help='Render text with handwriting effect')
    parser.add_argument('--font', help='Optional TrueType font path')
    args = parser.parse_args()

    generate_form(args.config, args.output, handwritten=args.handwritten,
                  font_path=args.font)


if __name__ == '__main__':
    main()
