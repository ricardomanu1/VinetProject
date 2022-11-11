import random, keyboard #, sys
import azure.cognitiveservices.speech as speechsdk
from interaction_manager import interaction_manager
from translator import translator
from sentiment import sentiment

with open('..\\..\\AzureKeys.txt') as f:
    lines = [line.rstrip() for line in f]
    print(lines)

# Voice Service API key
speech_key = str(lines[0]) #sys.argv[1]
# Translator Service API key
translator_key = str(lines[1]) #sys.argv[2]
# Language Service Api key
sentiment_key = str(lines[2]) #sys.argv[3]
# Tanslator Service Init
Translator = translator(translator_key)
# Audio and image interaction manager
Interaction = interaction_manager()
# Language
Sentiment = sentiment(sentiment_key)

# Sentiments list inputs
Emotions = ['isHappy','isSad','isFear','isAnger','isSurprise','isBored','isAnxious','isLonely','isTired']

# Voice service configuration
service_region = "westeurope"
# Detectable languages
auto_detect_source_language_config = \
    speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["es-ES","en-US","fr-FR","ja-JP"])
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Set multiple properties by id
speech_config.set_property(
    property_id=speechsdk.PropertyId.SpeechServiceConnection_SingleLanguageIdPriority, value='Latency')

# Audio input configuration
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Language recognizer
recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, 
    auto_detect_source_language_config=auto_detect_source_language_config, 
    audio_config=audio_config)

# Keyword Detection
model = speechsdk.KeywordRecognitionModel("Keywords/2faffcbd-2030-4c7e-86f3-69bceff47a28.table")
keyword = "Sonia"
keyword_recognizer = speechsdk.KeywordRecognizer()

while True:
    result_future = keyword_recognizer.recognize_once_async(model)
    print('Esperando al comando de voz: "{}"'.format(keyword))
    
    #if keyboard.is_pressed('q'):
    #    keyword_recognizer.stop_recognition_async() 
        #break

    # Waiting for keyword
    try:
        result = result_future.get()  
    except:
        break

    # Keyword detected
    try:                
        if result.reason == speechsdk.ResultReason.RecognizedKeyword: #keyboard.is_pressed('q'):
            print("Di algo...")
            # Waiting for sentence (maximum of 15 seconds of audio)
            result = recognizer.recognize_once()
            # System to detect emotion from audio
            emotion = random.choice(Emotions)            
            # Language recognition in first iteration
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                # Language detected
                detected_src_lang = result.properties[
                    speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult]
                print("Idioma detectado: {}".format(detected_src_lang))
                print("Entrada: {} <{}>".format(result.text,emotion))
                # Translation to Spanish
                text_trans = Translator.translator(result.text,detected_src_lang[0:2],'es')
                # System to detect polarity from audio (positive,negative,neutral)
                sentiment_analysis = Sentiment.sentiment(result.text,detected_src_lang[0:2])
                # Send the spanish translation to Rasa
                #Interaction.say(text_trans,detected_src_lang,emotion)   
                Interaction.say(text_trans,detected_src_lang,emotion,sentiment_analysis)   
                # New translation configurations
                translation_config = speechsdk.translation.SpeechTranslationConfig(
                    subscription=speech_key, region=service_region,
                    speech_recognition_language=str(detected_src_lang),
                    target_languages=('es', 'eu', 'fr', 'ja', 'en'))
                recognizer = speechsdk.translation.TranslationRecognizer(
                    translation_config=translation_config, audio_config=audio_config)
            # Direct translation after the second iteration
            elif result.reason == speechsdk.ResultReason.TranslatedSpeech:
                print("""Entrada: {}\n Traducción Español: {}\n Traducción Euskera: {}\n Traducción Inglés: {}\n Traducción Francés: {}\n Traducción Japanés: {}""".format(
                        result.text, result.translations['es'], result.translations['eu'], result.translations['en'], result.translations['fr'], result.translations['ja'],))
                sentiment_analysis = Sentiment.sentiment(result.text,detected_src_lang[0:2])
                # Send the spanish translation to Rasa
                #Interaction.say(result.translations['es'],detected_src_lang,emotion)
                Interaction.say(result.translations['es'],detected_src_lang,emotion,sentiment_analysis)
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                print("Translation canceled: {}".format(result.cancellation_details.reason))
                if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(result.cancellation_details.error_details))
    except:
        break