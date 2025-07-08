from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import base64
from io import BytesIO
import random

def create_captcha_image(text, output_path="captcha.png"):
    width, height = 180, 70
    background = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(background)

    # Font ayarı
    try:
        font = ImageFont.truetype("arial.ttf", 38)
    except:
        font = ImageFont.load_default()

    # Arka plan randomları
    for _ in range(random.randint(150, 250)):
        x, y = random.randint(0, width), random.randint(0, height)
        color = tuple(random.randint(180, 255) for _ in range(3))
        draw.point((x, y), fill=color)

    # Metni ayrı çizgide çizelim
    text_layer = Image.new('RGBA', background.size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_layer)

    # mat
    total_width = len(text) * 30
    start_x = (width - total_width) // 2

    # Her harfi çiz ve döndür
    for i, char in enumerate(text):
        char_img = Image.new('RGBA', (40, 60), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)

        angle = random.randint(-25, 25)
        char_color = tuple(random.randint(0, 100) for _ in range(3))

        char_draw.text((5, 5), char, font=font, fill=char_color)

        rotated_char = char_img.rotate(angle, expand=1)
        char_x = start_x + i * 30
        char_y = random.randint(5, 15)

        text_layer.paste(rotated_char, (char_x, char_y), rotated_char)

    # Metni arka plana yapıştır
    combined = Image.alpha_composite(background.convert("RGBA"), text_layer)

    # Çizgileri en son metnin üstüne çiz
    final_draw = ImageDraw.Draw(combined)
    for _ in range(6):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        line_color = tuple(random.randint(0, 100) for _ in range(3))
        final_draw.line([start, end], fill=line_color, width=random.randint(1, 2))

    # Blur efekti
    combined = combined.filter(ImageFilter.GaussianBlur(0.7))

    # Kaydet ve göster
    combined.convert("RGB").save(output_path)
    combined.show()

def create_advanced_captcha(text, output_path="captcha.png"):
    width, height = 240, 90
    background = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(background)
    
    # Fontlar
    fonts = []
    for font_name in ['arial.ttf', 'timesbd.ttf', 'verdana.ttf', 'courbd.ttf', 'comic.ttf']:
        try:
            fonts.append(ImageFont.truetype(font_name, random.randint(38, 44)))
        except:
            continue
    if not fonts:
        fonts = [ImageFont.load_default()]

    # Arka plan randomları
    for _ in range(random.randint(150, 250)):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.rectangle([x, y, x+1, y+1], fill=tuple(random.randint(200, 255) for _ in range(3)))
    
    # Karakterleri oluştur
    char_images = []
    for char in text:
        font = random.choice(fonts)
        color = tuple(random.randint(0, 70) for _ in range(3))
        char_img = Image.new('RGBA', (60, 70), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((10, 10), char, font=font, fill=color)

        angle = random.randint(-25, 25)
        rotated = char_img.rotate(angle, expand=1)

        scale = random.uniform(0.9, 1.05)
        w, h = rotated.size
        new_size = (int(w * scale), int(h * scale))
        resized = rotated.resize(new_size, Image.LANCZOS)

        char_images.append(resized)

    # Sığmazsa hepsini biraz küçült
    total_width = sum(img.width for img in char_images) + (len(text) - 1) * 5
    if total_width > width - 20:
        shrink_ratio = (width - 20) / total_width
        char_images = [img.resize((int(img.width * shrink_ratio), int(img.height * shrink_ratio)), Image.LANCZOS) for img in char_images]
        total_width = sum(img.width for img in char_images) + (len(text) - 1) * 5

    # Ortala
    current_x = (width - total_width) // 2
    text_layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    for char_img in char_images:
        y_pos = random.randint(10, height - char_img.height - 5)
        text_layer.paste(char_img, (current_x, y_pos), char_img)
        current_x += char_img.width + 5

    # Çizgileri METNİN ÜSTÜNE getir
    combined = Image.alpha_composite(background.convert("RGBA"), text_layer)
    draw = ImageDraw.Draw(combined)
    for _ in range(random.randint(3, 5)):
        points = []
        x = random.randint(-10, 0)
        for y in range(0, height, 5):
            x += random.randint(5, 7)
            points.append((x, y))
            if x > width: break
        line_color = tuple(random.randint(40, 120) for _ in range(3))
        draw.line(points, fill=line_color, width=random.randint(1, 2))

    # Efekt
    combined = combined.filter(ImageFilter.GaussianBlur(radius=0.4))
    final = ImageOps.autocontrast(combined.convert("RGB"))

    final.save(output_path)
    final.show()
    return final

def create_base64_image(text):
    width, height = 240, 90
    background = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(background)
    
    # Fontlar
    fonts = []
    for font_name in ['arial.ttf', 'timesbd.ttf', 'verdana.ttf', 'courbd.ttf', 'comic.ttf']:
        try:
            fonts.append(ImageFont.truetype(font_name, random.randint(38, 44)))
        except:
            continue
    if not fonts:
        fonts = [ImageFont.load_default()]

    # Arka plan randomları
    for _ in range(random.randint(150, 250)):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.rectangle([x, y, x+1, y+1], fill=tuple(random.randint(200, 255) for _ in range(3)))
    
    # Karakterleri oluştur
    char_images = []
    for char in text:
        font = random.choice(fonts)
        color = tuple(random.randint(0, 70) for _ in range(3))
        char_img = Image.new('RGBA', (60, 70), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((10, 10), char, font=font, fill=color)

        angle = random.randint(-25, 25)
        rotated = char_img.rotate(angle, expand=1)

        scale = random.uniform(0.9, 1.05)
        w, h = rotated.size
        new_size = (int(w * scale), int(h * scale))
        resized = rotated.resize(new_size, Image.LANCZOS)

        char_images.append(resized)

    # Genişlik hesapla
    total_width = sum(img.width for img in char_images) + (len(text) - 1) * 5
    if total_width > width - 20:
        shrink_ratio = (width - 20) / total_width
        char_images = [
            img.resize((int(img.width * shrink_ratio), int(img.height * shrink_ratio)), Image.LANCZOS)
            for img in char_images
        ]
        total_width = sum(img.width for img in char_images) + (len(text) - 1) * 5

    # Metni ortala
    current_x = (width - total_width) // 2
    text_layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    for char_img in char_images:
        y_pos = random.randint(10, height - char_img.height - 5)
        text_layer.paste(char_img, (current_x, y_pos), char_img)
        current_x += char_img.width + 5

    # Çizgileri metnin üstüne getir
    combined = Image.alpha_composite(background.convert("RGBA"), text_layer)
    draw = ImageDraw.Draw(combined)
    for _ in range(random.randint(3, 5)):
        points = []
        x = random.randint(-10, 0)
        for y in range(0, height, 5):
            x += random.randint(5, 7)
            points.append((x, y))
            if x > width:
                break
        line_color = tuple(random.randint(40, 120) for _ in range(3))
        draw.line(points, fill=line_color, width=random.randint(1, 2))

    # Blur
    combined = combined.filter(ImageFilter.GaussianBlur(radius=0.4))
    final = ImageOps.autocontrast(combined.convert("RGB"))

    # Base64 encode
    buffer = BytesIO()
    final.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()

    return encoded