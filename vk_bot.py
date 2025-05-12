import logging

import telegram
from environs import env
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow_instruments import detect_intent_texts
from tg_bot import LogsHandler


def reply_from_dialogflow(event, vk_api):
    message = detect_intent_texts(project_id, 'vk-' + str(event.user_id), event.text, "ru")
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
    chat_id = env('CHAT_ID')
    dev_bot = telegram.Bot(token=env('DEV_TG_TOKEN'))

    logger = logging.getLogger('bots')
    logger.setLevel(level=logging.DEBUG)
    logger.addHandler(LogsHandler(dev_bot, chat_id=chat_id))

    try:
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        logger.info('VK bot is running.')

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply_from_dialogflow(event, vk_api)
    except Exception as error:
        logger.error(error, exc_info=True)
