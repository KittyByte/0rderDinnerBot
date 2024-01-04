import os
from pathlib import Path
import re
from string import punctuation
from PIL import Image
from pytesseract import pytesseract
from loader import logging


class OCR:
    def __init__(self):
        self.__path = Path(__file__).parent.parent / 'downloads'  # ....\OrderDinnerBot\downloads
        self.__order_photo_path = self.__path / 'order.jpg'  # путь к фото для обрезки
        self.__path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe' if os.name == 'nt' else '/usr/bin/tesseract'
        self.__cropped_image_path = self.__path / 'cropped_order.jpg'

    def __crop_photo(self, path=None):
        path = path if path else self.__order_photo_path
        # обрезка фото
        img = Image.open(path)
        img = img.resize((1080, 1080))  # апскейл(расширение/сужение) фото до формата 1080x1080
        crop_img = img.crop((0, 180, 1070, 880))   # left, top, right, bottom
        crop_img.save(self.__cropped_image_path)
        # удаление лишних элементов, всех кроме букв
        img = Image.open(self.__cropped_image_path)
        pixels = img.load()
        all_color_range_rgb = [(i, i, i) for i in range(256)]
        for i in range(img.size[0]):  # проходим по каждому пикселю:
            for j in range(img.size[1]):
                if pixels[i, j] not in all_color_range_rgb:  # если не черный:
                    pixels[i, j] = (255, 255, 255)  # изменить на белый

        img.save(self.__cropped_image_path)

    @staticmethod
    def __format_text(text):
        def clear(txt: str) -> str:
            symbols: str = punctuation.replace('-', '') + '"”“'
            return re.sub(f"[{symbols}]", "", txt).capitalize().strip()

        lst_meals = [clear(text) for text in text.split('\n') if text and "дня" not in text.lower()]
        meals = []
        temp_str = ''
        for meal in lst_meals:
            if 'руб' not in meal:
                temp_str += meal
            else:
                meals.append(f'{temp_str} {meal}'[:-7].strip().capitalize())
                temp_str = ''
        meals[1], meals[2] = meals[2], meals[1]
        meals[3], meals[4] = meals[4], meals[3]
        meals[1], meals[4] = meals[4], meals[1]

        logging.info(f'Фото обрезано и очищено, получен текст - {meals}')
        return meals

    def img_to_text(self, path=None) -> list[str]:
        self.__crop_photo(path)

        img = Image.open(self.__cropped_image_path)
        pytesseract.tesseract_cmd = self.__path_to_tesseract
        text: str = pytesseract.image_to_string(img, lang='rus')

        return self.__format_text(text)


ocr = OCR()
