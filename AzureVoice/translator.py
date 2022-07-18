import os, requests, uuid, json

class translator(object):
    def __init__(self):
        self.endpoint_var_name = 'https://api.cognitive.microsofttranslator.com/'
        self.path = '/translate?'        
        self.headers = {
            'Ocp-Apim-Subscription-Key': 'f0270761bb7f413286eb5e15428b46ee',
            'Ocp-Apim-Subscription-Region': 'westeurope',
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

    def translator(self, text, f, t):
        body = [{
            'text' : text
        }]
        params = {
            'api-version': '3.0',
            'from': f,
            'to': t
        }
        constructed_url = self.endpoint_var_name + self.path
        request = requests.post(constructed_url, params=params, headers=self.headers, json=body)
        response = request.json()
        #print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
        return response[0]['translations'][0]['text']