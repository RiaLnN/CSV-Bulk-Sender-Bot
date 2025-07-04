from aiogram import Bot
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv
import pandas as pd
import os
import csv
router = Router()
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!\nI can send message from CSV files\nJust send me file!")

@router.message(F.document)
async def get_csv(message: Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "send_message.csv")
    with open('send_message.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            try:
                await bot.send_message(chat_id=row[1].strip(), text=row[2].strip())
                print(row[1], row[2])
            except Exception:
                pass




@router.message()
async def echo_handler(message: Message) -> None:
    await message.answer("Use commands or send CSV file")

