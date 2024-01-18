# clu_sentiment.py

from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

"""clu_endpoint = "https://emotiguard-clu.cognitiveservices.azure.com/"
clu_key = "5881bff47ca340ebabc85378c1730ec8"
project_name = "EmotiGuardluis"
deployment_name = "EmotiGuard_CLU"""


def get_clu_sentiment(user_input, clu_endpoint, clu_key, project_name, deployment_name):
    # Analyze conversation using CLU
    client = ConversationAnalysisClient(clu_endpoint, AzureKeyCredential(clu_key))
    with client:
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": user_input,
                    },
                    "isLoggingEnabled": False,
                },
                "parameters": {
                    "projectName": project_name,
                    "deploymentName": deployment_name,
                    "verbose": True,
                },
            }
        )

    # Extract the top intent (sentiment category)
    top_intent = result.get("result", {}).get("prediction", {}).get("topIntent", "N/A")
    return top_intent
