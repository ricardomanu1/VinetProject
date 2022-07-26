import os
import time
import csv
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream
from azure.cognitiveservices.speech.audio import AudioOutputConfig
#from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler
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
output_csv = open('visemes.csv','w+',newline='')
writer = csv.writer(output_csv, delimiter =';')
#writer.writerow(['audio_offset','viseme_id'])
speech_synthesizer.viseme_received.connect(lambda evt: print(
            "Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id)))
speech_synthesizer.viseme_received.connect(lambda evt: output_txt.write(str((
            "Viseme event received: audio offset: {}ms, viseme id: {}.\n".format(evt.audio_offset / 10000, evt.viseme_id)))))
speech_synthesizer.viseme_received.connect(lambda evt: writer.writerow([evt.audio_offset / 10000, evt.viseme_id]))

# indica que se ha iniciado la síntesis de voz
speech_synthesizer.synthesis_started.connect(lambda evt: print("Synthesis started: {}".format(evt)))
# 
speech_synthesizer.bookmark_reached.connect(lambda evt: print(
        "Bookmark reached: {}, audio offset: {}ms, bookmark text: {}.".format(evt, evt.audio_offset / 10000, evt.text)))
# cada vez que el sdk recibe un fragmento de audio
speech_synthesizer.synthesizing.connect(
            lambda evt: print("Synthesis ongoing, audio chunk received: {}".format(evt)))
# limite de palabra
speech_synthesizer.synthesis_word_boundary.connect(lambda evt: print(
            "Word boundary event received: {}, audio offset in ms: {}ms.".format(evt, evt.audio_offset / 10000))) 
# indica que la síntesis de voz se ha completado
speech_synthesizer.synthesis_completed.connect(lambda evt: print("Synthesis completed: {}".format(evt)))

while True:
    # Receives a text from console input.    
    time.sleep(1)
    #if os.path.exists('..\\VinetBot\\VinetProject\\respuesta.xml'):               
    if os.path.exists('..\\speech.txt'):               
        output_txt = open("visemes.txt","w+")    
        output_csv = open('visemes.csv','w+',newline='')
        writer = csv.writer(output_csv, delimiter =';')
        writer.writerow(['audio_offset','viseme_id'])

        #ssml_string = open("..\\VinetBot\\VinetProject\\respuesta.xml", "r", encoding="utf-8").read()
               
        with open('..\\speech.txt') as f:
            #contents = f.read()
            lines = [line.rstrip() for line in f]
            print(lines)
        contents = str(lines[0])
        tag = str(lines[1])
        lang = str(lines[2])
        tag = 'Cheerful'
        #tag = 'Sad'
        if lang == 'es-ES' or lang == 'eu-ES':
            voice_name = 'es-ES-ElviraNeural' ##español ##euskera
        elif lang == 'en-US':
            voice_name = 'en-US-JennyNeural' ##inglés con emociones
        elif lang == 'ja-JP':
            voice_name = 'ja-JP-NanamiNeural' ##japonés
        elif lang == 'fr-FR':
            voice_name = 'fr-FR-DeniseNeural'
        #voice_name = 'en-US-JennyMultilingualNeural'   ##inglés multilingüe

        text_trans = Translator.translator(contents,'es',lang[0:2])

        # Construccion del SSML        
        XML.name(text_trans,tag,lang,voice_name) 
        #XML.name2(text_trans,tag,lang,voice_name) 

        ssml_string = open("respuesta.xml", "r", encoding="utf-8").read()  

        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        stream = AudioDataStream(result)
        stream.save_to_wav_file("respuesta.wav")           

        # Comprobacion del resultado
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Síntesis de voz para el XML [{}]".format(ssml_string))
            audio_data = result.audio_data
            print("{} bytes of audio data received.".format(len(audio_data)))
            print(text_trans)
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))  
        output_txt.close()
        output_csv.close()
        #os.remove('..\\VinetBot\\VinetProject\\respuesta.xml')
        os.remove('..\\speech.txt')
        time.sleep(2)
