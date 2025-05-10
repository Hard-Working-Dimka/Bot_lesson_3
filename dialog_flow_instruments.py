from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def create_api_key(project_id: str, suffix: str) -> Key:
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()

    print(f"Successfully created an API key: {response.name}")
    return response


# if __name__ == "__main__":
    # create_api_key(per, "firs")

# per="tgbot-459318"
# fir = "5316948794"
# # create_api_key(per, "firs")
#
# detect_intent_texts(per, fir, ["hello"], "en-US")
