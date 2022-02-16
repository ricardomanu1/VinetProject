import os
import json
import typing
import importlib
import datetime as dt
import xml.etree.cElementTree as ET
from emotions_manager import emotions_manager
from belief_manager import belief_manager
from desires_manager import desires_manager
from intents_manager import intents_manager 

from os import listdir
from typing import Any, Text, Dict, List

from rasa_sdk import events
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, BotUttered, UserUttered, EventType

from rasa.shared.nlu.training_data.loading import load_data

if typing.TYPE_CHECKING:
    from rasa_sdk.trackers import DialogueStateTracker
    from rasa_sdk.dispatcher import Dispatcher
    from rasa_sdk.domain import Domain

# Variables globales
#user_event = []
user_intent = ''
count = 0
#resp = ''
daytime = ''
Emotions = emotions_manager()
Beliefs = belief_manager()
Desires = desires_manager()        
Intents = intents_manager()
smg = []

def __init__(self):

    self.agent_id = 'actions'
    self.emotions_manager = emotions_manager()
    self.belief_manager = belief_manager()        
    self.desires_manager = desires_manager()
    self.intents_manager = intents_manager()

def contador():
    global count
    count = count + 1
    return []

def get_latest_event(events):
    latest_actions = []
    for e in events:
        if e['event'] == 'bot':
            latest_actions.append(e)
    #return latest_actions[-2:][0]['name']
    return latest_actions#[-1:][0]['text']

## Estructura BOT
class ChatBot(Action):

    def name(self) -> Text:
        return "chatbot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        #global user_event
        global user_intent

        ## Valores de entrada, si es un texto
        intent = tracker.latest_message['intent']
        text = tracker.latest_message['text']
        entities = tracker.latest_message['entities']            
        slot_name = tracker.get_slot('name')       

        user_intent = intent['name']
        tracker.slots['daytime'] = 'evening'

        Bi = intent['name']  
                
        print(tracker.latest_message['metadata'])
    #
        #events = tracker.current_state()['events']
        #user_events = []
        #for e in events:
        #    if e['event'] == 'user':
        #        user_events.append(e)
        #print(user_events[-1]['metadata'])
    #

        with open('EmotionIntent.txt', 'r') as f:
            global Be
            contenido = f.read()
            Be = contenido  

        ## Evento en el caso de que sea un texto
        user_event = ['say',Bi,Be,text,slot_name,entities] 
        print('-----EVENT-----')
        print(user_event)

        ## comprobacion del diccionario de sinonimos de entidades
        synonyms_dict = Dictionary.get_synonym_mapper()
        for value, synonyms in synonyms_dict.items():
            ## print("Value:", value)
            ## print("Synonyms:", str(synonyms))
            Ricardo_synonyms = synonyms      
        
        EBDI.run(self, dispatcher, tracker, domain, user_event)

        return []

## Estructura EBDI
class EBDI(Action):

    def name(self) -> Text:
        return "ebdi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            user_event) -> List[Dict[Text, Any]]:   
        #global user_event
        global user_intent
        #global resp
        ## E conjunto de emociones
        global Emotions
        ## B conjunto de creencias
        global Beliefs
        ## D Conjunto de deseos generados por la creencia, pueden convertirse en intenciones
        global Desires
        ## I el conjunto intenciones/metas a realizar si se cumplen ciertas condiciones
        global Intents 

        newBelief = Beliefs.new_belief(user_event)     

        # la Emocion primaria
        E1 = Emotions.euf1(Intents,newBelief)
        print('-----PRIMARY EMOTION: ' + E1) 

        # BDI actualizacion        
        BDI.bdi(self,newBelief)             
        if(len(Intents.agent_intents)==0):
            Beliefs.del_belief(user_intent)
            user_intent = ''

        # la Emocion secundaria
        E2 = Emotions.euf2(Intents,Beliefs)
        print('-----SECONDARY EMOTION: ' + E2) 

        # if (inTime and E1 != E2):
        #    BDI.bdi(self,Beliefs.agent_beliefs)

        #Desires.agent_desires = [] 

        p = Plan.plan(self, Intents.agent_intents)  
        if Intents.agent_intents:
            del Intents.agent_intents[0]
            
        for i in p:
            print('--->' + i)
            exec(i) 

        return []

