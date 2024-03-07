import os
import requests
import telegram
import random
import vk_api as vk

from time import sleep
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from df_API import detect_intent_texts
from tg_logger import TelegramLogsHandler


def main():
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    bot = telegram.Bot(token=bot_token)
    bot.logger.addHandler(TelegramLogsHandler(bot, os.environ['TELEGRAM_CHAT_ID']))
    bot.logger.warning('Вк бот запущен')
    VK_API_TOKEN = os.environ['VK_API_TOKEN']
    vk_session = vk.VkApi(token=VK_API_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                has_answer, bot_message = detect_intent_texts([event.text])
                if has_answer:
                    vk_api.messages.send(
                        user_id=event.user_id,
                        message=bot_message,
                        random_id=random.randint(1, 1000)
                    )
    except requests.exceptions.ReadTimeout:
        sleep(5)
        
    except Exception as err:
        bot.logger.warning(f'Вк бот упал с ошибкой {err}')


if __name__ == "__main__":
    main()
