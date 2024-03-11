import os
import requests
import telegram

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from df_API import detect_intent_texts
from tg_logger import TelegramLogsHandler
from google.oauth2 import service_account


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Здравствуйте")


def send_answer(update, context, credentials, project_id, session_id):
    has_answer, bot_message = detect_intent_texts(update.message.text, credentials, project_id, session_id)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=bot_message)


def main():
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    project_id = os.environ['PROJECT_ID']
    session_id = os.environ['SESSION_ID']
    credentials = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    bot = telegram.Bot(token=bot_token)
    bot.logger.addHandler(TelegramLogsHandler(bot, os.environ['TELEGRAM_CHAT_ID']))
    bot.logger.warning('Телеграм бот запущен')
    updater = Updater(token=bot_token, use_context=True)
    send_answer_with_credentials = lambda update, context: send_answer(update,
                                                                       context,
                                                                       credentials,
                                                                       project_id,
                                                                       session_id)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, send_answer_with_credentials))

    try:
        updater.start_polling()
        updater.idle()
    except requests.exceptions.HTTPError as err:
        bot.logger.warning(f'Телеграм бот упал с ошибкой {err}')
   

if __name__ == '__main__':
    main()
