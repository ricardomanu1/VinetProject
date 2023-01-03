import random, keyboard, time #, sys
import azure.cognitiveservices.speech as speechsdk
from interaction_manager import interaction_manager
from translator import translator
from sentiment import sentiment
import TTS

print(TTS.listening)

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

flag = 1
# Sentiments list inputs
Emotions = ['isHappy','isSad','isFear','isAnger','isSurprise','isBored','isAnxious','isLonely','isTired']

# Voice service configuration
service_region = "westeurope"
# Detectable languages
auto_detect_source_language_config = \
    speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["es-ES","en-US"]) ##,"fr-FR","ja-JP"])
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
##model = speechsdk.KeywordRecognitionModel("Keywords/2faffcbd-2030-4c7e-86f3-69bceff47a28.table")
##keyword = "Sonia"
##keyword_recognizer = speechsdk.KeywordRecognizer()

while True:
    ##result_future = keyword_recognizer.recognize_once_async(model)
    ##print('Esperando al comando de voz: "{}"'.format(keyword))

    # Waiting for keyword
    #try:
        #result = result_future.get()  
    #except:
        #break

    # Keyword detected
    try:                
        #if keyboard.is_pressed('q'): #result.reason == speechsdk.ResultReason.RecognizedKeyword:
        print("Di algo...")
        # Waiting for sentence (maximum of 15 seconds of audio)
        result = recognizer.recognize_once()

        start_time = time.time()

        # System to detect emotion from audio
        emotion = random.choice(Emotions)            
        # Language recognition in first iteration
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:        
                
            if flag == 1:                    
                # Language detected
                detected_src_lang = result.properties[
                    speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult]
                print("Detected language: {}".format(detected_src_lang))
                print("Input: {} <{}>".format(result.text,emotion))
                if (str(result.text) == 'Apagar sistema.'):
                    print("Apagando sistema...")
                    break
                text_trans = result.text
                if(str(detected_src_lang) != "es-ES"):    
                    # Translation to Spanish
                    text_trans = Translator.translator(result.text,detected_src_lang[0:2],'es')
                # System to detect polarity from audio (positive,negative,neutral)
                sentiment_analysis = Sentiment.sentiment(result.text,detected_src_lang[0:2])
                # Send the spanish translation to Rasa
                Interaction.say(text_trans,detected_src_lang,emotion,sentiment_analysis)   
                if(str(detected_src_lang) != "es-ES"):
                    #print("OK")
                    # New translation configurations
                    translation_config = speechsdk.translation.SpeechTranslationConfig(
                        subscription=speech_key, region=service_region,
                        speech_recognition_language=str(detected_src_lang),
                        target_languages=('es','en'))##, 'fr', 'ja', 'eu'))
                    recognizer = speechsdk.translation.TranslationRecognizer(
                        translation_config=translation_config, audio_config=audio_config)              
                else:
                    #print("entra")
                    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
                    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=detected_src_lang, audio_config=audio_config)
            elif flag == 2:                       
                print("Input: {} <{}>".format(result.text,emotion))
                if (str(result.text) == 'Apagar sistema.'):
                    print("Apagando sistema...")
                    break
                # System to detect polarity from audio (positive,negative,neutral)
                sentiment_analysis = Sentiment.sentiment(result.text,detected_src_lang[0:2])
                # Send the spanish translation to Rasa
                Interaction.say(result.text,detected_src_lang,emotion,sentiment_analysis)
            flag = 2
        # Direct translation after the second iteration
        elif result.reason == speechsdk.ResultReason.TranslatedSpeech:            
            print("""Input: {}\n Translation to Spanish: {}""".format(
                    result.text, result.translations['es']))##, result.translations['en'], result.translations['eu'], result.translations['fr'], result.translations['ja']))
            sentiment_analysis = Sentiment.sentiment(result.text,detected_src_lang[0:2])
            if (str(result.translations['es']) == 'Apagar sistema.'):
                print("Apagando sistema...")
                break
            # Send the spanish translation to Rasa
            Interaction.say(result.translations['es'],detected_src_lang,emotion,sentiment_analysis)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
            # utter_please_rephrase
            Interaction.know("nlu_fallback")
        elif result.reason == speechsdk.ResultReason.Canceled:
            print("Translation canceled: {}".format(result.cancellation_details.reason))
            if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(result.cancellation_details.error_details))
        print("--- %s seconds ---" % (time.time() - start_time))
    except:
        continue