# actualizacion Beliefs Desires Intents
class BDI:

    def bdi(self,newBelief):     
        ## E conjunto de emociones
        global Emotions
        ## B conjunto de creencias
        global Beliefs
        ## D Conjunto de deseos generados por la creencia, pueden convertirse en intenciones
        global Desires
        ## I el conjunto intenciones/metas a realizar si se cumplen ciertas condiciones
        global Intents 

        #B = brf_in(E,I,Bm) # se actualizan las creencias
        Beliefs.brf_in(Emotions,Intents,newBelief)
        print('-----BELIEFS-----')
        for belief in Beliefs.agent_beliefs:
            print(belief[0], belief[1])

        #D = options(B,I) # se crean los deseos
        Desires.options(Beliefs,Intents)
        print('-----DESIRES-----')
        for desire in Desires.agent_desires:
            print(desire[0], desire[1])     

        #I = filterI(E,B,D,I)
        Intents.filterI(Emotions,Beliefs,Desires.agent_desires)
        print('-----INTENTS-----')
        for intent in Intents.agent_intents:
            print(intent)
        # se estan manteniendo deseos, asi que esta linea los elimina, pero se pueden mantener deseos?
        Desires.agent_desires = [] 

        return []

## Acciones ##

class Say(Action):

    def name(self) -> Text:
        return "say"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            resp) -> List[Dict[Text, Any]]:
        #global resp
        global daytime
        print('la respuesta es: ' + resp)
        print(f"{dt.datetime.now()}")
        #if name not null
        # dispatcher.utter_message(response=resp,name = daytime) 

        #tracker.slots['daytime'] = 'evening'
        #d = tracker.slots['daytime']#get_slot('daytime')
        #print("daytime: " + str(d))
        
        #SlotSet('daytime', 'evening')
        UnBuenSaludo.run(self, dispatcher, tracker, domain)

        #dispatcher.utter_message(response='utter_saludar')
        dispatcher.utter_message(response=resp)
        contador()
        print("dispatcher: " + str(count))  
        
        return []

##
class action_service_options(Action):

    def name(self) -> Text:
        return "action_service_options"

    def run (self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text,Any]) -> List[Dict[Text, Any]]: 

        buttons=[
            {"payload":'/hito1{"content_type":"hito1"}',"title":"Hito 1"},
            {"payload":'/hito2{"content_type":"hito2"}',"title":"Hito 2"}
            ]

        dispatcher.utter_message(text="Hitos:", buttons=buttons)   
        return []

class Plan:

    def plan(self, Intents):
        p = []    
        #global user_event
        #global resp
        global Be
        for intent in Intents:
            for idx, val in enumerate(intent):    
                # Seleccionamos la primera intencion y las acciones correspondientes        
                if val == 'acc_say':  
                    resp = intent[idx+1]
                    s = "Say.run(self, dispatcher, tracker, domain,'{0}')".format(str(resp))
                    p.append((s))

                if val == 'acc_new_belief':
                    user_event = ['say',intent[idx+1],Be,'','','']   
                    s = "EBDI.run(self, dispatcher, tracker, domain,{0})".format(user_event)
                    p.append((s))

                if val == 'acc_del_belief':
                    s = "Beliefs.del_belief('{0}')".format(str(intent[idx+1]))
                    p.append(s)

                if val == 'acc_fulfill':
                    s = "Beliefs.fulfill_belief('{0}')".format(str(intent[idx+1]))
                    p.append(s)
                #p = acciones a realizar        
        return p

class To_Speech(Action):

    def name(self) -> Text:
        return "to_speech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        global msg
        global count
        
        txt_responses = ''

        if count > 0:
            msg = get_latest_event(tracker.applied_events())        
            responses = msg[-count:]  
            txt = TXT()            
            print('-----RESPONSES-----')
            for e in responses:
                print('-' + str(e['text']))
                txt_responses += str(e['text'])
                txt_responses += ' '
            #ExecuteEBDI.execute_ebdi(resp,Emotions.tag())
            TXT.name(txt,txt_responses)
        count = 0

        return []


## Salida de la respuesta emocional en XML
class ExecuteEBDI:

    def execute_ebdi(message,tag):
        xml = XML()
        XML.name(xml,message,tag)        
        return "echo"

class TXT():
    def name(self,response) -> Text:
        output = open("speech.txt","w")
        print(response)
        output.write(str(response))
        output.close()
        return "echo"


## Salida de la respuesta emocional en XML
class XML():

    def name(self,response,tag) -> Text:
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xml:lang": "en-US"})
        voice = ET.SubElement(speak, "voice", name = "en-US-AriaNeural") 
        mstts = ET.SubElement(voice, "mstts:express-as", style = tag )
        mstts.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("respuesta.xml")
        return "echo"

## Se ejecuta una sola vez al principio de una conversacion
class Dictionary:

    def get_synonym_mapper():
        result_dict = {}
        for nlu_md in os.listdir("data"):
            if nlu_md == 'nlu.md':
                path_md = "data/{0}".format(nlu_md)
                nlu_md_file = load_data(path_md)
                nlu_md_json = nlu_md_file.nlu_as_json()
                for item in json.loads(nlu_md_json)['rasa_nlu_data']['entity_synonyms']:
                    result_dict[item['value']] = item['synonyms']
        return result_dict




