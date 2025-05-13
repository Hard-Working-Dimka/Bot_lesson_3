import telegram
from environs import env
from dialog_flow_instruments import detect_intent_texts
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


class LogsHandler(logging.Handler):
    def __init__(self, dev_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.dev_bot = dev_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.dev_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def reply_from_dialogflow(update: Update, context: CallbackContext, project_id):
    update.message.reply_text(
        (detect_intent_texts(project_id, f'tg-{update.effective_user.id}', update.message.text, "ru")))


def start_bot(tg_token, project_id):
    try:
        tg_bot = Updater(tg_token)

        dispatcher = tg_bot.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                              lambda update, context: reply_from_dialogflow(update, context,
                                                                                            project_id)))
        logger.info('Telegram bot is running.')

        tg_bot.start_polling()
        tg_bot.idle()
    except Exception as error:
        logger.exception(error)


if __name__ == '__main__':
    env.read_env()
    project_id = env('PROJECT_ID')
    chat_id = env('CHAT_ID')
    tg_token = env('TG_TOKEN')

    dev_bot = telegram.Bot(token=env('DEV_TG_TOKEN'))

    logger = logging.getLogger('bots')
    logger.setLevel(level=logging.DEBUG)
    logger.addHandler(LogsHandler(dev_bot, chat_id=chat_id))

    start_bot(tg_token, project_id)
