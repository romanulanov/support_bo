import json
import os
from google.cloud import dialogflow
from dotenv import load_dotenv
import requests 
from google.oauth2 import service_account

load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS =  os.environ['GOOGLE_APPLICATION_CREDENTIALS']  


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_APPLICATION_CREDENTIALS,
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
    intents_client = dialogflow.IntentsClient(credentials=credentials)

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
    
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def main():
    project_id = os.environ['PROJECT_ID']
    response = requests.get("https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json")
    phrases = json.loads(response.text)
    for phrase, phrase_info in phrases.items():
        create_intent(project_id, phrase, phrase_info['questions'], [phrase_info['answer']])


if __name__=="__main__":
    main()
