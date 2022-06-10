import requests
import json

class interaction_manager(object):

    def say(self,text):
        r = requests.post('http://127.0.0.1:5005/webhooks/myio/webhook', json={
        "sender": "Vinet_user",
        "message": "{}".format(text),
        "metadata": {"event":"say","sentiment":"isHappy"} 
        })

    def know(self):
        r = requests.post('http://127.0.0.1:5005/webhooks/myio/webhook', json={
        "sender": "Vinet_user",
        "message": "{}".format(text),
        "metadata": {"event":"know"} 
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




