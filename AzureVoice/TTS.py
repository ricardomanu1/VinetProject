import azure.cognitiveservices.speech as speechsdk
import os
import time
from azure.cognitiveservices.speech import AudioDataStream
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from interaction_manager import interaction_manager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

output = open("visemes.txt","w+")
speech_synthesizer.viseme_received.connect(lambda evt: print(
            "Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id)))
speech_synthesizer.viseme_received.connect(lambda evt: output.write(str((
            "Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id)))))
while True:
    # Receives a text from console input.    
    time.sleep(1)
    if os.path.exists('..\\VinetBot\\VinetProject\\response\\respuesta.xml'):               
        output = open("visemes.txt","w+")       
        #speech_synthesizer.synthesis_started.connect(lambda evt: print("Synthesis started: {}".format(evt)))
        #speech_synthesizer.synthesizing.connect(
        #    lambda evt: print("Synthesis ongoing, audio chunk received: {}".format(evt)))
        #speech_synthesizer.synthesis_word_boundary.connect(lambda evt: print(
        #    "Word boundary event received: {}, audio offset in ms: {}ms.".format(evt, evt.audio_offset / 10000))) 
        #speech_synthesizer.synthesis_completed.connect(lambda evt: print("Synthesis completed: {}".format(evt)))

        ssml_string = open("..\\VinetBot\\VinetProject\\response\\respuesta.xml", "r", encoding="utf-8").read()
       
        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        stream = AudioDataStream(result)
        stream.save_to_wav_file("respuesta.wav")     
        

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(ssml_string))
            audio_data = result.audio_data
            print("{} bytes of audio data received.".format(len(audio_data)))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))  
        output.close()
        os.remove('..\\VinetBot\\VinetProject\\response\\respuesta.xml')
        time.sleep(2)
