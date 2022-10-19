import time 
import azure.cognitiveservices.speech as speechsdk

speech_key, service_region = "abb6818d47cf4ec7ba7666eb35827855", "westeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

def from_file():
    audio_input = speechsdk.AudioConfig(filename="respuesta.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,         
        audio_config=audio_input,
        language="es-ES")
    speech_recognizer.start_continious_recognition()
    done = False
    def on_recognized(evt):
        assert(evt.result.reason == speechsdk.ResultReason.RecognizedSpeech),"a portion was not recognized"
        print("RECOGNIZED: {}".format(evt))

    def stop_cb(evt):
        print("CLOSING on {}".format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = false

    speech_recognizer.recognized.connect(on_recognized)
    speech_recognizer.session_stopped.connect(stop-cb)

    while not done:
        time.sleep(0.5)