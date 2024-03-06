
import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from df_API import detect_intent_texts


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Здравствуйте")


def send_answer(update, context):
    has_answer, bot_message = detect_intent_texts([update.message.text])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=bot_message)


def main():
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, send_answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
