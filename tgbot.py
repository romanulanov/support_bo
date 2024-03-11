import os
import requests
import telegram

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from df_API import detect_intent_texts
from tg_logger import TelegramLogsHandler


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Здравствуйте")


def send_answer(update, context):
    has_answer, bot_message = detect_intent_texts(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=bot_message)


def main():
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    bot = telegram.Bot(token=bot_token)
    bot.logger.addHandler(TelegramLogsHandler(bot, os.environ['TELEGRAM_CHAT_ID']))
    bot.logger.warning('Телеграм бот запущен')
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, send_answer))

    try:
        updater.start_polling()
        updater.idle()
    except requests.exceptions.HTTPError as err:
        bot.logger.warning(f'Телеграм бот упал с ошибкой {err}')
   

if __name__ == '__main__':
    main()
