import azure.cognitiveservices.speech as speechsdk
import os
import time
from interaction_manager import interaction_manager
Interaction = interaction_manager()

speech_key, service_region = "4ec49a617e534c16b0dcca93b0bd11cf", "westeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Note: if only language is set, the default voice of that language is chosen.
speech_config.speech_synthesis_language = "es-ES" # For example, "de-DE"
# The voice setting will overwrite the language setting.
# The voice setting will not overwrite the voice element in input SSML.
speech_config.speech_synthesis_voice_name ="es-ES-AlvaroNeural"

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
while(1):
    # Receives a text from console input.    
    time.sleep(1)
    if os.path.exists('..\\VinetBot\\VinetProject\\speech.txt'):
        fo = open('..\\VinetBot\\VinetProject\\speech.txt')        
        with fo  as f:
            lines = f.readlines()
            print(lines)
            text = str(lines)
        #text = input()
        #r = Interaction.tts()    

        # Synthesizes the received text to speech.
        # The synthesized speech is expected to be heard on the speaker with this line executed.
        result = speech_synthesizer.speak_text_async(text).get()

        # Checks result.
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
            print("Did you update the subscription info?")
        fo.close()
        time.sleep(2)
        # </code>
        os.remove('..\\VinetBot\\VinetProject\\speech.txt')
