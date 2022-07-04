import azure.cognitiveservices.speech as speechsdk
import os
import time
from azure.cognitiveservices.speech import AudioDataStream
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from interaction_manager import interaction_manager
Interaction = interaction_manager()

speech_key, service_region = "4ec49a617e534c16b0dcca93b0bd11cf", "westeurope"
"""performs speech synthesis and shows the viseme event."""
# Creates an instance of a speech config with specified subscription key and service region.
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Note: if only language is set, the default voice of that language is chosen.
speech_config.speech_synthesis_language = "en-US" # For example, "de-DE"
# The voice setting will overwrite the language setting.
# The voice setting will not overwrite the voice element in input SSML.
speech_config.speech_synthesis_voice_name ="en-US-JennyMultilingualNeural"

# Creates a speech synthesizer with a null output stream.
# This means the audio output data will not be written to any output channel.
# You can just get the audio from the result.
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=audio_config)

# Subscribes to viseme received event
# The unit of evt.audio_offset is tick (1 tick = 100 nanoseconds), divide it by 10,000 to convert to milliseconds.
speech_synthesizer.viseme_received.connect(lambda evt: print(
    "Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id)))

# Receives a text from console input and synthesizes it to result.
while True:
    print("Enter some text that you want to synthesize, Ctrl-Z to exit")
    try:
        ssml_string = open("..\\VinetBot\\VinetProject\\respuesta.xml", "r", encoding="utf-8").read()
        #text = input()
    except EOFError:
        break
    #result = speech_synthesizer.speak_text_async(text).get()
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

