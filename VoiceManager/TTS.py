import os, time, csv #, sys
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from XML import XML
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

# SSML Generator
XML = XML()
# Tanslator Service Init
Translator = translator(translator_key)
# Language
Sentiment = sentiment(sentiment_key)
lang = 'es-ES'

# External file used by Unreal
External_file = False
Output_file = '../../../../Desktop/MH-NEW/CSV'

# Service configuration
service_region = "westeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Standard configuration, but then it is applied with different languages
speech_config.speech_synthesis_language = "en-US" 
speech_config.speech_synthesis_voice_name ="en-US-JennyMultilingualNeural"

# Audio output configuration
    # audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
audio_config = speechsdk.AudioConfig(use_default_microphone=False, filename = "Response/response.wav")
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=audio_config)

# Visemes output file
output_csv = open('Response/visemes.csv','r+',newline='')
writer = csv.writer(output_csv, delimiter =';')
writer.writerow(['audio_offset','viseme_id','body_anim','emo_value','face_pos'])

# Visemes output file used by Unreal 
if (os.path.exists(Output_file)):
    External_file = True
    output_Unreal = open(Output_file + '/visemes.csv','r+',newline='')
    writerU = csv.writer(output_Unreal, delimiter =';')
    writerU.writerow(['audio_offset','viseme_id','body_anim','emo_value','face_pos'])

# Indicates that speech synthesis has started
    # speech_synthesizer.synthesis_started.connect(lambda evt: print("Synthesis started: {}".format(evt)))
# Indicates the limit of each word 
    # speech_synthesizer.synthesis_word_boundary.connect(lambda evt: print(
    #             "Word boundary event received: {}, audio offset in ms: {}ms.".format(evt, evt.audio_offset / 10000))) 
# Indicates that speech synthesis is complete
    # speech_synthesizer.synthesis_completed.connect(lambda evt: print("Synthesis completed: {}".format(evt)))

# Viseme event
def viseme_cb(evt):
    print("Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id))
    writer.writerow([evt.audio_offset / 10000, evt.viseme_id,body_anim,emo_value,face_pos])
    # Create a copy of the output file for Unreal
    if External_file:
        writerU.writerow([evt.audio_offset / 10000, evt.viseme_id,body_anim,emo_value,face_pos])
    # 'Animation' is an xml string for SVG or a json string for blend shapes
    animation = evt.animation

# Subscribes to viseme received event
speech_synthesizer.viseme_received.connect(viseme_cb)

while True:      
    time.sleep(1)  
    if os.path.exists('..\\speech.csv'):    
        start_time = time.time()
        with open('..\\speech.csv','r') as f:            
            csv_reader = csv.DictReader(f)
            #header = next(csv_reader)
            #if header != None:
            for row in csv_reader:
                if(str(row['action'])=="say"):
                    # Visemes output file
                    output_csv = open('Response/visemes.csv','r+',newline='')
                    writer = csv.writer(output_csv, delimiter =';')
                    writer.writerow(['audio_offset','viseme_id','body_anim','emo_value','face_pos'])
                    # Create a copy of the output file for Unreal
                    if External_file:
                        output_Unreal = open(Output_file + '/visemes.csv','r+',newline='')
                        writerU = csv.writer(output_Unreal, delimiter =';')
                        writerU.writerow(['audio_offset','viseme_id','body_anim','emo_value','face_pos'])
                    print(row)
                    # Sentence
                    contents = str(row['response'])
                    # Emotional tag
                    emotion = str(row['emotion'])
                    # Language
                    lang = str(row['language'])
                    # Animation
                    body_anim = str(row['animation'])
                    sentiment_analysis = Sentiment.sentiment(contents,lang)
                    print(sentiment_analysis)
                    # Polarity
                    emo_value = sentiment_analysis
                    # EyesTracking
                    face_pos = str(row['eyesTracking'])
                    # Emotional tag for Azure
                    emotionAzure = str(row['emotionAzure'])                
                    # XML - SSML generator               
                    if lang == 'es-ES' or lang == 'eu-ES': ## Spanish or Basque 
                        text_trans = contents
                        XML.esXML(contents,emotion,lang,sentiment_analysis) 
                    elif lang == 'en-US': ## English Emotional
                        # Sentence translation
                        text_trans = Translator.translator(contents,'es',lang[0:2])
                        XML.enSSML(text_trans,emotionAzure,lang) 
                    #elif lang == 'ja-JP': ## Japanese
                    #    XML.jpSSML(text_trans,emotionAzure,lang) 
                    #elif lang == 'fr-FR': ## French
                    #    XML.frSSML(text_trans,emotionAzure,lang)         
                    # Reading SSML file
                    ssml_string = open("Response/respuesta.xml", "r", encoding="utf-8").read()  
                    # Audio generated
                    result = speech_synthesizer.speak_ssml_async(ssml_string).get()
                    # Audio memory stream to file
                    stream = AudioDataStream(result)
                    stream.save_to_wav_file("Response/respuesta.wav")  
                    # Copy for Unreal
                    if External_file:
                        stream.save_to_wav_file(Output_file + "/respuesta.wav") 
                    # Checking the result
                    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                        duration = result.audio_duration
                        # Wav time
                        print("Audio duration: {} seconds.".format(duration.total_seconds()))
                        print("VINETbot: {} <{}>".format(text_trans,emotion))
                    elif result.reason == speechsdk.ResultReason.Canceled:
                        cancellation_details = result.cancellation_details
                        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
                        if cancellation_details.reason == speechsdk.CancellationReason.Error:
                            print("Error details: {}".format(cancellation_details.error_details))  
                    # Close visemes output file used by Unreal 
                    if External_file:
                        output_Unreal.close()
                    output_csv.close()
                    if(duration.total_seconds()>4):
                        time.sleep(duration.total_seconds())       
                    else:
                        time.sleep(4)       
                elif(str(row['action'])=="listen"):
                    archi1=open("listening.txt","w") 
                    archi1.close() 
                elif(str(row['action'])=="watch"):
                    output = open("..//..//Kinect.txt","w")
                    lines = [str(row['response'])]
                    output.write('\n'.join(lines))
                    output.close()
        os.remove('..\\speech.csv')        
        print("--- %s seconds ---" % (time.time() - start_time))
