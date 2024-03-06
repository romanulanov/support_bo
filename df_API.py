import json
import os
import requests

from dotenv import load_dotenv

from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow
from google.oauth2 import service_account


LANGUAGE_CODE = "ru"


def create_intent(project_id,
                  display_name,
                  training_phrases_parts,
                  message_texts):
    credentials = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
    intents_client = dialogflow.IntentsClient(credentials=credentials)
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
            )

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print('Intent created: {}'.format(response))


def detect_intent_texts(texts):
    credentials = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    client = dialogflow.SessionsClient(credentials=credentials)
    session = client.session_path(os.environ['PROJECT_ID'],
                                  os.environ['SESSION_ID']
                                  )

    for text in texts:
        text_input = dialogflow.TextInput(text=text,
                                          language_code=LANGUAGE_CODE)
        query_input = dialogflow.QueryInput(text=text_input)

        try:
            response = client.detect_intent(
                request={"session": session, "query_input": query_input}
            )
        except InvalidArgument:
            raise

        if response.query_result.intent.is_fallback:
            return None, response.query_result.fulfillment_text
        else:
            return True, response.query_result.fulfillment_text


def main():
    load_dotenv()
    project_id = os.environ['PROJECT_ID']
    response = requests.get("https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json")
    topics = json.loads(response.text)
    for topic, phrase in topics.items():
        create_intent(project_id,
                      topic,
                      phrase['questions'],
                      [phrase['answer']])


if __name__ == "__main__":
    main()
