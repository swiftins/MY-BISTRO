import telebot
from telebot import types
import os

TOKEN = '7265481895:AAEiGtEWswZa-Jz0CMf63j-zn9-wWcaOzME'
bot = telebot.TeleBot(TOKEN)

# Обработчик Inline Query
@bot.inline_handler(func=lambda query: True)
def inline_query_handler(query):
    # Путь к папке с изображениями
    image_folder = 'img'

    # Список всех изображений .jpg в каталоге
    images = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

    # Список результатов для Inline Query
    results = []

    # Перебираем изображения
    for i, image_name in enumerate(images):
        # Формируем полный путь к картинке
        image_path = os.path.join(image_folder, image_name)

        # Открываем изображение как InputFile
        with open(image_path, 'rb') as photo:
            input_file = types.InputFile(photo)  # Передаем файл через InputFile

            # Создаем результат для Inline Query
            result = types.InlineQueryResultPhoto(
                id=str(i),
                photo_url=f"attach://{image_name}",  # Миниатюра
                title=image_name,
                description="Выберите изображение",
                thumbnail_url=f"attach://{image_name}"  # Миниатюра изображения
            )

            # Указываем контент, который будет отправлен
            result.input_message_content = types.InputTextMessageContent(f"Изображение: {image_name}")

            # Добавляем результат в список
            results.append(result)

    # Отправляем результаты Inline Query
    bot.answer_inline_query(query.id, results)


# Запуск бота
bot.infinity_polling()
