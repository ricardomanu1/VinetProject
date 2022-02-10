# VinetProject
conda create -n RasaVinet python==3.8
conda activate RasaVinet 
conda install ujson
conda install tensorflow
pip install rasa==2.8

--- componente para fragmentar texto en español ---
pip3 install rasa[spacy]
python -m spacy download es_core_news_md