class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Hello World")
        dispatcher.utter_message(text="Hello World!")
        return []

class UnBuenSaludo(Action):

    def name(self) -> Text:
        return "un_buen_saludo"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        tracker.slots["daytime"] = 'evening'
        daytime = 'evening'
        
        #print("un_buen_saludo")
        #dispatcher.utter_message(response='utter_saludar')
        SlotSet("daytime", daytime)
        return [SlotSet("daytime", daytime)]


class You_are(Action):
    def name(self) -> Text:
        return "you_are"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:        
        entities = tracker.latest_message['entities']
        slot_name = tracker.get_slot('name')
        print(entities)

        message = "Hola, encantado de conocerte!"

        for e in entities:
            if e['entity'] == 'name':
                name = e['value']
            if name == "ricardo":
                message = "Hey " + slot_name + ", que tal?"                
            if name == "amalia":
                message = "Hola Amalia, yo soy el sargento David Robertson, encantado"
        tag = "cheerful" 
        xml = XML()
        XML.name(xml,message,tag)
        dispatcher.utter_message(text=message)
        return []

class Info_fecha(Action):

    def name(self) -> Text:
        return "info_fecha"
    def run (self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:        
        entities = tracker.latest_message['entities']
        print(entities)
        message = 'Lo siento, no he encontrado nada relacionado con esa fecha'
        for e in entities:
            if e['entity'] == 'fecha':
                fecha = e['value']
                if fecha == '1350':
                    message = "Antoine de le Puy, peregrino a santiago y alcanza a oir el sonido de una campana entre la niebla mientras desciende de la montania"
                if fecha == '1813':
                    message = "Tengo informacion sobre unos soldados que durante la guerra de independencia Española se encargaban de vigilar la frontera con Francia"
        dispatcher.utter_message(text=message)
        return []

class Buscar_informacion(Action):

    def name(self) -> Text:
        return "buscar_informacion"
    def run (self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:  
        print("Accediendo a informacion...")
        """ acceder a slot values, ahi se encuentra la fecha """
        slot_fecha = tracker.get_slot('fecha')
        print(slot_fecha)
        message = 'Error, informacion NO localizada'
        if slot_fecha == '1350':
            message = "Escuchad companieros el sonido de la campana! Roncesvalles ya esta al alcance y podremos..."
        if slot_fecha == '1813':
            message = "...A principios de octubre la nieve cayo en tal cantidad como no habia visto en Escocia. Casi perdimos..."
        dispatcher.utter_message(text=message)
        return []

class GenerarXML(Action):

    def name(self) -> Text:
        return "generar_xml"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xml:lang": "en-US"})
        voice = ET.SubElement(speak, "voice", name = "en-US-AriaNeural") 
        mstts = ET.SubElement(voice, "mstts:express-as", style="cheerful" )
        mstts.text = "Mi respuesta es estar alegre."
        arbol = ET.ElementTree(speak)
        arbol.write("respuesta.xml")
        return []


class Aprendizaje(Action):

    def name(self) -> Text:
        return "aprendizaje"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:        
        entities = tracker.latest_message['entities']
        intent = tracker.latest_message['intent']
        text = tracker.latest_message['text']
        slot_name = tracker.get_slot('name')
        print(intent)
        print(entities)        
        print(text)
        print(tracker.latest_action_name)
        print(tracker.slots)
        message = "Comando de aprendizaje"
        dispatcher.utter_message(text=message)
        for e in entities:
            if e['entity'] == 'name':
                name = e['value']
            if name == "ricardo":
                message = "Hola Ricardo, estoy listo para aprender"
                '''a = tracker.'''
            if name != "ricardo":
                message = "Lo siento, no estas autorizado"     
        dispatcher.utter_message(text=message)
        return []

##class RestInput (InputChannel):
#    def _extract_metadata(self, req: Request) -> Text:
#            return req.json.get("metadata") or self.name()
#            @custom_webhook.route("/webhook", methods=["POST"])
#            async def receive(request: Request):
#               sender_id = await self._extract_sender(request)
#               text = self._extract_message(request)
#               metadata = self._extract_metadata(request)
#               metadata = "{\"metadata\": \"" + str(metadata) + "\"}"
#               metadata = json.loads(metadata)
#
#               try:
#                   await on_new_message(
#                       UserMessage(
#                           text, collector, sender_id, input_channel=input_channel, metadata=metadata
#                       )
#                   )