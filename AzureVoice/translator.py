import os, requests, uuid, json

class translator(object):
    def __init__(self):
        self.endpoint_var_name = 'https://api.cognitive.microsofttranslator.com/'
        # If you encounter any issues with the base_url or path, make sure
        # that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
        self.path = '/translate?'
        #self.params = '&from=en&to=de&to=it'
        
        self.headers = {
            'Ocp-Apim-Subscription-Key': 'f0270761bb7f413286eb5e15428b46ee',
            'Ocp-Apim-Subscription-Region': 'westeurope',
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

    def translator(self, text, f, t):
        # You can pass more than one object in body.
        body = [{
            'text' : text
        }]
        params = {
            'api-version': '3.0',
            'from': f,
            'to': t
        }
        constructed_url = self.endpoint_var_name + self.path
        #print(constructed_url)
        request = requests.post(constructed_url, params=params, headers=self.headers, json=body)
        response = request.json()

        print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
        return response[0]['translations'][0]['text']