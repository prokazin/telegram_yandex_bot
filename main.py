import logging
import requests
import base64
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from config import TELEGRAM_TOKEN, YANDEX_API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

YANDEX_AI_URL = "https://generativeai.api.cloud.yandex.net/v1/images:generate"

def enhance_image(image_bytes):
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "anime-portrait",
        "input_image": encoded_image
    }
    response = requests.post(YANDEX_AI_URL, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    enhanced_image_base64 = result['output_image']
    return base64.b64decode(enhanced_image_base64)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_bytes = await bot.download_file(file.file_path)
    image_bytes = file_bytes.read()

    await message.reply("Оживляю фото... ⏳")

    try:
        enhanced_image = enhance_image(image_bytes)
        with open("enhanced.png", "wb") as f:
            f.write(enhanced_image)
        await message.reply_photo(InputFile("enhanced.png"))
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Отправь мне фотографию, и я её оживлю!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
