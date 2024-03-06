import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv
from google.cloud import dialogflow
from google.oauth2 import service_account
from google.api_core.exceptions import InvalidArgument
load_dotenv()
VK_API_TOKEN =  os.environ['VK_API_TOKEN'] 
GOOGLE_APPLICATION_CREDENTIALS =  os.environ['GOOGLE_APPLICATION_CREDENTIALS']  
credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_APPLICATION_CREDENTIALS,
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
client = dialogflow.SessionsClient(credentials=credentials)
project_id = os.environ['PROJECT_ID']
language_code = "ru"
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


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=detect_intent_texts(project_id, event.user_id, [event.text], language_code),
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=VK_API_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
