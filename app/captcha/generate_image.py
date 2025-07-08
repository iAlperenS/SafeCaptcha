from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import base64
from io import BytesIO
import random
import numpy as np

def create_strong_captcha(text, output_path="captcha.png"):
    width, height = 240, 90
    background = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(background)

    # Gürültü arka plan
    for _ in range(random.randint(250, 400)):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill=tuple(random.randint(180, 255) for _ in range(3)))

    # Fontlar
    font_names = ['arial.ttf', 'timesbd.ttf', 'verdana.ttf', 'courbd.ttf']
    fonts = []
    for name in font_names:
        try:
            fonts.append(ImageFont.truetype(name, random.randint(36, 44)))
        except:
            continue
    if not fonts:
        fonts = [ImageFont.load_default()]

    # Karakterleri oluştur
    char_images = []
    for char in text:
        font = random.choice(fonts)
        color = tuple(random.randint(0, 70) for _ in range(3))
        angle = random.randint(-30, 30)
        scale = random.uniform(0.9, 1.2)

        char_img = Image.new('RGBA', (60, 70), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((10, 10), char, font=font, fill=color)

        # Rotate ve scale
        rotated = char_img.rotate(angle, expand=1)
        w, h = rotated.size
        resized = rotated.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        char_images.append(resized)

    # Harflerin arasına yuvarlak/kare sıkıştır
    shape_count = random.randint(1, len(char_images) - 1)
    shape_positions = random.sample(range(1, len(char_images)), shape_count)

    for i in shape_positions:
        shape_size = random.randint(8, 14)
        shape_type = random.choice(['circle', 'square'])
        shape_color = tuple(random.randint(50, 120) for _ in range(3)) + (200,)

        shape_img = Image.new('RGBA', (shape_size, shape_size), (255, 255, 255, 0))
        shape_draw = ImageDraw.Draw(shape_img)

        if shape_type == 'circle':
            shape_draw.ellipse([0, 0, shape_size, shape_size], fill=shape_color)
        else:
            shape_draw.rectangle([0, 0, shape_size, shape_size], fill=shape_color)

        char_images.insert(i, shape_img)

    # Genişlik hesapla
    total_width = sum(img.width for img in char_images) + (len(text) - 1) * 5
    if total_width > width - 20:
        shrink = (width - 20) / total_width
        char_images = [img.resize((int(img.width * shrink), int(img.height * shrink)), Image.LANCZOS)
                       for img in char_images]
        total_width = sum(img.width for img in char_images) + (len(text) - 1) * 5

    # Metni katmana çiz
    text_layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    x = (width - total_width) // 2
    for img in char_images:
        y = random.randint(5, height - img.height - 5)
        text_layer.paste(img, (x, y), img)
        x += img.width + 5

    # Çizgiler
    combined = Image.alpha_composite(background.convert("RGBA"), text_layer)
    draw = ImageDraw.Draw(combined)
    for _ in range(random.randint(4, 6)):
        p1 = (random.randint(0, width//2), random.randint(0, height))
        p2 = (random.randint(width//2, width), random.randint(0, height))
        draw.line([p1, p2], fill=tuple(random.randint(60, 120) for _ in range(3)), width=random.randint(2, 3))

    # Gürültü + blur
    combined = combined.filter(ImageFilter.GaussianBlur(0.7))
    final = ImageOps.autocontrast(combined.convert("RGB"))
    # final.save(output_path)
    # final.show() we dont gonna save
    return final

def create_base64_image(text):
    img = create_strong_captcha(text, "temp.png")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()
