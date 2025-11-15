import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TELEGRAM_TOKEN, YANDEX_API_KEY
from yandex.cloud import sdk
import io
import requests

logging.basicConfig(level=logging.INFO)

# Инициализация Telegram бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Инициализация Yandex.Cloud SDK
yc = sdk.SDK(token=YANDEX_API_KEY)

# Клиент Vision AI (или замените на Generative AI для анимации)
vision_client = yc.client("vision.v1.ImageService")  

# Команда /start
@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.answer("Привет! Отправь мне фото, и я попробую его оживить через Yandex AI.")

# Обработка фото
@dp.message(lambda message: message.content_type == "photo")
async def handle_photo(message: types.Message):
    photo = message.photo[-1]  # Берем наибольшее фото
    file_info = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_info.file_path}"

    # Скачиваем фото
    response = requests.get(file_url)
    image_bytes = io.BytesIO(response.content)

    try:
        # ---- РЕАЛЬНЫЙ ВЫЗОВ YANDEX AI ----
        # Пример: если используете Vision AI или Generative AI
        # result_bytes = vision_client.process_image(image_bytes)  # замените на метод своего сервиса
        result_bytes = image_bytes  # пока просто возвращаем исходное фото
        # ----------------------------------

        await message.answer_photo(photo=result_bytes, caption="Оживленное фото!")
    except Exception as e:
        await message.answer(f"Ошибка при обработке фото: {e}")

# Старт бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
