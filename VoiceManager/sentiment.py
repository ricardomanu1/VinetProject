from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class sentiment(object):
    def __init__(self,key):
        key = "7484640a6b2b46bb871145fe2be337d5"
        endpoint = "https://languagevinet1.cognitiveservices.azure.com/"
        self.text_analytics_client = TextAnalyticsClient(endpoint=endpoint,credential=AzureKeyCredential(key))

    def sentiment(self,text,lang):
        documents = [ text ]

        response = self.text_analytics_client.analyze_sentiment(documents, language=lang)
        result = [doc for doc in response if not doc.is_error]

        for doc in result:
            print(f"Overall sentiment: {doc.sentiment}")
            print(
                f"Scores: positive={doc.confidence_scores.positive}; "
                f"neutral={doc.confidence_scores.neutral}; "
                f"negative={doc.confidence_scores.negative}\n"
            )
        return [doc.confidence_scores.positive,doc.confidence_scores.neutral,doc.confidence_scores.negative]