# VinetProject
## Instalación
### conda create -n RasaVinet python==3.8
### conda activate RasaVinet 
### conda install ujson
### conda install tensorflow
### pip install --upgrade rasa==2.8.23

## Componente para fragmentar texto en español
### pip3 install rasa[spacy]
### python -m spacy download es_core_news_md

## Rasa x
### pip install --upgrade --use-deprecated=legacy-resolver --user rasa-x --extra-index-url https://pypi.rasa.com/simple

## Ejecución
### rasa run --enable-api
### rasa run actions

