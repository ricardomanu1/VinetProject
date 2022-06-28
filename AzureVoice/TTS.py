import azure.cognitiveservices.speech as speechsdk
import os
import time
from azure.cognitiveservices.speech import AudioDataStream
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from interaction_manager import interaction_manager
Interaction = interaction_manager()

speech_key, service_region = "4ec49a617e534c16b0dcca93b0bd11cf", "westeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Note: if only language is set, the default voice of that language is chosen.
speech_config.speech_synthesis_language = "en-US" # For example, "de-DE"
# The voice setting will overwrite the language setting.
# The voice setting will not overwrite the voice element in input SSML.
speech_config.speech_synthesis_voice_name ="en-US-JennyMultilingualNeural"

audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=audio_config)
#speech_synthesizer_visem = speechsdk.SpeechSynthesisVisemeEventArgs(AudioOffset)


while(1):
    # Receives a text from console input.    
    time.sleep(1)
    if os.path.exists('..\\VinetBot\\VinetProject\\respuesta.xml'):
    #if os.path.exists('..\\VinetBot\\VinetProject\\speech.txt'):
        #fo = open('..\\VinetBot\\VinetProject\\speech.txt')        
        #with fo  as f:
        #    lines = f.readlines()
        #    print(lines)
        #    text = str(lines)
        
        #text = input()
        #r = Interaction.tts()    

        # Synthesizes the received text to speech.
        # The synthesized speech is expected to be heard on the speaker with this line executed.
        #result = speech_synthesizer.speak_text_async(text).get()
        ssml_string = open("..\\VinetBot\\VinetProject\\respuesta.xml", "r", encoding="utf-8").read()
        
        # Subscribes to viseme received event        
        speech_synthesizer.synthesis_started.connect(lambda evt: print("Synthesis started: {}".format(evt)))
        #speech_synthesizer.synthesizing.connect(
        #    lambda evt: print("Synthesis ongoing, audio chunk received: {}".format(evt)))
        speech_synthesizer.synthesis_word_boundary.connect(lambda evt: print(
            "Word boundary event received: {}, audio offset in ms: {}ms.".format(evt, evt.audio_offset / 10000)))
        
        #speech_synthesizer.viseme_received.connect(lambda evt: print(
        #    "Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id)))      
        speech_synthesizer.viseme_received.connect(lambda evt: print(
            "Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id)))

        speech_synthesizer.synthesis_completed.connect(lambda evt: print("Synthesis completed: {}".format(evt)))
       
        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        stream = AudioDataStream(result)
        stream.save_to_wav_file("respuesta.wav")             

        # Checks result.
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for text [{}]".format(ssml_string))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
            print("Did you update the subscription info?")
        #fo.close()        
        time.sleep(2)
        # </code>
        #os.remove('..\\VinetBot\\VinetProject\\speech.txt')
        os.remove('..\\VinetBot\\VinetProject\\respuesta.xml')
