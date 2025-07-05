from aiogram import Bot
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
import os
import csv
import sqlite3

router = Router()
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)

class Users:
    def __init__(self, name, id, message):
        self.name = name
        self.id = id
        self.message = message

    def __repr__(self):
        return f"MyClass(name={self.name}, id={self.id}, message={self.message})"

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (name TEXT, id TEXT, message TEXT)''')
conn.commit()

def insert_data(user):
    with conn:
        c.execute("INSERT OR IGNORE INTO users VALUES (:name, :id, :message)",
                  {'name': user.name, 'id': user.id, 'message': user.message})

def check_user_exists(user_id):
    c.execute("SELECT COUNT(*) FROM users WHERE id = ?", (user_id,))
    return c.fetchone()[0] > 0

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!\nI can send message from CSV files\nJust send me file!")


@router.message(F.document)
async def get_csv(message: Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    if not '.csv' in file_path:
        await message.answer('The CSV file is not formed correctly')
        return
    await bot.download_file(file_path, "send_message.csv")

    with open('send_message.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) < 3:
                continue
            try:
                await bot.send_message(chat_id=row[1].strip(), text=row[2].strip())
                await message.answer(f"The message was sent to the user: {row[0].strip()} with id: {row[1].strip()}")
                print(row[1], row[2])
            except Exception as e:
                print(f"Error sending to {row[1]}: {e}")
            if check_user_exists(row[1].strip()):
                print(f"User {row[1].strip()} already exists, skipping...")
                continue
            user = Users(row[0], row[1], row[2])
            insert_data(user)

    os.remove("send_message.csv")

@router.message(Command("send"))
async def send_text(message: Message):
    c.execute("SELECT id, message FROM users")
    values = c.fetchall()
    for value in values:
        user_id = value[0]
        user_send = value[1]
        try:
            # value is a tuple, so we need to access the first element
            await bot.send_message(chat_id=user_id, text=user_send)
            await message.answer(f"Sent to: {user_id}")
        except Exception as e:
            print(f"Error sending to {user_id}: {e}")

@router.message()
async def echo_handler(message: Message) -> None:
    await message.answer("Use commands or send CSV file")

