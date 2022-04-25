# VinetProject
## Instalación
### conda create -n RasaVinet python==3.8
### conda activate RasaVinet 
### conda install ujson
### conda install tensorflow
### pip install rasa
### pip install --upgrade rasa==2.8.23

## Componente para fragmentar texto en español
### pip3 install rasa[spacy]
### python -m spacy download es_core_news_md

## Componente sentiment
### pip install nltk

## Rasa x
### pip install --upgrade --use-deprecated=legacy-resolver --user rasa-x --extra-index-url https://pypi.rasa.com/simple

## Ejecución con API
### rasa run -m models --enable-api --credentials credentials.yml --debug
### rasa run actions

http://localhost:5005/webhooks/myio/webhook

## Ejemplo de mensaje
{
    "sender": "Vinet_user",
    "message": "Hola",
    "metadata": {"event":"say","sentiment":"happy"} 
}
