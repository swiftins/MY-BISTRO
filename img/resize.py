import os
from PIL import Image

# Укажите путь к основному каталогу
base_dir = "./"

def resize_image(image_path, save_path, new_width=600):
    """Изменяет размер изображения до указанной ширины с сохранением пропорций"""
    with Image.open(image_path) as img:
        width_percent = new_width / float(img.size[0])
        new_height = int(float(img.size[1]) * width_percent)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_img.save(save_path)

def process_directory(directory):
    """Проходит по каталогу, находит JPEG и сохраняет в NewJPEG"""
    for root, dirs, files in os.walk(directory):
        if ".venv" in root or '.idea' in root or 'JPGnew' in root:
            continue

        if "JPG" in root:
            new_jpeg_dir = root.replace("\\JPG", "")
            #os.makedirs(new_jpeg_dir, exist_ok=True)
            
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(root, file)
                    save_path = os.path.join(new_jpeg_dir, file)
                    
                    resize_image(image_path, save_path)
                    print(f"Сохранено: {save_path}")

# Запуск обработки
process_directory(base_dir)
