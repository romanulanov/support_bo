import argparse
import os
import json
import textwrap
from dotenv import load_dotenv

from google.cloud import dialogflow
from google.oauth2 import service_account


LANGUAGE_CODE = "ru"


def create_intent(project_id,
                  display_name,
                  training_phrases_parts,
                  message_texts,
                  credentials):

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


def detect_intent_texts(text, credentials, project_id, session_id):
    client = dialogflow.SessionsClient(credentials=credentials)
    session = client.session_path(project_id,
                                  session_id,
                                  )

    text_input = dialogflow.TextInput(text=text,
                                      language_code=LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)

    response = client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return not (response.query_result.intent.is_fallback), response.query_result.fulfillment_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                        default='questions.json',
                        help=textwrap.dedent('''Введите путь до JSON,
                        откуда будут браться данные для обучения.
                        По умолчанию данные находятся в questions.json
                        в корне проекта.''')
                        )
    load_dotenv()
    credentials = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
    args = parser.parse_args()
    project_id = os.environ['PROJECT_ID']

    questions_path = args.path
    with open(questions_path, "r", encoding="utf-8") as file:
        topics = json.loads(file.read())
    print(topics)
    for topic, phrase in topics.items():
        create_intent(project_id,
                      topic,
                      phrase['questions'],
                      [phrase['answer']],
                      credentials)


if __name__ == "__main__":
    main()
