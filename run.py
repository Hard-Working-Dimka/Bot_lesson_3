import asyncio
import logging

from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from environs import env
from dialog_flow_instruments import detect_intent_texts_for_tg

env.read_env()
bot_dispatcher = Dispatcher()
dev_bot_dispatcher = Dispatcher()
dev_tg_token = env('DEV_TG_TOKEN')
tg_token = env('TG_TOKEN')
bot = Bot(token=tg_token)
dev_bot = Bot(token=dev_tg_token)
chat_id = env('CHAT_ID')


class MyLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        asyncio.create_task(self.tg_bot.send_message(self.chat_id, log_entry))


@bot_dispatcher.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f'Привет, {html.bold(message.from_user.full_name)}!')


@bot_dispatcher.message()
async def echo_handler(message: Message):
    try:
        await message.answer(detect_intent_texts_for_tg(project_id, message.from_user.id, message.text, "ru"))
    except Exception as error:
        logger_1.error(error, exc_info=True)


async def start_bots():
    task_bot = asyncio.create_task(bot_dispatcher.start_polling(bot))
    task_dev_bot = asyncio.create_task(dev_bot_dispatcher.start_polling(dev_bot))
    logger_1.info('Telegram bot is running.')
    await task_bot
    await task_dev_bot


if __name__ == "__main__":
    env.read_env()
    project_id = env('PROJECT_ID')
    dev_tg_token = env('DEV_TG_TOKEN')
    chat_id = env('CHAT_ID')
    tg_token = env('TG_TOKEN')

    bot = Bot(token=tg_token)
    dev_bot = Bot(token=dev_tg_token)

    logger_1 = logging.getLogger('tg_bot')
    logger_1.setLevel(level=logging.DEBUG)
    logger_1.addHandler(MyLogsHandler(dev_bot, chat_id=chat_id))
    asyncio.run(start_bots())
