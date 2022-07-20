import keyboard
import azure.cognitiveservices.speech as speechsdk
from interaction_manager import interaction_manager
from translator import translator

Translator = translator()
Interaction = interaction_manager()

sentiment = 'isHappy' #['isHappy','isSad','isFear','isAnger','isSurprise','isBored','isAnxious','isLonely','isTired']
    
speech_key, service_region = "595638ac99d0464a9227b07e48e08875", "westeurope"

auto_detect_source_language_config = \
    speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["es-ES", "en-US", "ja-JP"])

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

speech_config.set_property(
    property_id=speechsdk.PropertyId.SpeechServiceConnection_SingleLanguageIdPriority, value='Latency')

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        auto_detect_source_language_config=auto_detect_source_language_config, 
        audio_config=audio_config)

while True:
    try:
        if keyboard.is_pressed('q'):
            print("Di algo...")
            result = recognizer.recognize_once()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                detected_src_lang = result.properties[
                        speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult]
                print("Idioma detectado: {}".format(detected_src_lang))
                print("Entrada: {}".format(result.text))
                text_trans = Translator.translator(result.text,detected_src_lang[0:2],'es')
                Interaction.say(text_trans,detected_src_lang,sentiment)                
                translation_config = speechsdk.translation.SpeechTranslationConfig(
                    subscription=speech_key, region=service_region,
                    speech_recognition_language=str(detected_src_lang),
                    target_languages=('es', 'eu', 'fr', 'ja', 'en'))
                recognizer = speechsdk.translation.TranslationRecognizer(
                    translation_config=translation_config, audio_config=audio_config)
            elif result.reason == speechsdk.ResultReason.TranslatedSpeech:
                print("""Entrada: {}
                    Traducción Español: {}
                    Traducción Euskera: {}                    
                    Traducción Inglés: {}
                    Traducción Francés: {}
                    Traducción Japanés: {}""".format(
                        result.text, 
                        result.translations['es'],
                        result.translations['eu'],
                        result.translations['en'],
                        result.translations['fr'],
                        result.translations['ja'],))
                Interaction.say(result.translations['es'],detected_src_lang,sentiment)
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                print("Translation canceled: {}".format(result.cancellation_details.reason))
                if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(result.cancellation_details.error_details))
    except:
        break




