import os
import random
import vk_api as vk

from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from df_API import detect_intent_texts


if __name__ == "__main__":
    load_dotenv()
    VK_API_TOKEN = os.environ['VK_API_TOKEN']
    vk_session = vk.VkApi(token=VK_API_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            has_answer, bot_message = detect_intent_texts([event.text])
            if has_answer:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=bot_message,
                    random_id=random.randint(1, 1000)
                )
