
import os

from dotenv import load_dotenv
from time import sleep
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from google.cloud import dialogflow
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.api_core.exceptions import InvalidArgument

import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS =  os.environ['GOOGLE_APPLICATION_CREDENTIALS']  
project_id = os.environ['PROJECT_ID']
language_code = "ru"
session_id = "138419352"
credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_APPLICATION_CREDENTIALS,
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
client = dialogflow.SessionsClient(credentials=credentials)

def detect_intent_texts(project_id, session_id, texts, language_code):
    session = client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        try:
            response = client.detect_intent(
                request={"session": session, "query_input": query_input}
            )
        except InvalidArgument:
            raise

        return response.query_result.fulfillment_text


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def echo2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=detect_intent_texts(project_id, session_id, [update.message.text], language_code))

def main():
    
    bot_token = os.environ['TG_BOT_TOKEN']
   
    updater = Updater(token=bot_token, use_context=True)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
   
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo2))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
