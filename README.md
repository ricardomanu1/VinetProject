# VinetProject
## Instalación con Anaconda
### conda create -n RasaVinet python==3.8
### conda activate RasaVinet 
### conda install ujson
### conda install tensorflow
### pip install rasa
### pip install --upgrade rasa==2.8.23

## Instalación del componente para fragmentar texto en español
### pip3 install rasa[spacy]
### python -m spacy download es_core_news_md

## Instalación del componente sentiment
### pip install nltk

## Instalación de Rasa x
### pip install --upgrade --use-deprecated=legacy-resolver --user rasa-x --extra-index-url https://pypi.rasa.com/simple

## Activación del canal personalizado
### rasa run --enable-api

# Ejecución con API
## Consola 1
### rasa run -m models --enable-api --credentials credentials.yml --debug
## Consola 2
### rasa run actions

## Dirección de mensajes Json
http://localhost:5005/webhooks/myio/webhook

## Ejemplo de mensaje Json
{
    "sender": "Vinet_user",
    "message": "Hola",
    "metadata": {"event":"say","sentiment":"isHappy","language":"es-ES"} 
}
### Mas ejemplos en inputs.txt

# Configuraciones personalizadas (tras descargar el proyecto es necesario realizar un entrenamiento)
## Rasa Train
### rasa train --domain domains

## Voice manager
### Solo almacena algunos scripts para otra seccion que usa azure para incorporar la voz, ver al final.

## Uso con OpenSmile
### Pregunta: ¿Qué tal estas?
### El Json con el mensaje también tiene que llevar una de las siguientes emociones:
### ['isHappy','isSad','isFear','isAnger','isSurprise','isBored','isAnxious','isLonely','isTired']
El sistema actualmente esta actuando con un gestor de emociones espejo, si pregusto mientras estoy feliz (isHappy),
me contesta estando feliz (Happy), de la misma manera, si estoy triste (isSad), me responde estando triste (Sad)
## la salida textual: speech.txt

# Ejemplos:
## input:
{
    "sender": "Vinet_user",
    "message": "¿Qué tal estas?",
    "metadata": {"event":"say","sentiment":"isHappy","language":"es-ES"} 
}
## output:
	Me siento genial. (happy)
## input:
{
    "sender": "Vinet_user",
    "message": "¿Qué tal estas?",
    "metadata": {"event":"say","sentiment":"isSad","language":"es-ES"} 
}
## output:
	Muy triste. (sad)


# Ejecucion usando Azure
## Instalacion Azure 
### pip install keyboard
### pip install azure-cognitiveservices-speech

# Ejecución con Azure (dentro del fichero VoiceManager)
## Consola 3
### python STT.py
## Consola 4
### python TTS.py

## Nota: cada vez que se presione la tecla 'q' se da un tiempo para hablar. 
