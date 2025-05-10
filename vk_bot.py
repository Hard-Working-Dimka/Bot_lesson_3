import asyncio
import logging

from environs import env
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import run
from dialog_flow_instruments import detect_intent_texts_for_vk


class LogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot
        self.loop = asyncio.get_event_loop()

    def emit(self, record):
        log_entry = self.format(record)
        # Синхронный вызов асинхронной функции через loop.run_until_complete()
        self.loop.run_until_complete(self.send_telegram_message(log_entry))

    async def send_telegram_message(self, message):
        await self.tg_bot.send_message(self.chat_id, message)


def echo(event, vk_api):
    message = detect_intent_texts_for_vk(project_id, event.user_id, event.text, "ru")
    if message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    env.read_env()
    project_id = env("PROJECT_ID")
    vk_session = vk.VkApi(token=env('VK_API_KEY'))
    logger_2 = logging.getLogger('vk_bot')
    logger_2.setLevel(logging.DEBUG)
    logger_2.addHandler(LogsHandler(run.dev_bot, run.chat_id))
    try:
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        logger_2.info('VK bot is running.')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)
    except Exception as error:
        logger_2.error(error, exc_info=True)
