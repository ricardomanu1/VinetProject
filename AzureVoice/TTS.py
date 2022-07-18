import os
import time
import csv
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from XML import XML
from translator import translator

XML = XML()
Translator = translator()

speech_key, service_region = "4ec49a617e534c16b0dcca93b0bd11cf", "westeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

speech_config.speech_synthesis_language = "en-US" 
speech_config.speech_synthesis_voice_name ="en-US-JennyMultilingualNeural"

audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=audio_config)

output_txt = open("visemes.txt","w+")
output_csv = open('visemes.csv','w+')
writer = csv.writer(output_csv, delimiter =';')
writer.writerow(['audio_offset','viseme_id'])
speech_synthesizer.viseme_received.connect(lambda evt: print(
            "Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id)))
speech_synthesizer.viseme_received.connect(lambda evt: output_txt.write(str((
            "Viseme event received: audio offset: {}ms, viseme id: {}.\n".format(evt.audio_offset / 10000, evt.viseme_id)))))
speech_synthesizer.viseme_received.connect(lambda evt: writer.writerow([evt.audio_offset / 10000, evt.viseme_id]))

while True:
    # Receives a text from console input.    
    time.sleep(1)
    if os.path.exists('..\\VinetBot\\VinetProject\\response\\respuesta.xml'):               
        output_txt = open("visemes.txt","w+")    
        output_csv = open('visemes.csv','w+')
        writer = csv.writer(output_csv, delimiter =';')
        writer.writerow(['audio_offset','viseme_id'])
        #speech_synthesizer.synthesis_started.connect(lambda evt: print("Synthesis started: {}".format(evt)))
        #speech_synthesizer.synthesizing.connect(
        #    lambda evt: print("Synthesis ongoing, audio chunk received: {}".format(evt)))
        #speech_synthesizer.synthesis_word_boundary.connect(lambda evt: print(
        #    "Word boundary event received: {}, audio offset in ms: {}ms.".format(evt, evt.audio_offset / 10000))) 
        #speech_synthesizer.synthesis_completed.connect(lambda evt: print("Synthesis completed: {}".format(evt)))

        #ssml_string = open("..\\VinetBot\\VinetProject\\response\\respuesta.xml", "r", encoding="utf-8").read()
               
        with open('..\\VinetBot\\VinetProject\\speech.txt') as f:
            contents = f.read()
            print(contents)
        tag = 'Neutral'
        #lang = 'en-US'        
        lang = 'es-ES'        
        #voice_name = 'en-US-JennyMultilingualNeural'
        voice_name = 'es-ES-ElviraNeural'
        text_trans = Translator.translator(contents,'es',lang[0:2])

        # Construccion del SSML        
        XML.name(text_trans,tag,lang,voice_name) 

        ssml_string = open("respuesta.xml", "r", encoding="utf-8").read()  

        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        stream = AudioDataStream(result)
        stream.save_to_wav_file("respuesta.wav")           

        # Comprobacion del resultado
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Síntesis de voz para el XML [{}]".format(ssml_string))
            audio_data = result.audio_data
            print("{} bytes of audio data received.".format(len(audio_data)))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))  
        output_txt.close()
        output_csv.close()
        os.remove('..\\VinetBot\\VinetProject\\response\\respuesta.xml')
        time.sleep(2)
