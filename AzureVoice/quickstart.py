import azure.cognitiveservices.speech as speechsdk
from interaction_manager import interaction_manager
Interaction = interaction_manager()

speech_key, service_region = "595638ac99d0464a9227b07e48e08875", "westeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,language="es-ES")

print("Di algo...")

result = speech_recognizer.recognize_once()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Has dicho: {}".format(result.text))
    Interaction.say(result.text)
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No se ha reconocido una entrada: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Reconocimiento cancelado: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Detalles de error: {}".format(cancellation_details.error_details))


