from aiogram import types

import json
import os
import io

from src.core import BASE_DIR

file = os.path.join(BASE_DIR, "questions_to_states.txt")


def get_questions_to_states():
    data = load_data(file)
    return data


def load_data(file_):
    with open(file_, "r", encoding="utf-8") as doc:
        data = json.load(doc)
        return data


async def get_media_from_user(message: types.Message):
    if message.photo:
        file_info = await message.bot.get_file(message.photo[-1].file_id)
        downloaded_file = await message.bot.download_file(file_info.file_path)
    else:
        file_id = message.document.file_id
        file_info = await message.bot.get_file(file_id)
        downloaded_file = await message.bot.download_file(file_info.file_path)
    bytes_of_media = io.BytesIO(downloaded_file.read()).getvalue()
    print(bytes_of_media)

    return bytes_of_media
