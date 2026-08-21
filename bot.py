import os
from PIL import Image

# Список файлов изображений товаров
image_files = [
    "mint.jpg", 
    "grape_plus.jpg", 
    "watermelon.jpg",
    "energy_raspberry.jpg", 
    "pink_lemonade.jpg",
    "triple_raspberry.jpg", 
    "blueberry_mint.jpg",
    "tropic_punch.jpg", 
    "energy_cherry.jpg", 
    "pineapple.jpg"
]

TARGET_SIZE = (600, 600)      # Единый размер картинки
BACKGROUND_COLOR = (255, 255, 255)  # Чисто белый фон (#FFFFFF)

def process_image(file_path):
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден, пропускаем.")
        return
    
    try:
        img = Image.open(file_path).convert("RGBA")
        
        # 1. Заменяем все светлые оттенки фонов (RGB > 230) на чисто белый
        datas = img.getdata()
        new_data = []
        for item in datas:
            if item[0] > 230 and item[1] > 230 and item[2] > 230:
                new_data.append((255, 255, 255, 255))
            else:
                new_data.append(item)
        img.putdata(new_data)
        
        # 2. Пропорционально подгоняем размер флакона под 480x480
        img.thumbnail((480, 480), Image.Resampling.LANCZOS)
        
        # 3. Создаем идеальный белый холст 600x600 и ставим флакон ровно по центру
        final_img = Image.new("RGB", TARGET_SIZE, BACKGROUND_COLOR)
        offset = ((TARGET_SIZE[0] - img.size[0]) // 2, (TARGET_SIZE[1] - img.size[1]) // 2)
        
        if img.mode == 'RGBA':
            final_img.paste(img, offset, mask=img.split()[3])
        else:
            final_img.paste(img, offset)
            
        # Сохраняем результат
        final_img.save(file_path, "JPEG", quality=98)
        print(f"Изображение {file_path} успешно обработано!")
    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")

if __name__ == "__main__":
    for filename in image_files:
        process_image(filename)
