import azure.cognitiveservices.speech as speechsdk
import keyboard
from interaction_manager import interaction_manager

Interaction = interaction_manager()
i = 0
speech_key, service_region = "595638ac99d0464a9227b07e48e08875", "westeurope"

auto_detect_source_language_config = \
    speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["es-ES", "en-US", "ja-JP"])

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

speech_config.set_property(
    property_id=speechsdk.PropertyId.SpeechServiceConnection_SingleLanguageIdPriority, value='Latency')

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

#source_language_recognizer = speechsdk.SourceLanguageRecognizer(
#    speech_config=speech_config,
#    auto_detect_source_language_config=auto_detect_source_language_config,
#    audio_config=audio_config)

#speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,language="es-ES")
speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        auto_detect_source_language_config=auto_detect_source_language_config, 
        audio_config=audio_config)

while True:
    try:
        if keyboard.is_pressed('q'):
            print("Di algo...")
            #result = source_language_recognizer.recognize_once()
            result = speech_recognizer.recognize_once()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("RECOGNIZED: {}".format(result))
                # Primera iter
                if i==0:
                    detected_src_lang = result.properties[
                        speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult]
                    print("Detected Language: {}".format(detected_src_lang))
                print("Has dicho: {}".format(result.text))
                Interaction.say(result.text,detected_src_lang)
                i += 1
                # Segunda iter
                if i == 1:
                    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,language=str(detected_src_lang))

            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No se ha reconocido una entrada: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Reconocimiento cancelado: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Detalles de error: {}".format(cancellation_details.error_details))
            #break  # finishing the loop
    except:
        break




