import requests
import json

class interaction_manager(object):

    def say(self,text,lang,sentiment):
        r = requests.post('http://127.0.0.1:5005/webhooks/myio/webhook', json={
        "sender": "Vinet_user",
        "message": "{}".format(text),
        "metadata": {"event":"say","sentiment":"{}".format(sentiment),"language":"{}".format(lang)} 
        })

    def know(self,text,var,value):
        if var == 'people':
            r = requests.post('http://127.0.0.1:5005/webhooks/myio/webhook', json={
            "sender": "Vinet_user",
            "message": "{}".format(text),
            "metadata": {"event":"know","people":value} 
            })
        elif var == 'chapter':
            r = requests.post('http://127.0.0.1:5005/webhooks/myio/webhook', json={
            "sender": "Vinet_user",
            "message": "{}".format(text),
            "metadata": {"event":"know","chapter":value} 
            })
        elif var == 'emotion':
            r = requests.post('http://127.0.0.1:5005/webhooks/myio/webhook', json={
            "sender": "Vinet_user",
            "message": "{}".format(text),
            "metadata": {"event":"know","emotion":value} 
            })

    def tts(self):
        r = requests.get('http://127.0.0.1:5005/webhooks/myio')
        print(r.json())
        return r.json()
    def stt(self,text):
        r = requests.post('http://localhost:5055/webhooks', json={
        "sender": "Vinet_user",
        "message": "{}".format(text),
        "metadata": {"event":"know"} 
        })




