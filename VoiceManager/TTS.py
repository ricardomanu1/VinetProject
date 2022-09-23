import os
import time
import csv
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from XML import XML
from translator import translator

XML = XML()
Translator = translator()

speech_key, service_region = "4ec49a617e534c16b0dcca93b0bd11cf", "westeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

speech_config.speech_synthesis_language = "en-US" 
speech_config.speech_synthesis_voice_name ="en-US-JennyMultilingualNeural"

#audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
#audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False, filename = "respuesta.wav")
audio_config = speechsdk.AudioConfig(use_default_microphone=False, filename = "respuesta.wav")
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=audio_config)



#output_txt = open("visemes.txt","w+")
output_csv = open('visemes.csv','w+',newline='')
writer = csv.writer(output_csv, delimiter =';')
writer.writerow(['audio_offset','viseme_id'])

if (os.path.exists('../../../../Desktop/final/ExternalCSV')):
    output_Unreal = open('../../../../Desktop/final/ExternalCSV/visemes.csv','w+',newline='')
    writerU = csv.writer(output_Unreal, delimiter =';')
    writerU.writerow(['audio_offset','viseme_id'])
#speech_synthesizer.viseme_received.connect(lambda evt: print(
#            "Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id)))
#speech_synthesizer.viseme_received.connect(lambda evt: output_txt.write(str((
#            "Viseme event received: audio offset: {}ms, viseme id: {}.\n".format(evt.audio_offset / 10000, evt.viseme_id)))))
#speech_synthesizer.viseme_received.connect(lambda evt: writer.writerow([evt.audio_offset / 10000, evt.viseme_id]))

# indica que se ha iniciado la síntesis de voz
speech_synthesizer.synthesis_started.connect(lambda evt: print("Synthesis started: {}".format(evt)))
# 
#speech_synthesizer.bookmark_reached.connect(lambda evt: print(
#        "Bookmark reached: {}, audio offset: {}ms, bookmark text: {}.".format(evt, evt.audio_offset / 10000, evt.text)))
# cada vez que el sdk recibe un fragmento de audio
#speech_synthesizer.synthesizing.connect(
#            lambda evt: print("Synthesis ongoing, audio chunk received: {}".format(evt)))

# limite de palabra
# se genera al principio de cada palabra hablada nueva. Proporciona un desfase de tiempo dentro de la secuencia hablada y un desplazamiento de texto
# si desea resaltar palabras a medida que se pronuncian, debe saber qué resaltar, cuándo hacerlo y durante cuánto tiempo se debe resaltar.
speech_synthesizer.synthesis_word_boundary.connect(lambda evt: print(
            "Word boundary event received: {}, audio offset in ms: {}ms.".format(evt, evt.audio_offset / 10000))) 

def viseme_cb(evt):
    print("Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id))
    #output_txt.write(str(("Viseme event received: audio offset: {}ms, viseme id: {}.\n".format(evt.audio_offset / 10000, evt.viseme_id))))
    writer.writerow([evt.audio_offset / 10000, evt.viseme_id])
    if (os.path.exists('../../../../Desktop/final/ExternalCSV')):
        writerU.writerow([evt.audio_offset / 10000, evt.viseme_id])


    # `Animation` is an xml string for SVG or a json string for blend shapes
    animation = evt.animation

# Subscribes to viseme received event
speech_synthesizer.viseme_received.connect(viseme_cb)

# indica que la síntesis de voz se ha completado
speech_synthesizer.synthesis_completed.connect(lambda evt: print("Synthesis completed: {}".format(evt)))

while True:  
    time.sleep(1)         
    if os.path.exists('..\\speech.txt'):               
        #output_txt = open("visemes.txt","w+")    
        #output_csv = open('visemes.csv','w+',newline='')
        #writer = csv.writer(output_csv, delimiter =';')
        #writer.writerow(['audio_offset','viseme_id'])

        with open('..\\speech.txt') as f:
            lines = [line.rstrip() for line in f]
            print(lines)
        contents = str(lines[0])
        tag = str(lines[1])
        lang = str(lines[2])
        
        text_trans = Translator.translator(contents,'es',lang[0:2])
        
        if lang == 'es-ES' or lang == 'eu-ES': ##español ##euskera
            XML.esXML(text_trans,tag,lang) 
        elif lang == 'en-US': ##inglés con emociones
            XML.enSSML(text_trans,tag,lang) 
        elif lang == 'ja-JP': ##japonés
            XML.jpSSML(text_trans,tag,lang) 
        elif lang == 'fr-FR': ##francés
            XML.frSSML(text_trans,tag,lang)         

        ssml_string = open("respuesta.xml", "r", encoding="utf-8").read()  

        result = speech_synthesizer.speak_ssml_async(ssml_string).get() ## se genera el audio

        stream = AudioDataStream(result) # pasar una secuencia de memoria de audio y escribirla en un archivo

        stream.save_to_wav_file("respuesta1.wav")    
        if (os.path.exists('../../../../Desktop/final/ExternalAutoImport')):
            stream.save_to_wav_file("../../../../Desktop/final/ExternalAutoImport/respuesta.wav")             

        # Comprobacion del resultado
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Síntesis de voz para el XML [{}]".format(ssml_string))
            audio_data = result.audio_data
            print("{} bytes of audio data received.".format(len(audio_data)))
            print("VINETbot: {} ({})".format(text_trans,tag))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))  
        #output_txt.close()
        output_csv.close()
        os.remove('..\\speech.txt')
        time.sleep(2)
