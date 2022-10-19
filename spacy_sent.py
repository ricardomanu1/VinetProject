# the following installations are required
# python -m textblob.download_corpora
# python -m spacy download en_core_web_sm

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
print(spacy.__version__)
print(nlp.components)
print(nlp.pipeline)
#print(nlp.components_names)
print(nlp.pipe_names)
nlp.add_pipe('spacytextblob')
text = 'I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy.'
#text = "John love eating apples wheb he works at Apple"
doc = nlp(text)
print(text)
print("Polaridad: {}".format(doc._.blob.polarity))
print("Subjetividad: {}".format(doc._.blob.subjectivity))
print("Lista de polaridad y subjetividad por tokens: \n{}".format(doc._.blob.sentiment_assessments.assessments))
print("Lista de n-gramas: \n{}".format(doc._.blob.ngrams()))
print("Lista de tags por tokens: \n{}".format(doc._.blob.pos_tags))
for token in doc:
    print("token: ",token.text,token.pos,token.tag)