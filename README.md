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

## Instalación del componente sentiment de spyce
### pip install nltk

## Instalación de Rasa x
### pip install --upgrade --use-deprecated=legacy-resolver --user rasa-x --extra-index-url https://pypi.rasa.com/simple

# Ejecución con API
## Consola 1
### rasa run -m models --enable-api --credentials credentials.yml --debug
## Consola 2
### rasa run actions

http://localhost:5005/webhooks/myio/webhook

## Ejemplo de mensaje json
{
    "sender": "Vinet_user",
    "message": "Hola",
    "metadata": {"event":"say","sentiment":"isHappy","language":"es-ES"} 
}
### Mas ejemplos en inputs.txt

# Configuraciones personalizadas
## Rasa Train
### rasa train --domain domains

## Voice manager
### Solo almacena algunos scripts para otra seccion que usa azure para incorporar la voz