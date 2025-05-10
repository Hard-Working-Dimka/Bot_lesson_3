import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from environs import env
from dialog_flow_instruments import detect_intent_texts

env.read_env()
TOKEN = env('BOT_TOKEN')
PROJECT_ID = env('PROJECT_ID')
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f'Привет, {html.bold(message.from_user.full_name)}!')


@dp.message()
async def echo_handler(message: Message):
    try:
        await message.answer(detect_intent_texts(PROJECT_ID, message.from_user.id, message.text, "ru"))
    except TypeError:
        await message.answer("Nice try!")


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
